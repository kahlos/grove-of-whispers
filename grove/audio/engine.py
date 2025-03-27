# grove/audio/engine.py
# v40: Fix IndentationError, fix NameError in _generate_binaural_beats (AGAIN).

try: import sounddevice as sd
except ImportError: print("\nERROR: SD Missing\n"); sd = None
try: import numpy as np
except ImportError: print("\nERROR: NP Missing\n"); np = None

import threading
import time
import random
import sys
import traceback
from queue import Queue, Empty
from typing import Optional, Dict, List, Any, Tuple, Union

# Local imports
try: from .synth import generate_sine_wave, generate_lfo
except ImportError as e: print(f"Synth import Err: {e}"); generate_sine_wave = None; generate_lfo = None
try: from .. import config
except ImportError: config = type('config', (), {'DEBUG': False}) # Correct dummy

# --- Debugging Toggles ---
ENABLE_LFOS = False # Keep OFF
ENABLE_BINAURAL = True # Keep ON

# --- Constants ---
DEFAULT_SAMPLE_RATE = 44100; BUFFER_DURATION = 0.08; MIN_BASE_FREQ = 50; MAX_BASE_FREQ = 120
CROSSFADE_DURATION = 0.7; INITIAL_RAMP_DURATION = 0.2
BINAURAL_CARRIER_HZ = 120.0; BINAURAL_DIFFERENCE_HZ = 7.0; BINAURAL_AMPLITUDE = 0.15
# No DCB / Declick constants

# --- Mood Definitions ---
# Unchanged
MOOD_PRESETS: Dict[str, List[Tuple[float, float, float, float]]] = {
    "clearing_calm": [(1.0, 0.4, 0.1, 0.15), (1.5, 0.2, 0.15, 0.1), (2.0, 0.15, 0.08, 0.1), (3.0, 0.05, 0.3, 0.04)],
    "forest_neutral": [(1.0, 0.35, 0.12, 0.1), (1.498, 0.18, 0.2, 0.1), (2.5, 0.1, 0.25, 0.08)],
    "forest_mysterious": [(1.0, 0.3, 0.1, 0.1), (1.333, 0.2, 0.18, 0.1), (1.78, 0.15, 0.22, 0.08), (4.0, 0.04, 0.4, 0.03)],
    "woods_deep": [(1.0, 0.4, 0.08, 0.05), (1.189, 0.2, 0.15, 0.1), (1.682, 0.1, 0.2, 0.08)],
    "stream": [(1.0, 0.25, 0.2, 0.15), (2.0, 0.20, 0.25, 0.15), (2.5, 0.15, 0.3, 0.1), (3.5, 0.10, 0.4, 0.08)],
    "default": [(1.0, 0.3, 0.1, 0.1), (1.5, 0.15, 0.15, 0.08)]
}

# --- Helper Function for Ramps ---
def _calculate_equal_power_ramps(prog_start_norm: float, prog_end_norm: float, frames: int) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    if not np: return (None, None)
    lin_prog_ramp = np.linspace(prog_start_norm, prog_end_norm, frames, dtype=np.float32); lin_prog_ramp = np.clip(lin_prog_ramp, 0.0, 1.0)
    fade_in_ramp_eqp = np.sqrt(lin_prog_ramp); fade_out_ramp_eqp = np.sqrt(np.clip(1.0 - lin_prog_ramp, 0.0, 1.0))
    return fade_in_ramp_eqp, fade_out_ramp_eqp

class AudioEngine:
    """Audio engine with corrected scope/indentation."""

    def __init__(self, sample_rate: int = DEFAULT_SAMPLE_RATE):
        self._is_disabled = not (sd and np and generate_sine_wave and _calculate_equal_power_ramps)
        if ENABLE_LFOS and 'generate_lfo' not in globals(): self._is_disabled = True
        if self._is_disabled: print("AudioEngine disabled."); return
        self.sample_rate = sample_rate; self.buffer_size = int(BUFFER_DURATION * self.sample_rate)
        self._stream: Optional[sd.OutputStream] = None; self._thread: Optional[threading.Thread] = None; self._running: bool = False
        self._parameter_queue: Queue = Queue(maxsize=5)
        self._target_params: Dict[str, Any] = { 'base_freq': 65.41, 'mood': 'default', 'master_volume': 0.6 }
        self._current_params: Dict[str, Any] = self._target_params.copy()
        self._current_osc_times: List[float] = []; self._current_lfo_times: List[float] = []
        self._previous_osc_times: List[float] = []; self._previous_lfo_times: List[float] = []
        self._binaural_time_l: float = 0.0; self._binaural_time_r: float = 0.0
        self._crossfade_state: Dict[str, Any] = { 'active': False, 'progress_samples': 0, 'total_samples': int(CROSSFADE_DURATION * self.sample_rate), 'completion_logged': False} # Include flag
        self._previous_mood_key: Optional[str] = None
        self._initial_ramp_samples_done = 0; self._initial_ramp_total_samples = max(1, int(INITIAL_RAMP_DURATION * self.sample_rate)); self._is_initial_ramp = True
        # No DCBlock/Declick

    def _initialize_time_list_pair(self, num_oscillators: int, osc_times_list: List, lfo_times_list: List):
        num_oscillators = max(0, num_oscillators)
        if num_oscillators != len(osc_times_list): osc_times_list[:] = [0.0] * num_oscillators
        current_lfo_len = len(lfo_times_list)
        if num_oscillators > current_lfo_len: lfo_times_list.extend([0.0] * (num_oscillators - current_lfo_len))
        elif num_oscillators < current_lfo_len: lfo_times_list[:] = lfo_times_list[:num_oscillators]

    def _reset_binaural_times(self):
        self._binaural_time_l = 0.0; self._binaural_time_r = 0.0

    def _generate_audio_chunk(self, preset_data_list: List[Tuple[Union[float, int], ...]], base_freq: float, osc_times: List[float], lfo_times: List[float], frames: int ) -> Tuple[Optional[np.ndarray], bool]:
        # Generator (robust v39) unchanged internally
        if self._is_disabled or not np: return (np.zeros(frames, dtype=np.float32), False)
        num_oscillators = len(preset_data_list); buffer_duration_actual = frames / self.sample_rate
        if len(osc_times) != num_oscillators or len(lfo_times) != num_oscillators: return (np.zeros(frames, dtype=np.float32), False)
        if not isinstance(base_freq, (int, float)): return (np.zeros(frames, dtype=np.float32), False)
        total_wave = np.zeros(frames, dtype=np.float32); generation_successful_overall = True; MAX_LFO_DEPTH_SCALE = 0.90
        for i in range(num_oscillators):
            osc_start_time, lfo_start_time, osc_end_time, lfo_end_time = 0.0, 0.0, 0.0, 0.0
            current_osc_generated = False; amp_modulator = None
            try:
                if i >= len(osc_times) or i >= len(lfo_times): raise IndexError("Time OOB")
                osc_start_time = osc_times[i]; lfo_start_time = lfo_times[i]; osc_end_time = osc_start_time + buffer_duration_actual; lfo_end_time = lfo_start_time + buffer_duration_actual
                osc_params_tuple = preset_data_list[i];
                if not isinstance(osc_params_tuple, tuple) or len(osc_params_tuple)!=4: raise ValueError("Fmt")
                freq_mult, base_amp, lfo_rate, lfo_depth = osc_params_tuple
                if not all(isinstance(v,(int, float)) for v in osc_params_tuple): raise ValueError("Type")
                osc_frequency = max(0.0, base_freq * freq_mult); current_base_amp = max(0.0, base_amp)
                if ENABLE_LFOS and generate_lfo is not None:
                    current_lfo_rate = max(0.0, lfo_rate); current_lfo_depth = max(0.0, min(1.0, lfo_depth * MAX_LFO_DEPTH_SCALE))
                    effective_lfo_depth = current_base_amp * current_lfo_depth; effective_lfo_offset = current_base_amp * (1.0 - current_lfo_depth)
                    amp_modulator = generate_lfo(current_lfo_rate, buffer_duration_actual, self.sample_rate, depth=effective_lfo_depth, offset=effective_lfo_offset, start_time=lfo_start_time)
                    if amp_modulator is None: raise RuntimeError("LFO Fail")
                wave_chunk = None; amplitude_to_use = amp_modulator if (ENABLE_LFOS and amp_modulator is not None) else current_base_amp
                if osc_frequency > 0 and generate_sine_wave is not None:
                    wave_chunk, computed_osc_end_time = generate_sine_wave(osc_frequency, buffer_duration_actual, self.sample_rate, amplitude=amplitude_to_use, start_time=osc_start_time)
                    if wave_chunk is not None: osc_end_time = computed_osc_end_time; current_osc_generated = True
                    else: raise RuntimeError("Sine Fail")
                if current_osc_generated: total_wave[:min(frames, wave_chunk.shape[0])] += wave_chunk[:min(frames, wave_chunk.shape[0])]
            except (IndexError, ValueError, RuntimeError) as e: generation_successful_overall = False;
            except Exception as e: generation_successful_overall = False; print(f"[UNEX GEN {i}]: {e}");
            finally: # Robust Time Update
                if i < len(osc_times): osc_times[i] = osc_end_time
                if i < len(lfo_times): lfo_times[i] = lfo_end_time
        if not generation_successful_overall: return (np.zeros(frames, dtype=np.float32), False)
        return total_wave, True


    def _generate_binaural_beats(self, frames: int) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """ Generates L/R binaural channels, fixed constant access. """
        if self._is_disabled or not np or not generate_sine_wave or not ENABLE_BINAURAL: return None
        buffer_duration_actual = frames / self.sample_rate

        # *** FIX: Access constants correctly within method scope ***
        freq_l = BINAURAL_CARRIER_HZ
        freq_r = BINAURAL_CARRIER_HZ + BINAURAL_DIFFERENCE_HZ
        amp = BINAURAL_AMPLITUDE

        wave_l_chunk, end_time_l = generate_sine_wave(freq_l, buffer_duration_actual, self.sample_rate, amplitude=amp, start_time=self._binaural_time_l); self._binaural_time_l = end_time_l
        wave_r_chunk, end_time_r = generate_sine_wave(freq_r, buffer_duration_actual, self.sample_rate, amplitude=amp, start_time=self._binaural_time_r); self._binaural_time_r = end_time_r

        if wave_l_chunk is not None and wave_r_chunk is not None:
             if wave_l_chunk.shape[0] != frames: wave_l_chunk = np.pad(wave_l_chunk, (0, frames - wave_l_chunk.shape[0]), mode='constant') if wave_l_chunk.shape[0] < frames else wave_l_chunk[:frames]
             if wave_r_chunk.shape[0] != frames: wave_r_chunk = np.pad(wave_r_chunk, (0, frames - wave_r_chunk.shape[0]), mode='constant') if wave_r_chunk.shape[0] < frames else wave_r_chunk[:frames]
             return wave_l_chunk.astype(np.float32), wave_r_chunk.astype(np.float32)
        else: print("[WARN] Binaural gen failed."); return None


    def _audio_callback(self, outdata: np.ndarray, frames: int, time_info, status):
        """Callback: Stereo Mix, EqPower CF, Initial ramp. Fixed syntax/scope."""
        if self._is_disabled or not np: outdata.fill(0); return
        if status and config.DEBUG: print(f"Audio Status: {status}", flush=True)

        try:
            # --- Check Queue & Handle Mood Change Request ---
            mood_change_request_mood: Optional[str] = None; new_target_params: Dict[str, Any] = {}
            while not self._parameter_queue.empty():
                try:
                    new_params = self._parameter_queue.get_nowait()
                    self._parameter_queue.task_done()
                # ** SYNTAX FIX: Correct except blocks **
                except Empty:
                    break
                except Exception as qe:
                    print(f"Queue Err: {qe}", flush=True)
                    continue # Skip to next item if error reading one

                if 'mood' in new_params: mood_change_request_mood = new_params.pop('mood')
                new_target_params.update(new_params)
            self._target_params.update(new_target_params)

            # Initiate Crossfade
            if mood_change_request_mood and mood_change_request_mood != self._current_params['mood']:
                 self._previous_mood_key = self._current_params['mood']; self._previous_osc_times = self._current_osc_times[:]; self._previous_lfo_times = self._current_lfo_times[:]
                 self._target_params['mood'] = mood_change_request_mood
                 if config.DEBUG: print(f"[DEBUG] CF Trig: '{self._previous_mood_key}'({len(self._previous_osc_times)}o) -> '{self._target_params['mood']}'")
                 target_preset = MOOD_PRESETS.get(self._target_params['mood'], MOOD_PRESETS['default'])
                 self._initialize_time_list_pair(len(target_preset), self._current_osc_times, self._current_lfo_times)
                 if config.DEBUG: print(f"[DEBUG] -> Target:{len(target_preset)}o, Cur times:{len(self._current_osc_times)}")
                 self._crossfade_state = {'active': True, 'progress_samples': 0, 'total_samples': max(1, int(CROSSFADE_DURATION * self.sample_rate)), 'completion_logged': False} # Add flag

            # Update Current Params (Instant Update)
            self._current_params['base_freq'] = self._target_params['base_freq']; self._current_params['master_volume'] = self._target_params['master_volume']; self._current_params['mood'] = self._target_params['mood']
            callback_base_freq = float(self._current_params.get('base_freq', 65.41))


            # --- Generate MONO Drone Layer (Crossfade or Normal) ---
            mono_drone_wave = np.zeros(frames, dtype=np.float32); drone_generated = False
            # Store fade status for this specific callback invocation
            is_crossfading_this_buffer = self._crossfade_state['active']

            if is_crossfading_this_buffer and _calculate_equal_power_ramps is not None:
                # Crossfade logic remains the same (separate gen + eqpower ramps)
                prog_start, total_samples = self._crossfade_state['progress_samples'], self._crossfade_state['total_samples']; prog_end = prog_start + frames
                p_start_norm = max(0.0, min(1.0, prog_start/total_samples)); p_end_norm = max(0.0, min(1.0, prog_end/total_samples))
                fade_in_ramp, fade_out_ramp = _calculate_equal_power_ramps(p_start_norm, p_end_norm, frames)
                final_wave_prev = np.zeros(frames, dtype=np.float32); final_wave_curr = np.zeros(frames, dtype=np.float32)
                if self._previous_mood_key and fade_out_ramp is not None:
                     prev_preset = MOOD_PRESETS.get(self._previous_mood_key, []);
                     if len(self._previous_osc_times) == len(prev_preset):
                         prev_wave, success = self._generate_audio_chunk(prev_preset, callback_base_freq, self._previous_osc_times, self._previous_lfo_times, frames)
                         if success and prev_wave is not None: final_wave_prev = prev_wave * fade_out_ramp; drone_generated = True
                target_preset = MOOD_PRESETS.get(self._target_params['mood'], MOOD_PRESETS['default'])
                if len(self._current_osc_times) == len(target_preset):
                    if fade_in_ramp is not None:
                        curr_wave, success = self._generate_audio_chunk(target_preset, callback_base_freq, self._current_osc_times, self._current_lfo_times, frames)
                        if success and curr_wave is not None: final_wave_curr = curr_wave * fade_in_ramp; drone_generated = True
                mono_drone_wave = final_wave_prev + final_wave_curr
                # Update fade state AFTER generating this buffer's audio
                self._crossfade_state['progress_samples'] = prog_end
                if self._crossfade_state['progress_samples'] >= total_samples:
                    self._crossfade_state['active'] = False # Deactivate
                    self._previous_mood_key = None
                    if config.DEBUG and not self._crossfade_state.get('completion_logged', True): # Only print once
                        print("[DEBUG] CF Complete.")
                        self._crossfade_state['completion_logged'] = True # Mark as printed
            else: # Normal Playback
                 # Reset completion flag if we're no longer crossfading
                 if not self._crossfade_state.get('completion_logged', True): self._crossfade_state['completion_logged'] = False

                 current_preset = MOOD_PRESETS.get(self._target_params['mood'], MOOD_PRESETS['default'])
                 if len(self._current_osc_times) != len(current_preset): self._initialize_time_list_pair(len(current_preset), self._current_osc_times, self._current_lfo_times)
                 mono_drone_wave, success = self._generate_audio_chunk(current_preset, callback_base_freq, self._current_osc_times, self._current_lfo_times, frames)
                 if success: drone_generated = True;
                 if self._previous_mood_key is not None: self._previous_mood_key = None


            # --- Generate STEREO Binaural ---
            binaural_stereo_pair = self._generate_binaural_beats(frames)

            # --- Combine to STEREO Output Buffer ---
            stereo_output = np.zeros((frames, 2), dtype=np.float32)
            buffer_contains_sound = False
            if drone_generated: stereo_output[:, 0] += mono_drone_wave; stereo_output[:, 1] += mono_drone_wave; buffer_contains_sound = True
            if binaural_stereo_pair is not None: stereo_output[:, 0] += binaural_stereo_pair[0]; stereo_output[:, 1] += binaural_stereo_pair[1]; buffer_contains_sound = True

            # --- Post-processing (Stereo) ---
            if buffer_contains_sound:
                master_vol = self._current_params.get('master_volume', 0.6)
                # Initial Ramp
                if self._is_initial_ramp:
                    ramp_start, ramp_end, total_ramp = self._initial_ramp_samples_done, self._initial_ramp_samples_done + frames, self._initial_ramp_total_samples
                    start_gain = max(0.0, min(1.0, ramp_start / total_ramp)) if total_ramp > 0 else 1.0; end_gain = max(0.0, min(1.0, ramp_end / total_ramp)) if total_ramp > 0 else 1.0
                    if start_gain < 1.0 or end_gain < 1.0:
                         initial_gain_ramp = np.linspace(start_gain, end_gain, frames, dtype=np.float32)[:, np.newaxis]
                         stereo_output *= initial_gain_ramp
                    self._initial_ramp_samples_done = ramp_end
                    if self._initial_ramp_samples_done >= total_ramp: self._is_initial_ramp = False;
                    if config.DEBUG: print("[DEBUG] Initial ramp done.") # Single print
                # Master Volume
                stereo_output *= master_vol
                # No DC Blocker / No Declicking
                # Clip LAST
                np.clip(stereo_output, -1.0, 1.0, out=stereo_output)
                # Frame Clamp Safety
                if stereo_output.shape[0] != frames: stereo_output = stereo_output[:frames, :] if stereo_output.shape[0] > frames else np.pad(stereo_output, ((0, frames - stereo_output.shape[0]),(0,0)))
                outdata[:] = stereo_output
            else: outdata.fill(0) # Silence

        # Catch all exceptions in callback to prevent crashing audio thread
        except Exception as e: print(f"---!! Crit CB Err !!---\n{type(e).__name__}: {e}", file=sys.stderr, flush=True); traceback.print_exc(file=sys.stderr); sys.stderr.flush(); outdata.fill(0)

    # --- _run, update_parameters, start ---
    def _run(self): # Same simplified logic v39
        if self._is_disabled: return
        stream_context = None
        try:
            stream_context = sd.OutputStream( samplerate=self.sample_rate, blocksize=self.buffer_size, channels=2, dtype='float32', callback=self._audio_callback, latency='low') # STEREO
            with stream_context as stream:
                if config.DEBUG: print(f"Audio stream active (STEREO, {self.sample_rate} Hz, {self.buffer_size} frames, {stream.latency:.4f}s latency)")
                else: print("Audio stream active.")
                while self._running: time.sleep(BUFFER_DURATION)
        except sd.PortAudioError as pae: print(f"PortAudio Error: {pae}")
        except ValueError as ve: print(f"Stream Setup ValueError: {ve} (Check Stereo?)")
        except Exception as e: print(f"Audio thread error: {e}"); traceback.print_exc()
        finally: self._running = False; self._stream = None; print("Audio thread _run method finished.")

    def update_parameters(self, params: Dict[str, Any]): # Same v39
        if self._is_disabled: return
        self._parameter_queue.put(params)

    def start(self): # Same v39
        if self._is_disabled: print("Cannot start: Disabled."); return
        if self._running: print("Already running."); return
        try: sd.check_output_settings(samplerate=self.sample_rate, channels=2, dtype='float32') # STEREO
        except Exception as e: print(f"Audio settings check FAIL (Stereo?): {e}. Check device."); return
        self._running = True; self._is_initial_ramp = True; self._initial_ramp_samples_done = 0
        self._reset_binaural_times()
        preset = MOOD_PRESETS.get(self._target_params['mood'], MOOD_PRESETS['default'])
        self._initialize_time_list_pair(len(preset), self._current_osc_times, self._current_lfo_times)
        self._thread = threading.Thread(target=self._run, daemon=False, name="AudioEngineThread")
        self._thread.start()
        print("Audio engine thread started.")

    # *** stop Method: Corrected v39 applied ***
    def stop(self):
        """Simplified shutdown: Signal loop and join thread. Correct scope."""
        thread = self._thread # Assign first
        if self._is_disabled: return
        if not self._running and not (thread and thread.is_alive()): return

        print("Stop requested...");
        self._running = False # Signal loop

        if thread and thread.is_alive():
            print(f"Waiting for '{thread.name}' join...");
            thread.join(timeout=1.5) # Wait
            if thread.is_alive(): print("[WARN] Audio thread join timed out!")
            else: print("Audio thread joined.")

        self._thread = None; self._stream = None; # Clear refs after attempt
        print("Audio engine stop sequence complete.")


print("[engine.py] Corrected binaural NameError & except syntax.")