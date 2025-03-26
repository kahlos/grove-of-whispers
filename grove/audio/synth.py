# grove/audio/synth.py
# Generates basic audio data (numpy arrays) for synthesis.

import random
from typing import Optional, Union, List

try:
    import numpy as np
except ImportError:
    print("\n--- ERROR ---")
    print("Failed to import 'numpy'.")
    print("Please install it: pip install numpy (or use requirements.txt)")
    print("-------------\n")
    # Provide dummy class/function if needed to prevent load failures later
    np = None # Signal that numpy is missing

# Use string hint for numpy array if np might be None
NpArray = Optional['np.ndarray']

# Modified to accept array for amplitude
def generate_sine_wave(frequency: float, duration: float, sample_rate: int,
                       amplitude: Union[float, NpArray] = 0.5) -> NpArray: # <--- Changed Type Hint
    """Generates a single sine wave, optionally modulated by an amplitude array."""
    if not np: return None

    num_samples = int(duration * sample_rate)

    # Check amplitude: if it's an array, does it match length?
    # Also handle the scalar case where amplitude is zero.
    is_amplitude_array = isinstance(amplitude, np.ndarray)
    if is_amplitude_array:
        if amplitude.shape[0] != num_samples:
             print(f"[Synth Warning] Amplitude array shape mismatch ({amplitude.shape[0]} vs {num_samples}). Using mean.")
             # Fallback: use the average amplitude, or could try resizing/clipping
             amplitude_value = np.mean(amplitude).astype(np.float32)
        else:
             amplitude_value = amplitude # Use the array directly
    else: # Amplitude is scalar
        if amplitude == 0 or frequency == 0:
            return np.zeros(num_samples, dtype=np.float32) # Return silence efficiently
        amplitude_value = float(amplitude) # Ensure it's a float

    # Generate time vector
    try:
        t = np.linspace(0., duration, num_samples, endpoint=False, dtype=np.float32)
        # Generate base sine wave (amplitude 1)
        base_wave = np.sin(2 * np.pi * frequency * t)
        # Multiply by the amplitude (scalar or array)
        final_wave = amplitude_value * base_wave # NumPy handles broadcasting/element-wise multiplication
        return final_wave.astype(np.float32)
    except Exception as e:
        print(f"Error generating sine wave (freq={frequency}): {e}")
        return None
    pass

# Modified to pass amplitude array directly, remove ambiguous check
def generate_drone(frequencies: List[float], amplitudes: List[Union[float, NpArray]], # <--- Changed Type Hint
                   duration: float, sample_rate: int) -> NpArray:
    """Generates multiple overlapping sine waves (a drone), potentially with time-varying amplitudes."""
    if not np: return None
    if not frequencies or len(frequencies) != len(amplitudes):
        print("Error: Mismatched or empty frequencies/amplitudes for drone.")
        return np.zeros(int(duration * sample_rate), dtype=np.float32) # Return silence on error

    num_samples = int(duration * sample_rate)
    final_wave = np.zeros(num_samples, dtype=np.float32)
    count = 0

    for freq, amp in zip(frequencies, amplitudes):
        # --- REMOVED this problematic check: if amp > 0.001 and freq > 0: ---
        # Let generate_sine_wave handle potentially zero/low amplitude or freq
        if freq > 0: # Still makes sense to skip if frequency is zero
            wave = generate_sine_wave(freq, duration, sample_rate, amp) # Pass amp (scalar or array)
            if wave is not None:
                final_wave += wave
                count += 1

    # Normalize if waves were added (might need adjustment if input amps were already low)
    if count > 0:
         max_amp = np.max(np.abs(final_wave))
         # Only normalize if potentially clipping significantly
         if max_amp > 1.0:
            # Consider softer normalization? dividing by max_amp might make quiet sounds too quiet
            # Option: final_wave /= max_amp
            # Option: Soft clipping or compression (more complex)
            # For now, simple normalization:
             final_wave /= max_amp
             #print(f"[DEBUG] Normalizing drone, max amp was {max_amp:.2f}") # Optional Debug


    return final_wave.astype(np.float32)
    pass


# --- Example LFO (Low Frequency Oscillator) for amplitude modulation ---
def generate_lfo(rate: float, duration: float, sample_rate: int, depth: float = 0.5, offset: float = 0.5) -> NpArray:
    """Generates a low-frequency sine wave typically used for modulation."""
    if not np: return None
    num_samples = int(duration * sample_rate)

    if rate == 0: # No modulation
         # Ensure offset doesn't exceed 1.0 if depth is 0
         effective_offset = min(offset, 1.0) if depth == 0 else offset
         return np.full(num_samples, effective_offset, dtype=np.float32)

    amp_mod = generate_sine_wave(rate, duration, sample_rate, depth) # Uses the updated generate_sine_wave
    if amp_mod is not None:
        # Apply offset and ensure the LFO signal usually stays within a reasonable range (e.g., 0 to 1)
        lfo_wave = amp_mod + offset
        # Optional: Clip LFO to prevent extreme values if desired, e.g. np.clip(lfo_wave, 0, 1)
        return lfo_wave.astype(np.float32)
    else:
        # Fallback if sine generation fails
        return np.full(num_samples, offset, dtype=np.float32)
    pass

print("[synth.py] Loaded.")