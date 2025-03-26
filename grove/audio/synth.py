# grove/audio/synth.py
# Generates basic audio data (numpy arrays) for synthesis, tracking time.

import random
from typing import Optional, Union, List, Tuple

try:
    import numpy as np
except ImportError:
    print("\n--- ERROR ---")
    print("Failed to import 'numpy'.")
    print("Please install it: pip install numpy (or use requirements.txt)")
    print("-------------\n")
    np = None # Signal that numpy is missing

# Type hint for numpy array robust against np possibly being None during import errors
NpArray = Optional['np.ndarray']

def generate_sine_wave(
    frequency: float,
    duration: float,
    sample_rate: int,
    amplitude: Union[float, NpArray] = 0.5,
    start_time: float = 0.0
) -> Tuple[NpArray, float]:
    """
    Generates a single sine wave, optionally modulated, starting from a specific time.

    Args:
        frequency: The frequency of the sine wave in Hz.
        duration: The duration of the wave chunk in seconds.
        sample_rate: The audio sample rate in Hz.
        amplitude: The amplitude (float) or an array for amplitude modulation.
        start_time: The starting time index (phase) for this chunk.

    Returns:
        A tuple containing:
          - The generated wave as a NumPy array.
          - The end time index for the next chunk.
    """
    empty_wave = np.zeros(0, dtype=np.float32) if np else None # Define empty result for np=None case
    if not np: return (empty_wave, start_time)

    num_samples = int(duration * sample_rate)
    end_time = start_time + duration
    placeholder_wave = np.zeros(num_samples, dtype=np.float32) # Default return on error / silence

    # Basic input validation
    if duration <= 0 or sample_rate <= 0:
         return (placeholder_wave, start_time) # Return silence if duration/rate invalid

    # Check amplitude validity and calculate effective amplitude for wave generation
    amplitude_value: Union[float, NpArray] = 0.0 # Initialize
    is_amplitude_array = isinstance(amplitude, np.ndarray)

    if is_amplitude_array:
        if amplitude.shape[0] != num_samples:
             print(f"[Synth Warning] Amplitude array shape mismatch ({amplitude.shape[0]} vs {num_samples}). Using mean.")
             amplitude_value = np.mean(amplitude).astype(np.float32) if amplitude.size > 0 else 0.0
        else:
             amplitude_value = amplitude # Use the array directly
    elif isinstance(amplitude, (int, float)): # Amplitude is scalar
        if amplitude == 0 or frequency == 0:
            # Efficiently return silence if amplitude or frequency is zero
            return (placeholder_wave, end_time)
        amplitude_value = float(amplitude)
    else: # Invalid amplitude type
        print(f"[Synth Warning] Invalid amplitude type: {type(amplitude)}. Using 0.")
        return (placeholder_wave, end_time)


    # Generate time vector starting from start_time
    try:
        t = np.linspace(start_time, end_time, num_samples, endpoint=False, dtype=np.float32)
        # Generate base sine wave (amplitude 1)
        base_wave = np.sin(2 * np.pi * frequency * t)
        # Multiply by the amplitude (scalar or array)
        final_wave = amplitude_value * base_wave

        # Ensure output is float32
        if not np.issubdtype(final_wave.dtype, np.float32):
             final_wave = final_wave.astype(np.float32)

        return (final_wave, end_time)

    except Exception as e:
        print(f"Error generating sine wave (freq={frequency}, start_time={start_time:.2f}): {e}")
        # Return silence on error, but still advance time
        return (placeholder_wave, end_time)

# Removed generate_drone as its logic is moved to the AudioEngine callback
# to manage phase/time continuity per oscillator.

def generate_lfo(
    rate: float,
    duration: float,
    sample_rate: int,
    depth: float = 0.5,
    offset: float = 0.5,
    start_time: float = 0.0
) -> NpArray:
    """Generates a low-frequency sine wave for modulation, also tracking time."""
    placeholder_lfo = np.full(int(duration * sample_rate), offset, dtype=np.float32) if np else None
    if not np: return placeholder_lfo # Return constant offset if numpy failed

    num_samples = int(duration * sample_rate)

    # Basic validation
    if duration <= 0 or sample_rate <= 0:
         return placeholder_lfo

    if rate == 0: # No modulation
        effective_offset = min(offset, 1.0) if depth == 0 else offset
        return np.full(num_samples, effective_offset, dtype=np.float32)

    # LFOs often don't need strict phase continuity, but let's add start_time for consistency
    # The generate_sine_wave below now handles the start_time correctly
    # Depth acts as amplitude here
    # We ignore the returned end_time for the LFO itself, the caller tracks oscillator time
    lfo_wave_chunk, _ = generate_sine_wave(rate, duration, sample_rate, depth, start_time)

    if lfo_wave_chunk is not None:
        lfo_wave = lfo_wave_chunk + offset
        # Optional Clipping: If LFO is meant to stay in 0-1 range, e.g., for amplitude scaling
        # lfo_wave = np.clip(lfo_wave, 0.0, 1.0)
        return lfo_wave.astype(np.float32)
    else:
        # Fallback if sine generation fails, return constant offset
        return np.full(num_samples, offset, dtype=np.float32)

print("[synth.py] Modified for time continuity.")