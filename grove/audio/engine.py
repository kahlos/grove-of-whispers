# grove/audio/engine.py
# v34: FIX UnboundLocalError in stop() AGAIN. Keep click compromises.

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

# --- Debugging Toggles ---
ENABLE_LFOS = False # <<< *** KEEPING LFOS DISABLED ***

# --- Constants ---
DEFAULT_SAMPLE_RATE = 44100
BUFFER_DURATION = 0.08
MIN_BASE_FREQ = 50
MAX_BASE_FREQ = 120
CROSSFADE_DURATION = 0.7 # Keep longer duration
INITIAL_RAMP_DURATION = 0.2
# No DC Blocker, No edge declicking/windowing

# --- Mood Definitions ---
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
    """Audio engine - No edge declicking/DCBlock, fixed shutdown scope."""

    def __init__(self, sample_rate: int = DEFAULT_SAMPLE_RATE):
        self._is_disabled = not (sd and np and generate_sine_wave and generate_lfo and _calculate_equal_power_ramps)
        if self._is_disabled: print("AudioEngine disabled."); return
        self.sample_rate = sample_rate; self.buffer_size = int(BUFFER_DURATION * self.sample_rate)
        self._stream: Optional[sd.OutputStream] = None; self._thread: Optional[threading.Thread] = None; self._running: bool = False
        self._parameter_queue: Queue = Queue(maxsize=5)
        self._target_params: Dict[str, Any] = { 'base_freq': 65.41, 'mood': 'default', 'master_volume': 0.6 }
        self._current_params: Dict[str, Any] = self._target_params.copy()
        self._current_osc_times: List[float] = []; self._current_lfo_times: List[float] = []
        self._previous_osc_times: List[float] = []; self._previous_lfo_times: List[float] = []
        self._crossfade_state: Dict[str, Any] = { 'active': False, 'progress_samples': 0, 'total_samples': int(CROSSFADE_DURATION * self.sample_rate) }
        self._previous_mood_key: Optional[str] = None
        # No Declick/Hann state
        self._initial_ramp_samples_done = 0; self._initial_ramp_total_samples = max(1, int(INITIAL_RAMP_DURATION * self.sample_rate)); self._is_initial_ramp = True
        # No DC Blocker state

    def _initialize_time_list_pair(self, num_oscillators: int, osc_times_list: List, lfo_times_list: List):
        # Keeps LFO phase unless size changes
        num_oscillators = max(0, num_oscillators)
        if num_oscillators != len(osc_times_list): osc_times_list[:] = [0.0] * num_oscillators
        current_lfo_len = len(lfo_times_list)
        if num_oscillators > current_lfo_len: lfo_times_list.extend([0.0] * (num_oscillators - current_lfo_len))
        elif num_oscillators < current_lfo_len: lfo_times_list[:] = lfo_times_list[:num_oscillators]

    def _generate_audio_chunk(self,
        preset_data_list: List[Tuple[Union[float, int], ...]],
        base_freq: float, osc_times: List[float], lfo_times: List[float], frames: int
    ) -> Tuple[Optional[np.ndarray], bool]:
        # Generator logic unchanged (v32 robust version)
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
                if ENABLE_LFOS:
                    current_lfo_rate = max(0.0, lfo_rate); current_lfo_depth = max(0.0, min(1.0, lfo_depth * MAX_LFO_DEPTH_SCALE))
                    effective_lfo_depth = current_base_amp * current_lfo_depth; effective_lfo_offset = current_base_amp * (1.0 - current_lfo_depth)
                    amp_modulator = generate_lfo(current_lfo_rate, buffer_duration_actual, self.sample_rate, depth=effective_lfo_depth, offset=effective_lfo_offset, start_time=lfo_start_time)
                    if amp_modulator is None: raise RuntimeError("LFO Fail")
                # Time advances in finally
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


    def _audio_callback(self, outdata: np.ndarray, frames: int, time_info, status):
        """Callback: EqPower crossfade, Initial ramp, NO declicking."""
        if self._is_disabled or not np: outdata.fill(0); return
        if status: print(f"Audio Status: {status}", flush=True)

        try:
            # Queue / Crossfade Setup / Instant Param Update (Same as v32)
            mood_change_request_mood: Optional[str] = None; new_target_params: Dict[str, Any] = {}
            while not self._parameter_queue.empty():
                try: new_params = self._parameter_queue.get_nowait(); self._parameter_queue.task_done()
                except Empty: break;
                except Exception as qe: print(f"Queue Err: {qe}", flush=True); continue
                if 'mood' in new_params: mood_change_request_mood = new_params.pop('mood')
                new_target_params.update(new_params)
            self._target_params.update(new_target_params)
            if mood_change_request_mood and mood_change_request_mood != self._current_params['mood']:
                 self._previous_mood_key = self._current_params['mood']; self._previous_osc_times = self._current_osc_times[:]; self._previous_lfo_times = self._current_lfo_times[:]
                 self._target_params['mood'] = mood_change_request_mood
                 print(f"[DEBUG] CF Trig: '{self._previous_mood_key}'({len(self._previous_osc_times)}o) -> '{self._target_params['mood']}'")
                 target_preset = MOOD_PRESETS.get(self._target_params['mood'], MOOD_PRESETS['default'])
                 self._initialize_time_list_pair(len(target_preset), self._current_osc_times, self._current_lfo_times) # Resizes CURRENT lists
                 print(f"[DEBUG] -> Target:{len(target_preset)}o, Cur times:{len(self._current_osc_times)}")
                 self._crossfade_state = {'active': True, 'progress_samples': 0, 'total_samples': max(1, int(CROSSFADE_DURATION * self.sample_rate))}
            self._current_params['base_freq'] = self._target_params['base_freq']; self._current_params['master_volume'] = self._target_params['master_volume']; self._current_params['mood'] = self._target_params['mood']
            callback_base_freq = float(self._current_params.get('base_freq', 65.41))

            # Generate Audio (Separate Gen + EqPower Ramps - logic same)
            final_wave = np.zeros(frames, dtype=np.float32); buffer_generated = False
            if self._crossfade_state['active'] and _calculate_equal_power_ramps is not None:
                # Crossfade generation (v32)
                prog_start, total_samples = self._crossfade_state['progress_samples'], self._crossfade_state['total_samples']; prog_end = prog_start + frames
                p_start_norm = max(0.0, min(1.0, prog_start/total_samples)); p_end_norm = max(0.0, min(1.0, prog_end/total_samples))
                fade_in_ramp, fade_out_ramp = _calculate_equal_power_ramps(p_start_norm, p_end_norm, frames)
                final_wave_prev = np.zeros(frames, dtype=np.float32); final_wave_curr = np.zeros(frames, dtype=np.float32)
                if self._previous_mood_key and fade_out_ramp is not None:
                     prev_preset = MOOD_PRESETS.get(self._previous_mood_key, []);
                     if len(self._previous_osc_times) == len(prev_preset):
                         prev_wave, success = self._generate_audio_chunk(prev_preset, callback_base_freq, self._previous_osc_times, self._previous_lfo_times, frames)
                         if success and prev_wave is not None: final_wave_prev = prev_wave * fade_out_ramp; buffer_generated = True
                target_preset = MOOD_PRESETS.get(self._target_params['mood'], MOOD_PRESETS['default'])
                if len(self._current_osc_times) == len(target_preset):
                    if fade_in_ramp is not None:
                        curr_wave, success = self._generate_audio_chunk(target_preset, callback_base_freq, self._current_osc_times, self._current_lfo_times, frames)
                        if success and curr_wave is not None: final_wave_curr = curr_wave * fade_in_ramp; buffer_generated = True
                final_wave = final_wave_prev + final_wave_curr # Combine
                # Update State
                self._crossfade_state['progress_samples'] = prog_end
                if self._crossfade_state['progress_samples'] >= total_samples:
                    self._crossfade_state['active'] = False; self._previous_mood_key = None; print("[DEBUG] CF Complete.")
            else: # Normal Playback
                current_preset = MOOD_PRESETS.get(self._target_params['mood'], MOOD_PRESETS['default'])
                if len(self._current_osc_times) != len(current_preset): self._initialize_time_list_pair(len(current_preset), self._current_osc_times, self._current_lfo_times)
                final_wave, success = self._generate_audio_chunk(current_preset, callback_base_freq, self._current_osc_times, self._current_lfo_times, frames)
                if success: buffer_generated = True;
                if self._previous_mood_key is not None: self._previous_mood_key = None

            # --- Post-processing ---
            if buffer_generated:
                master_vol = self._current_params.get('master_volume', 0.6)
                # Initial Ramp
                if self._is_initial_ramp:
                    ramp_start, ramp_end, total_ramp = self._initial_ramp_samples_done, self._initial_ramp_samples_done + frames, self._initial_ramp_total_samples
                    start_gain = max(0.0, min(1.0, ramp_start / total_ramp)) if total_ramp > 0 else 1.0; end_gain = max(0.0, min(1.0, ramp_end / total_ramp)) if total_ramp > 0 else 1.0
                    if start_gain < 1.0 or end_gain < 1.0: final_wave *= np.linspace(start_gain, end_gain, frames, dtype=np.float32)
                    self._initial_ramp_samples_done = ramp_end
                    if self._initial_ramp_samples_done >= total_ramp: self._is_initial_ramp = False;
                # Master Volume
                final_wave *= master_vol
                # NO DC Blocker / NO Declicking ramps applied here
                # Clip LAST
                np.clip(final_wave, -1.0, 1.0, out=final_wave)
                # Frame Clamp Safety Check
                if final_wave.shape[0] != frames:
                    if final_wave.shape[0] > frames: final_wave = final_wave[:frames]
                    else: final_wave = np.pad(final_wave, (0, frames - final_wave.shape[0]))
                outdata[:] = final_wave.reshape(-1, 1)
            else: outdata.fill(0)

        except Exception as e: print(f"---!! Crit CB Err !!---\n{type(e).__name__}: {e}", file=sys.stderr, flush=True); traceback.print_exc(file=sys.stderr); sys.stderr.flush(); outdata.fill(0)


    # --- _run, update_parameters, start Methods ---
    def _run(self):
        # Unchanged v32
        if self._is_disabled: return
        stream_context = None
        try:
            stream_context = sd.OutputStream( samplerate=self.sample_rate, blocksize=self.buffer_size, channels=1, dtype='float32', callback=self._audio_callback, latency='low')
            with stream_context as stream:
                print(f"Audio stream active ({self.sample_rate} Hz, {self.buffer_size} frames, {stream.latency:.4f}s latency)")
                while self._running: time.sleep(BUFFER_DURATION)
        except sd.PortAudioError as pae: print(f"PortAudio Error: {pae}")
        except Exception as e: print(f"Audio thread error: {e}"); traceback.print_exc()
        finally: self._running = False; self._stream = None; print("Audio thread _run method finished.")

    def update_parameters(self, params: Dict[str, Any]):
        # Unchanged v32
        if self._is_disabled: return
        self._parameter_queue.put(params)

    def start(self):
        # Unchanged v32
        if self._is_disabled: print("Cannot start: Disabled."); return
        if self._running: print("Already running."); return
        try: sd.check_output_settings(samplerate=self.sample_rate, channels=1, dtype='float32')
        except Exception as e: print(f"Audio settings check FAIL: {e}. Check device."); return
        self._running = True; self._is_initial_ramp = True; self._initial_ramp_samples_done = 0
        # No DC Blocker reset
        preset = MOOD_PRESETS.get(self._target_params['mood'], MOOD_PRESETS['default'])
        self._initialize_time_list_pair(len(preset), self._current_osc_times, self._current_lfo_times)
        # No declick/hann init
        self._thread = threading.Thread(target=self._run, daemon=False, name="AudioEngineThread")
        self._thread.start()
        print("Audio engine thread start requested.")

    # *** CORRECTED STOP METHOD ***
    def stop(self):
        """Simplified shutdown: Signal loop and join thread."""
        if self._is_disabled: return
        # ** FIX: Assign thread to local var *before* checking if running **
        thread = self._thread
        # Now checks are safe
        if not self._running and not (thread and thread.is_alive()):
            # print("Engine stop: Not running.") # Reduce noise
            return

        print("Stop requested...");
        self._running = False # Signal loop

        # Check the local 'thread' variable assigned at the start
        if thread and thread.is_alive():
            print(f"Waiting for '{thread.name}' join...");
            thread.join(timeout=1.5) # Wait for loop/context manager to finish
            if thread.is_alive():
                print("[WARN] Audio thread join timed out!")
            else:
                print("Audio thread joined.")
        # else: print("Audio thread already finished or none existed.")

        # Clear instance refs after checking/joining
        self._thread = None; self._stream = None;
        print("Audio engine stop sequence complete.")


print("[engine.py] Corrected shutdown scope. Using config from v31 (No DCB/Declick).")