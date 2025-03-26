#!/usr/bin/env python3
# main.py / grove_of_whispers.py
# Main entry point for The Grove of Whispers.

# Standard library imports
import sys
import traceback
from typing import Optional # For type hinting

# Local package imports
try:
    # Explicitly add project root to sys.path if running script directly
    # and imports fail. Usually better to run as a module (python -m grove...)
    # or install the package. For simplicity now, this might help.
    # import os
    # project_root = os.path.dirname(os.path.abspath(__file__))
    # sys.path.insert(0, project_root)

    from grove.core.game_loop import run_game
    from grove.core.game_state import GameState, load_initial_state
    from grove.presentation.intro import introduction
except ImportError as e:
    print("Critical Error: Failed to import required game components.")
    print(f"Ensure all package directories (__init__.py) and files exist.")
    print(f"Import error details: {e}")
    # Print traceback to see where the import failed
    # traceback.print_exc() # Uncomment for more detailed debug
    sys.exit(1) # Can't run without imports

def main():
    """Initializes and runs the game."""
    game_state: Optional[GameState] = None # Initialize for error scope
    try:
        # Display the introduction sequence
        introduction()

        # Load the initial state (e.g., starting location)
        game_state = load_initial_state()
        if not game_state:
            print("Error: Could not load initial game state.")
            return # Exit if state loading fails

        # Start the main game loop
        run_game(game_state)

    except KeyboardInterrupt:
        print("\n\nInterrupted journey. May you find peace.")
    except Exception as e:
        print("\n\n" + "="*20 + " An Unexpected Error Occurred " + "="*20)
        if game_state:
             print(f"Last known Location ID: {game_state.current_location_id}")
        else:
            print("Error occurred before game state was fully initialized.")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {e}")
        print("\nTraceback:")
        traceback.print_exc()
        print("\n" + "="*60)
        print("The Grove fades... please report this error if possible.")

    finally:
        # Code here runs whether loop finishes normally, breaks, or errors
        print("\nGame ended.")

if __name__ == "__main__":
    main()