#!/usr/bin/env python3
# grove_of_whispers.py
# Main entry point for The Grove of Whispers. Handles args and runs game loop.

# Standard library imports
import sys
import traceback
import time # Keep time import for shutdown safety if needed
import argparse # <<< Added for command-line arguments

# Local package imports
try:
    from grove.core.game_loop import run_game
    from grove.core.game_state import GameState, load_initial_state
    from grove.presentation.intro import introduction
    from grove.audio.engine import AudioEngine
    from grove import config # <<< Added config import
except ImportError as e:
    print("Critical Error: Failed to import required game components.")
    print(f"Ensure all package directories (__init__.py) and files exist.")
    print(f"Import error details: {e}")
    sys.exit(1)

def main():
    """Parses arguments, initializes, and runs the game."""
    # --- Argument Parsing ---
    parser = argparse.ArgumentParser(description="The Grove of Whispers - A Text-Based Mindfulness Adventure")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output messages.")
    args = parser.parse_args()

    # --- Set Global Debug Config ---
    config.DEBUG = args.debug
    if config.DEBUG:
        print("--- DEBUG MODE ENABLED ---")

    # --- Initialization ---
    game_state: Optional[GameState] = None
    audio_engine: Optional[AudioEngine] = None

    try:
        # Initialize Audio Engine (Only create if not disabled internally)
        if hasattr(AudioEngine, '__init__') and not getattr(AudioEngine(0), '_is_disabled', True): # Check if not disabled
            print("Initializing audio engine...")
            audio_engine = AudioEngine()
            audio_engine.start()
            # time.sleep(0.5) # Less necessary now shutdown is better? Keep for safety.
        else:
            print("Audio is disabled (check dependencies or engine code).")

        # Display Introduction
        introduction()

        # Load Game State
        game_state = load_initial_state()
        if not game_state:
            print("Error: Could not load initial game state.")
            # Cleanly stop audio if it started
            if audio_engine and audio_engine._running:
                 audio_engine.stop()
            return

        # --- Run Game ---
        run_game(game_state, audio_engine)

    except KeyboardInterrupt:
        print("\n\nInterrupted journey. May you find peace.")
    except Exception as e:
        print("\n\n" + "="*20 + " An Unexpected Error Occurred " + "="*20)
        if game_state: print(f"Last known Location ID: {game_state.current_location_id}")
        else: print("Error occurred before game state was fully initialized.")
        print(f"Error Type: {type(e).__name__}"); print(f"Error Details: {e}")
        print("\nTraceback:"); traceback.print_exc()
        print("\n" + "="*60)
        print("The Grove fades... please report this error if possible.")

    finally:
        # --- Clean Shutdown ---
        if audio_engine and getattr(audio_engine, '_running', False): # Check if running
            print("Shutting down audio engine...")
            audio_engine.stop() # Call the corrected stop method
        # else: print("Audio engine not active or already stopped.") # Reduce noise

        print("\nGame ended.")

if __name__ == "__main__":
    main()