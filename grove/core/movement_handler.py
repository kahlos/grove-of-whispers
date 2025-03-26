# grove/core/movement_handler.py
# Handles processing player movement commands.

import random
import time
from typing import Dict

# Project imports
from .game_state import GameState
from ..content.locations import locations # Read-only access needed
from ..utils.text_utils import wrap_text

def handle_movement(command: str, game_state: GameState) -> bool:
    """
    Attempts to move the player based on the command.
    Returns True if movement occurred, False otherwise.
    """
    location_id = game_state.current_location_id
    location_data = locations.get(location_id)

    if not location_data:
        print(f"Error: Data missing for current location '{location_id}' during movement.")
        return False # Cannot determine exits

    # Check standard exits + revealed exits
    combined_exits = location_data.get('exits', {}).copy()
    combined_exits.update(game_state.revealed_exits_this_turn)

    if command in combined_exits:
        destination_id = combined_exits[command]

        # Validate destination exists
        if destination_id in locations:
            print(f"\n...") # Indicate moving
            game_state.set_location(destination_id) # Updates location and clears revealed exits
            time.sleep(random.uniform(1.0, 2.0)) # Travel pause
            return True # Movement successful
        else:
            # Log error if destination doesn't exist in locations data
            print(wrap_text(f"ERROR: The path '{command.upper()}' from '{location_id}' "
                            f"leads to an undefined location ('{destination_id}')! Path ignored."))
            time.sleep(1.5)
            return False # Movement failed (bad data)
    else:
        # This case shouldn't normally be reached if input validation catches non-exit commands
        return False # Command was not a valid exit

print("[movement_handler.py] Loaded.")