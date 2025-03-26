# grove/audio/engine.py
# Manages audio stream, generation parameters, and background playback thread.

import threading
import time
import random
from queue import Queue, Empty
from typing import Optional, Dict, List, Any

try:
    import sounddevice as sd
except ImportError:
    print("\n--- ERROR ---")
    print("Failed to import 'sounddevice'.")
    print("Please install it: pip install sounddevice")
    print("You may also need system libraries like PortAudio (e.g., 'sudo apt-get install libportaudio2' on Debian/Ubuntu).")
    print("-------------\n")
    sd = None # Signal missing dependency

try:
    import numpy as np
except ImportError:
    print("\n--- ERROR ---")
    print("Failed to import 'numpy'.")
    print("Please install it: pip install numpy (or use requirements.txt)")
    print("-------------\n")
    # Provide dummy class/function if needed to prevent load failures later
    np = None # Signal that numpy is missing

# Local imports
try:
    from .synth import generate_drone, generate_lfo
except ImportError:
    print("Error importing synth functions in engine.py")
    # Define dummies only if really needed and if synth itself didn't fail first
    if np: # Only define dummies if numpy at least loaded
        def generate_drone(*args, **kwargs): return np.zeros(1024, dtype=np.float32)
        def generate_lfo(*args, **kwargs): return np.ones(1024, dtype=np.float32) * 0.5
    else: # If numpy also failed, make them return None
        def generate_drone(*args, **kwargs): return None
        def generate_lfo(*args, **kwargs): return None

# --- Constants ---
DEFAULT_SAMPLE_RATE = 44100
BUFFER_DURATION = 0.2 # seconds - smaller = more responsive, larger = more stable
MIN_BASE_FREQ = 50 # Hz
MAX_BASE_FREQ = 120 # Hz

# --- Mood Definitions (Frequencies relative to base) ---
# Structure: mood_name: [(freq_multiplier, base_amp, lfo_rate, lfo_depth), ...]
# Freq Multiplier: e.g., 1=root, 1.5=fifth, 2=octave
MOOD_PRESETS: Dict[str, List[tuple[float, float, float, float]]] = {
    "clearing_calm": [
        (1.0, 0.4, 0.1, 0.15),  # Root drone, slow gentle pulse
        (1.5, 0.2, 0.15, 0.1), # Fifth, slightly faster pulse
        (2.0, 0.15, 0.08, 0.1),# Octave, very slow pulse
        (3.0, 0.05, 0.3, 0.04),# Higher harmonic shimmer
    ],
    "forest_neutral": [
        (1.0, 0.35, 0.12, 0.1), # Root
        (1.498, 0.18, 0.2, 0.1), # Slightly flat fifth (just intonation feel?)
        (2.5, 0.1, 0.25, 0.08),# Different harmonic interval
    ],
    "forest_mysterious": [
        (1.0, 0.3, 0.1, 0.1),   # Root
        (1.333, 0.2, 0.18, 0.1),# Perfect Fourth
        (1.78, 0.15, 0.22, 0.08), # ~Minor Sixth harmonic area
        (4.0, 0.04, 0.4, 0.03), # High distant octave x2 shimmer
    ],
    "woods_deep": [
        (1.0, 0.4, 0.08, 0.05), # Low Root, very slow pulse
        (1.189, 0.2, 0.15, 0.1),# ~Augmented unison/minor second area (dissonance)
        (1.682, 0.1, 0.2, 0.08), # ~Tritone area
    ],
    "stream": [
        (1.0, 0.25, 0.2, 0.15), # Root
        (2.0, 0.20, 0.25, 0.15),# Octave, slight faster shimmer
        (2.5, 0.15, 0.3, 0.1), # Ninth harmonic shimmer
        (3.5, 0.10, 0.4, 0.08),# Higher shimmer
    ],
    "default": [ # Fallback
        (1.0, 0.3, 0.1, 0.1),
        (1.5, 0.15, 0.15, 0.08),
    ]
}

class AudioEngine:
    """Manages dynamic audio generation and playback in a separate thread."""

    def __init__(self, sample_rate: int = DEFAULT_SAMPLE_RATE):
        self.sample_rate = sample_rate
        self.buffer_size = int(BUFFER_DURATION * self.sample_rate)
        self._stream: Optional[sd.OutputStream] = None
        self._thread: Optional[threading.Thread] = None
        self._running: bool = False
        self._parameter_queue: Queue = Queue(maxsize=1) # Queue for thread-safe updates

        # Default parameters
        self._current_params: Dict[str, Any] = {
            'base_freq': 65.41, # C2
            'mood': 'default',
            'master_volume': 0.6 # Overall volume control
        }
        self._target_params: Dict[str, Any] = self._current_params.copy()

    def _audio_callback(self, outdata: np.ndarray, frames: int, time_info, status):
        """Called by sounddevice to fill the output buffer."""
        if not np: # Check dependencies at start of critical function
             outdata.fill(0); return
        
        if status:
            print(f"Audio Status Warning: {status}", flush=True)

        try:
            # --- Smooth parameter transitions ---
            # Very simple interpolation (can be improved with proper smoothing)
            interp_factor = 0.05 # Smaller = slower transition
            current_base = self._current_params['base_freq']
            target_base = self._target_params['base_freq']
            self._current_params['base_freq'] += (target_base - current_base) * interp_factor
            # Update mood directly for now (can also interpolate preset values)
            self._current_params['mood'] = self._target_params['mood']
            self._current_params['master_volume'] = self._target_params['master_volume']


            # --- Get preset for current mood ---
            mood = self._current_params['mood']
            preset = MOOD_PRESETS.get(mood, MOOD_PRESETS['default'])
            num_oscillators = len(preset)

            # --- Prepare oscillator parameters ---
            frequencies = []
            target_amplitudes = []
            lfo_rates = []
            lfo_depths = []
            base_freq = self._current_params['base_freq']

            for freq_mult, base_amp, lfo_rate, lfo_depth in preset:
                 frequencies.append(base_freq * freq_mult)
                 target_amplitudes.append(base_amp)
                 lfo_rates.append(lfo_rate)
                 lfo_depths.append(lfo_depth)

            # --- Generate LFOs for amplitude modulation ---
            amplitude_modulators = []
            for i in range(num_oscillators):
                 lfo = generate_lfo(lfo_rates[i], BUFFER_DURATION, self.sample_rate, lfo_depths[i], offset=1.0 - lfo_depths[i])
                 if lfo is None: lfo = np.ones(self.buffer_size, dtype=np.float32) # Fallback: no modulation
                 amplitude_modulators.append(lfo)

            # --- Calculate final amplitudes for this buffer ---
            current_amplitudes = [target_amplitudes[i] * amplitude_modulators[i] for i in range(num_oscillators)]

            # --- Generate the drone audio data ---
            drone_wave = generate_drone(frequencies, current_amplitudes, BUFFER_DURATION, self.sample_rate)

            if drone_wave is not None:
                # Apply master volume
                final_wave = drone_wave * self._current_params['master_volume']

                # Ensure shape matches outdata (frames, channels)
                # Assuming mono for now, broadcast if needed for stereo
                if final_wave.shape[0] != frames:
                     # Basic handling if frame count doesn't match buffer size estimate
                     if final_wave.shape[0] > frames:
                         final_wave = final_wave[:frames]
                     else: # Pad with silence if too short
                         padding = np.zeros(frames - final_wave.shape[0], dtype=np.float32)
                         final_wave = np.concatenate((final_wave, padding))

                outdata[:] = final_wave.reshape(-1, 1) # Reshape for (frames, 1 channel)
            else:
                outdata.fill(0) # Fill with silence on error

        except Exception as e:
            print(f"Error in audio callback: {e}", flush=True)
            import traceback
            traceback.print_exc() # Print detailed traceback
            outdata.fill(0) # Output silence if anything goes wrong
        pass

    def _run(self):
        """The main loop for the audio thread."""
        if not sd or not np: # Check dependencies before trying to start stream
             print("Cannot start audio thread: Missing dependencies (sounddevice or numpy).")
             self._running = False
             return
        try:
            self._stream = sd.OutputStream(
                samplerate=self.sample_rate,
                blocksize=self.buffer_size,
                channels=1, # Mono output
                dtype='float32',
                callback=self._audio_callback
            )
            with self._stream:
                print(f"Audio stream started (Sample Rate: {self.sample_rate}, Buffer Size: {self.buffer_size})")
                while self._running:
                    # Check queue for parameter updates non-blockingly
                    try:
                        new_params = self._parameter_queue.get_nowait()
                        # Update the target parameters smoothly
                        self._target_params.update(new_params)
                        self._parameter_queue.task_done() # Mark task as done
                    except Empty:
                        pass # No update request, continue processing
                    except Exception as qe:
                        print(f"Error processing parameter queue: {qe}")

                    time.sleep(BUFFER_DURATION / 2) # Sleep briefly, callback drives output

        except sd.PortAudioError as pae:
             print(f"PortAudio Error starting stream: {pae}")
             print("Please ensure audio output device is available and PortAudio (or equivalent) is installed correctly.")
             self._running = False # Stop if stream fails
        except Exception as e:
            print(f"Fatal error in audio thread: {e}")
            import traceback
            traceback.print_exc()
            self._running = False
        finally:
            print("Audio stream stopped.")
            if self._stream and not self._stream.closed:
                try:
                    self._stream.stop()
                    self._stream.close()
                except Exception as ce:
                    print(f"Error closing audio stream: {ce}")
            self._stream = None
        pass


    def update_parameters(self, params: Dict[str, Any]):
        """Request an update to the audio generation parameters (thread-safe)."""
        # Clear previous update requests if queue is full and add new one
        while not self._parameter_queue.empty():
             try: self._parameter_queue.get_nowait()
             except Empty: break
             self._parameter_queue.task_done() # Need to mark as done even if discarding
        self._parameter_queue.put(params) # Add the latest parameters


    def start(self):
        """Starts the audio generation thread and stream."""
        if not sd or not np: # Check before trying to check settings/start
             print("Cannot start audio engine: Missing dependencies.")
             return
        if self._running:
            print("Audio engine already running.")
            return
        try:
            sd.check_output_settings(samplerate=self.sample_rate, channels=1, dtype='float32')
            print("Audio output settings check passed.")
        except Exception as e:
             print(f"Audio output settings check FAILED: {e}")
             print("Audio might not work correctly. Try different sample rate or check device.")
             # Optionally, could prevent starting here, but let's try anyway.

        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True) # Daemon=True allows main program to exit
        self._thread.start()
        print("Audio engine thread started.")
        pass


    def stop(self):
        """Stops the audio generation thread and stream."""
        if not self._running:
            print("Audio engine not running.")
            return

        print("Stopping audio engine...")
        self._running = False # Signal the thread to stop
        if self._thread is not None:
            try:
                # Wait a short time for the thread to finish cleanly
                 self._thread.join(timeout=BUFFER_DURATION * 3)
                 if self._thread.is_alive():
                     print("Audio thread did not stop gracefully.")
                     # Force closing the stream might be needed here if thread is stuck
                     if self._stream: self._stream.abort(ignore_errors=True)
            except Exception as e:
                print(f"Error joining audio thread: {e}")

        self._thread = None
        print("Audio engine stopped.")
    pass


print("[engine.py] Loaded.")