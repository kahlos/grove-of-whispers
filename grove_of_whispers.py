# main.py
# Main entry point for The Grove of Whispers. Contains the game loop.

import random
import time
from typing import Dict, Set, Optional # For type hinting

# Import data and logic from other files
try:
    from game_data import locations # We only need locations here, logic functions access pools directly
    from game_logic import (
        introduction, display_location, display_prompt,
        process_action, wrap_text, slow_print
    )
except ImportError as e:
    print("Critical Error: Failed to import required components.")
    print(f"Make sure 'game_data.py' and 'game_logic.py' are in the same directory and contain the necessary definitions.")
    print(f"Import error details: {e}")
    exit() # Can't run without imports

# -----------------------------------------------------------------------------
# Game State Variables
# -----------------------------------------------------------------------------
current_location_id: str = 'clearing' # Start player in the clearing
game_active: bool = True
# Store revealed exits persistently while player is in a location
revealed_exits_this_turn: Dict[str, str] = {}

# --- Potential future state variables ---
# player_state = {'calm': 0, 'insights': set()}

# -----------------------------------------------------------------------------
# Main Game Loop
# -----------------------------------------------------------------------------
if __name__ == "__main__": # Standard Python practice to wrap main execution
    try:
        introduction() # Start with the introduction

        while game_active:
            # --- Display current location and prompt ---
            # Reset revealed exits only when *entering* a location (handled in display_location now?)
            # No, reset needs to be handled per location display *or* per move. Let's do per move.
            current_location_data = locations.get(current_location_id)
            if not current_location_data:
                 print(wrap_text(f"ERROR: Current location '{current_location_id}' is invalid. Returning to start."))
                 current_location_id = 'clearing' # Try to recover
                 revealed_exits_this_turn = {}
                 continue

            display_location(current_location_id, revealed_exits_this_turn)
            valid_commands = display_prompt(current_location_id, revealed_exits_this_turn)

            # --- Get player input ---
            raw_input = input("> ").strip().lower()

            # --- Process Input ---
            if not raw_input:
                print(wrap_text("Silence... what do you choose to do?"))
                time.sleep(1)
                continue

            # --- Quit ---
            if raw_input == "quit":
                print("\nMay you carry the quiet of the Grove with you. Goodbye.")
                game_active = False
                break # Exit the while loop

            # --- Validate Input ---
            if raw_input not in valid_commands:
                potential_matches = [cmd for cmd in valid_commands if isinstance(cmd, str) and cmd.startswith(raw_input)]
                if len(potential_matches) == 1 and len(raw_input) >= 2:
                    print(wrap_text(f"Did you mean '{potential_matches[0].capitalize()}'? Try typing the full command."))
                else:
                    print(wrap_text("That doesn't seem like a valid option right now. Look for choices in [Brackets]."))
                time.sleep(1)
                continue

            # --- Handle Movement ---
            combined_exits = current_location_data.get('exits', {}).copy()
            combined_exits.update(revealed_exits_this_turn)

            if raw_input in combined_exits:
                destination_id = combined_exits[raw_input]
                if destination_id in locations:
                    print(f"\n...") # Indicate moving
                    current_location_id = destination_id
                    revealed_exits_this_turn = {} # *** RESET revealed exits on successful move ***
                    time.sleep(random.uniform(1.0, 2.0))
                else:
                    # Enhanced error message
                    print(wrap_text(f"ERROR: The path '{raw_input.upper()}' from '{current_location_id}' "
                                    f"leads somewhere undefined ('{destination_id}')! Path ignored."))
                    time.sleep(1.5)
                continue # Move processed (or failed), start next turn loop

            # --- Handle Actions ---
            available_actions = current_location_data.get('actions', {})
            if raw_input in available_actions:
                action_results = process_action(available_actions[raw_input])

                # Apply reveals gathered from the action
                if action_results.get('reveal'):
                    revealed_exits_this_turn.update(action_results['reveal'])
                    # print(f"[DEBUG] Revealed exits updated: {revealed_exits_this_turn}") # Optional debug

                # Handle potential state changes (future)
                # if action_results.get('state_change'): process_state_change(...)
                continue # Action processed, start next turn loop (will re-display location with updates)

            # --- Fallback (should ideally not be reached if validation is correct) ---
            if game_active: # Avoid printing if game just quit
                 print(wrap_text("An unexpected error occurred processing your input."))


    except KeyboardInterrupt:
        print("\n\nInterrupted journey. May you find peace.")
    except Exception as e:
        print("\n\n" + "="*20 + " An Unexpected Error Occurred " + "="*20)
        print(f"Location ID: {current_location_id}")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Details: {e}")
        import traceback
        print("\nTraceback:")
        traceback.print_exc()
        print("\n" + "="*60)
        print("The Grove fades... please report this error if possible.")

    finally:
        # Code here runs whether loop finishes normally, breaks, or errors
        print("\nGame ended.")

# --- End of Game ---