# grove/audio/engine.py
# Manages audio stream, generation parameters, background thread, and phase continuity.

try:
    import sounddevice as sd
except ImportError:
    print("\n--- ERROR ---")
    print("Failed to import 'sounddevice'. Install: pip install sounddevice")
    print("May require PortAudio library (e.g., 'sudo apt-get install libportaudio2').")
    print("-------------\n")
    sd = None

try:
    import numpy as np
except ImportError:
    print("\n--- ERROR ---")
    print("Failed to import 'numpy' in audio engine. Install: pip install numpy")
    print("-------------\n")
    np = None

import threading
import time
import random
from queue import Queue, Empty
from typing import Optional, Dict, List, Any, Tuple # Ensure all needed types are here

# Local imports
try:
    # Ensure synth.py has loaded ok, it might set generate_sine_wave=None if numpy fails
    from .synth import generate_sine_wave, generate_lfo
except ImportError as e:
    print(f"Error importing synth functions in engine.py: {e}")
    generate_sine_wave = None
    generate_lfo = None

# --- Constants ---
DEFAULT_SAMPLE_RATE = 44100
BUFFER_DURATION = 0.1 # seconds - potentially reduced for quicker response
MIN_BASE_FREQ = 50
MAX_BASE_FREQ = 120

# --- Mood Definitions (Frequencies relative to base, base amplitude, LFO rate, LFO depth) ---
# Ensure keys here match the `audio_mood` strings used in locations.py
MOOD_PRESETS: Dict[str, List[Tuple[float, float, float, float]]] = {
    "clearing_calm": [(1.0, 0.4, 0.1, 0.15), (1.5, 0.2, 0.15, 0.1), (2.0, 0.15, 0.08, 0.1), (3.0, 0.05, 0.3, 0.04)],
    "forest_neutral": [(1.0, 0.35, 0.12, 0.1), (1.498, 0.18, 0.2, 0.1), (2.5, 0.1, 0.25, 0.08)],
    "forest_mysterious": [(1.0, 0.3, 0.1, 0.1), (1.333, 0.2, 0.18, 0.1), (1.78, 0.15, 0.22, 0.08), (4.0, 0.04, 0.4, 0.03)],
    "woods_deep": [(1.0, 0.4, 0.08, 0.05), (1.189, 0.2, 0.15, 0.1), (1.682, 0.1, 0.2, 0.08)],
    "stream": [(1.0, 0.25, 0.2, 0.15), (2.0, 0.20, 0.25, 0.15), (2.5, 0.15, 0.3, 0.1), (3.5, 0.10, 0.4, 0.08)],
    "default": [(1.0, 0.3, 0.1, 0.1), (1.5, 0.15, 0.15, 0.08)] # Fallback
}


class AudioEngine:
    """Manages dynamic audio generation and playback with phase continuity."""

    def __init__(self, sample_rate: int = DEFAULT_SAMPLE_RATE):
        if not sd or not np:
            print("AudioEngine disabled due to missing dependencies (sounddevice or numpy).")
            self._is_disabled = True
            return # Don't initialize further if dependencies missing

        self._is_disabled = False
        self.sample_rate = sample_rate
        self.buffer_size = int(BUFFER_DURATION * self.sample_rate)
        self._stream: Optional[sd.OutputStream] = None
        self._thread: Optional[threading.Thread] = None
        self._running: bool = False
        self._parameter_queue: Queue = Queue(maxsize=5) # Allow few queued updates

        # --- State for Audio Generation ---
        # Target parameters requested via update_parameters
        self._target_params: Dict[str, Any] = { 'base_freq': 65.41, 'mood': 'default', 'master_volume': 0.6 }
        # Current parameters, interpolated towards target
        self._current_params: Dict[str, Any] = self._target_params.copy()
        # Holds the current 'time' for each oscillator (phase tracking)
        self._oscillator_times: List[float] = []
        # LFOs usually don't need strict continuity, but we can track time for them too if needed
        self._lfo_times: List[float] = []
        self._last_preset_size = 0 # To detect when mood changes require resizing time buffers

    def _initialize_oscillator_times(self, num_oscillators: int):
        """Resets oscillator time tracking lists to the correct size."""
        if num_oscillators != len(self._oscillator_times):
             print(f"[DEBUG] Resizing oscillator time tracking from {len(self._oscillator_times)} to {num_oscillators}")
             self._oscillator_times = [0.0] * num_oscillators
             self._lfo_times = [random.random() * 10] * num_oscillators # Start LFOs at random phase points
             self._last_preset_size = num_oscillators

    def _audio_callback(self, outdata: np.ndarray, frames: int, time_info, status):
        """Called by sounddevice to fill the output buffer."""
        if not np: # Final check inside callback
             outdata.fill(0); return

        if status: print(f"Audio Status Warning: {status}", flush=True)

        try:
            # --- Update Target Params from Queue ---
            updated_mood = False
            while not self._parameter_queue.empty():
                try:
                    new_params = self._parameter_queue.get_nowait()
                    if 'mood' in new_params and new_params['mood'] != self._target_params['mood']:
                         updated_mood = True
                    self._target_params.update(new_params)
                    self._parameter_queue.task_done()
                except Empty: break # Should not happen, but safety
                except Exception as qe: print(f"Error processing parameter queue: {qe}")


            # --- Smooth parameter transitions ---
            interp_factor = 0.02 # Slower interpolation might sound smoother
            # Interpolate frequency
            target_freq = self._target_params['base_freq']
            self._current_params['base_freq'] += (target_freq - self._current_params['base_freq']) * interp_factor
            # Interpolate volume
            target_vol = self._target_params['master_volume']
            self._current_params['master_volume'] += (target_vol - self._current_params['master_volume']) * interp_factor * 0.5 # Slower volume change

            # Update mood directly - applying interpolation to preset values is more complex
            current_mood = self._target_params['mood'] # Use the target mood directly for preset lookup
            self._current_params['mood'] = current_mood


            # --- Get preset and ensure time tracking is sized correctly ---
            preset = MOOD_PRESETS.get(current_mood, MOOD_PRESETS['default'])
            num_oscillators = len(preset)
            # If mood changed (or first run), resize time tracking arrays
            if updated_mood or num_oscillators != self._last_preset_size:
                 self._initialize_oscillator_times(num_oscillators)

            if num_oscillators == 0: # Handle empty preset case
                outdata.fill(0)
                return


            # --- Prepare parameters for this buffer ---
            base_freq = self._current_params['base_freq']
            master_volume = self._current_params['master_volume']
            total_wave = np.zeros(frames, dtype=np.float32) # Buffer to accumulate waves

            # --- Generate Each Oscillator with Time Continuity ---
            for i in range(num_oscillators):
                freq_mult, base_amp, lfo_rate, lfo_depth = preset[i]
                osc_frequency = base_freq * freq_mult
                osc_start_time = self._oscillator_times[i]
                lfo_start_time = self._lfo_times[i] # Use separate time tracking for LFO phase if desired

                # Generate LFO for amplitude modulation for *this specific oscillator*
                # Depth is scaled by base_amp, Offset ensures modulation around base_amp
                effective_lfo_depth = base_amp * lfo_depth
                effective_lfo_offset = base_amp * (1.0 - lfo_depth)
                amp_modulator = generate_lfo(lfo_rate, BUFFER_DURATION, self.sample_rate,
                                             depth=effective_lfo_depth, offset=effective_lfo_offset,
                                             start_time=lfo_start_time)
                # Update LFO time tracker (simple accumulation, same as oscillator)
                self._lfo_times[i] = lfo_start_time + BUFFER_DURATION


                if amp_modulator is not None:
                    # Generate the main sine wave, modulated by the LFO amplitude
                    wave_chunk, end_time = generate_sine_wave(
                        osc_frequency, BUFFER_DURATION, self.sample_rate,
                        amplitude=amp_modulator, # Pass the generated LFO array
                        start_time=osc_start_time
                    )

                    # Accumulate the generated wave chunk
                    if wave_chunk is not None:
                         # Ensure length matches frames (handle potential slight timing discrepancies)
                         if wave_chunk.shape[0] == frames:
                             total_wave += wave_chunk
                         elif wave_chunk.shape[0] > frames:
                             total_wave += wave_chunk[:frames]
                         else: # Pad if too short
                             total_wave[:wave_chunk.shape[0]] += wave_chunk

                    # Store the end time for the next callback for this oscillator
                    self._oscillator_times[i] = end_time
                else:
                     # If LFO generation failed, advance time anyway
                     self._oscillator_times[i] = osc_start_time + BUFFER_DURATION


            # --- Post-processing ---
            # Apply master volume
            final_wave = total_wave * master_volume

            # Simple hard clipping to prevent > +/- 1.0 (more advanced limiting could be used)
            np.clip(final_wave, -1.0, 1.0, out=final_wave)

            # Ensure shape matches outdata (frames, channels=1)
            outdata[:] = final_wave.reshape(-1, 1)

        except Exception as e:
            print(f"Error in audio callback: {e}", flush=True)
            import traceback
            traceback.print_exc()
            outdata.fill(0) # Output silence if anything goes wrong


    def _run(self):
        """The main loop for the audio thread."""
        # Dependency check is now done in __init__ and start
        if self._is_disabled: return

        try:
            self._stream = sd.OutputStream(
                samplerate=self.sample_rate,
                blocksize=self.buffer_size,
                channels=1, # Mono
                dtype='float32',
                callback=self._audio_callback,
                latency='low' # Request lower latency
            )
            with self._stream:
                print(f"Audio stream started (SR: {self.sample_rate}, BufSiz: {self.buffer_size}, Latency: {self._stream.latency:.4f}s)")
                while self._running:
                    # No need to process queue here anymore, _audio_callback handles it
                    # Just keep the thread alive while the stream is running
                    time.sleep(BUFFER_DURATION) # Sleep interval based on buffer

        except sd.PortAudioError as pae:
             print(f"PortAudio Error starting stream: {pae}")
             print("Please ensure audio output device is available and PortAudio is installed correctly.")
             self._running = False
        except Exception as e:
            print(f"Fatal error in audio thread: {e}")
            import traceback
            traceback.print_exc()
            self._running = False
        finally:
            print("Audio stream processing loop finished.")
            # Clean closing is handled by the 'with self._stream:' block exiting or stop()


    def update_parameters(self, params: Dict[str, Any]):
        """Request an update to the audio generation parameters (thread-safe)."""
        if self._is_disabled: return
        # Simple put to queue, callback will process
        self._parameter_queue.put(params)


    def start(self):
        """Starts the audio generation thread and stream."""
        if self._is_disabled:
             print("Cannot start AudioEngine: Dependencies missing.")
             return
        if self._running:
            print("Audio engine already running.")
            return

        try:
            sd.check_output_settings(samplerate=self.sample_rate, channels=1, dtype='float32')
            print("Audio output settings check passed.")
        except Exception as e:
             print(f"Audio output settings check FAILED: {e}")
             print("Audio might not work correctly. Ensure correct device selected and functional.")
             # Optional: Prevent starting? Let's still try for now.

        self._running = True
        # Re-initialize time tracking on fresh start
        preset = MOOD_PRESETS.get(self._target_params['mood'], MOOD_PRESETS['default'])
        self._initialize_oscillator_times(len(preset))

        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print("Audio engine thread start requested.")


    def stop(self):
        """Stops the audio generation thread and stream."""
        if self._is_disabled: return
        if not self._running:
            # print("Audio engine not running or already stopped.")
            return

        print("Stopping audio engine...")
        self._running = False # Signal the thread loop to stop

        # Attempt to close the stream directly if open
        # The callback will stop being called once stream is closed/aborted
        if self._stream:
            try:
                 print("Closing audio stream...")
                 # Close blocks until buffers are finished, Abort stops immediately
                 self._stream.abort(ignore_errors=True) # Use abort for quicker shutdown
                 self._stream.close(ignore_errors=True)
                 print("Audio stream closed.")
            except Exception as ce:
                 print(f"Error closing audio stream during stop: {ce}")
            finally:
                 self._stream = None

        # Wait for the thread to finish
        if self._thread is not None and self._thread.is_alive():
            try:
                 # print("Waiting for audio thread to join...")
                 self._thread.join(timeout=1.0) # Wait up to 1 second
                 if self._thread.is_alive():
                     print("Warning: Audio thread did not stop cleanly after 1 second.")
            except Exception as e:
                print(f"Error joining audio thread: {e}")

        self._thread = None
        print("Audio engine stopped.")


print("[engine.py] Modified for time continuity.")