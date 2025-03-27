# grove/audio/generation.py
# Contains audio buffer generation logic, separated from engine state.

from typing import Optional, Dict, List, Any, Tuple

try: import numpy as np
except ImportError: np = None
try: from .synth import generate_sine_wave, generate_lfo
except ImportError: generate_sine_wave = None; generate_lfo = None

# Reference mood presets (read-only) - Needs careful import management
# Avoid circular dependency - engine should pass the relevant preset data.

def generate_audio_chunk_for_preset(
    preset_data: List[Tuple[float, ...]], # The list of tuples for this mood
    base_freq: float,
    osc_times: List[float], # List to read *and update*
    lfo_times: List[float], # List to read *and update*
    frames: int,
    sample_rate: int,
    amplitude_scale_factor: float = 1.0 # For interpolating amplitude during fades
) -> Tuple[Optional[np.ndarray], bool]:
    """
    Generates audio buffer for a given preset snapshot and advances time states.
    Handles potential errors and ensures time states are always advanced.

    Args:
        preset_data: The specific parameters [(freq_mult, base_amp, lfo_rate, lfo_depth), ...]
        base_freq: Current base frequency.
        osc_times: List holding current phase time for each oscillator (modified in-place).
        lfo_times: List holding current phase time for each LFO (modified in-place).
        frames: Number of samples to generate.
        sample_rate: Audio sample rate.
        amplitude_scale_factor: Multiplier for base_amp (used for simple fade interp).

    Returns:
        Tuple (Generated audio buffer or None on failure, success_flag).
    """
    if not np or not generate_sine_wave: return (np.zeros(frames, dtype=np.float32) if np else None, False)

    num_oscillators = len(preset_data)
    buffer_duration_actual = frames / sample_rate

    # **CRITICAL CHECK**: Ensure time arrays match expected length
    if len(osc_times) != num_oscillators or len(lfo_times) != num_oscillators:
        print(f"[ERROR] generate_audio internal mismatch! Need {num_oscillators} states, got Osc:{len(osc_times)}, LFO:{len(lfo_times)}. SILENCE.")
        # We MUST advance the times we *do* have, otherwise they get stuck
        for i in range(len(osc_times)): osc_times[i] += buffer_duration_actual
        for i in range(len(lfo_times)): lfo_times[i] += buffer_duration_actual
        return (np.zeros(frames, dtype=np.float32), False)

    total_wave = np.zeros(frames, dtype=np.float32)
    generation_successful = True
    MAX_LFO_DEPTH_SCALE = 0.95 # Limit LFO depth slightly

    for i in range(num_oscillators):
        osc_successful = True # Flag for this specific oscillator
        try:
            freq_mult, raw_base_amp, lfo_rate, lfo_depth = preset_data[i]

            # Apply overall amplitude scaling factor (for crossfade amplitude interpolation)
            base_amp = raw_base_amp * amplitude_scale_factor

            osc_frequency = base_freq * freq_mult
            osc_start_time = osc_times[i]
            lfo_start_time = lfo_times[i] # Use LFO phase continuity

            # LFO calculation (amplitude modulation for the oscillator)
            safe_lfo_depth = max(0.0, min(1.0, lfo_depth * MAX_LFO_DEPTH_SCALE)) # Clamp 0-1 & scale
            effective_lfo_depth = base_amp * safe_lfo_depth # Modulate relative to current scaled base_amp
            effective_lfo_offset = base_amp * (1.0 - safe_lfo_depth)

            amp_modulator = generate_lfo( max(0.0, lfo_rate), buffer_duration_actual, sample_rate, depth=effective_lfo_depth, offset=effective_lfo_offset, start_time=lfo_start_time)

            # Generate main sine wave
            if amp_modulator is not None and osc_frequency > 0:
                wave_chunk, end_time_osc = generate_sine_wave( osc_frequency, buffer_duration_actual, sample_rate, amplitude=amp_modulator, start_time=osc_start_time )

                if wave_chunk is not None:
                    len_to_add = min(frames, wave_chunk.shape[0])
                    total_wave[:len_to_add] += wave_chunk[:len_to_add]
                    osc_times[i] = end_time_osc # Update osc time state
                else: osc_successful = False; osc_times[i] = osc_start_time + buffer_duration_actual # Still advance time on failure
            else: # LFO failed or freq=0
                osc_successful = False
                osc_times[i] = osc_start_time + buffer_duration_actual # Advance osc time

            # Always advance LFO time state regardless of sine success
            lfo_times[i] = lfo_start_time + buffer_duration_actual

        except IndexError: osc_successful = False; print(f"[ERROR] Gen Index Err @ osc {i}."); break # Exit loop for this buffer
        except Exception as e: osc_successful = False; print(f"[ERROR] Gen Err @ osc {i}: {e}")
        finally: # Ensure generation_successful reflects individual oscillator failure
             if not osc_successful: generation_successful = False

    # Return accumulated wave (even if partially failed) or silence if completely failed
    # The calling function handles deciding whether to use partial result
    # For simplicity now, return silence if any oscillator failed? Or return partial? Return partial.
    # return total_wave, generation_successful
    # Let's be stricter: return silence if *any* failure
    if not generation_successful:
         print("[WARN] Generation incomplete, returning silence for chunk.")
         return (np.zeros(frames, dtype=np.float32), False)

    return total_wave, True

print("[generation.py] Loaded.")