# grove/core/movement_handler.py
# v2: No sleep on move, debug prints added.

import random
# import time # Replaced with conditional_sleep
from typing import Dict

# Project imports
from .game_state import GameState
from ..content.locations import locations
from ..utils.text_utils import wrap_text, conditional_sleep # Import utility
from .. import config # Import config

def handle_movement(command: str, game_state: GameState) -> bool:
    """
    Attempts movement. Returns True if moved, False otherwise.
    No internal delay unless conditional_sleep is used.
    """
    location_id = game_state.current_location_id
    location_data = locations.get(location_id)
    if not location_data: print(f"Error: Data missing for '{location_id}' during move."); return False

    combined_exits = location_data.get('exits', {}).copy()
    combined_exits.update(game_state.revealed_exits_this_turn)

    if command in combined_exits:
        destination_id = combined_exits[command]

        if destination_id in locations:
            # *** Debug Print before moving ***
            if config.DEBUG: print(f"[DEBUG Move] Moving via '{command.upper()}' from '{location_id}' to '{destination_id}'")
            print(f"\n...") # Keep brief move indicator
            game_state.set_location(destination_id) # Updates loc & clears revealed
            conditional_sleep(0.5, 0.8) # Add SHORT conditional delay for non-debug visual flow
            return True
        else:
            print(wrap_text(f"ERROR: Path '{command.upper()}' leads undefined ('{destination_id}')!"))
            conditional_sleep(1.0) # Give user time to read error, even in debug? Maybe remove.
            return False
    else:
        return False # Command was not a valid exit

print("[movement_handler.py] v2 Loaded (conditional sleep).")