# grove/core/action_handler.py
# v2: Uses conditional_sleep, adds debug prints.

import random
# import time # Not needed directly
from typing import Dict, Optional, Any

# Project imports
from .game_state import GameState
from ..content.locations import locations
from ..content.dynamics import generate_dynamic_text, select_random_outcome, _get_random_from_pool
# Updated presentation layer imports for direct calls if needed (display_message IS used)
from ..presentation.display import display_action_text, display_message
from ..utils.text_utils import wrap_text, conditional_sleep # Import conditional_sleep
from .. import config # Import config

def handle_action(command: str, game_state: GameState) -> bool:
    """
    Processes a non-movement action. Returns True if handled.
    Delays handled by display functions checking config.DEBUG.
    """
    location_id = game_state.current_location_id
    location_data = locations.get(location_id)
    if not location_data: print(f"Error: Data missing for '{location_id}' during action."); return False

    available_actions = location_data.get('actions', {})
    if command in available_actions:
        action_data = available_actions[command]
        # *** Debug Print Start Action ***
        if config.DEBUG: print(f"[DEBUG Action] Attempting action '{command}' in '{location_id}'")

        # Generate and display action text (uses debug-aware slow_print via display_action_text)
        action_text_template = action_data.get('text', "You do that.")
        action_pools = action_data.get('description_pools', {})
        final_action_text = generate_dynamic_text(action_text_template, action_pools)
        display_action_text(final_action_text)

        # Determine Outcome (Message/Reveal - logic same as before)
        final_message: Optional[str] = None; reveals_for_this_action: Optional[Dict[str, str]] = None
        reveal_chance = action_data.get('reveal_chance', 1.0)
        if 'possible_reveals' in action_data:
            chosen_outcome = select_random_outcome(action_data['possible_reveals'])
            if chosen_outcome:
                 message_ref = chosen_outcome.get('message'); final_message = _get_random_from_pool(message_ref, "action_msg")
                 potential_reveal = chosen_outcome.get('reveal');
                 if potential_reveal and random.random() < reveal_chance: reveals_for_this_action = potential_reveal
        elif 'possible_messages' in action_data:
             message_ref = action_data['possible_messages']; final_message = _get_random_from_pool(message_ref, "action_msg")
             potential_reveal = action_data.get('reveal');
             if potential_reveal and random.random() < reveal_chance: reveals_for_this_action = potential_reveal
        else:
             final_message = action_data.get('message')
             potential_reveal = action_data.get('reveal');
             if potential_reveal and random.random() < reveal_chance: reveals_for_this_action = potential_reveal
        if isinstance(final_message, list): final_message = random.choice(final_message) if final_message else None # Ensure string
        elif not isinstance(final_message, (str, type(None))): final_message = str(final_message)

        # Display Message (uses debug-aware delays via display_message)
        if final_message and final_message != "<action_msg?#>":
             display_message(final_message, slow=True) # Insightful messages are slow printed

        # Apply Reveals
        if reveals_for_this_action:
            if isinstance(reveals_for_this_action, dict):
                 # *** Debug Print for Reveals ***
                 if config.DEBUG: print(f"[DEBUG Action] Revealing exits: {reveals_for_this_action}")
                 for rev_cmd, rev_dest in reveals_for_this_action.items():
                     if isinstance(rev_cmd, str) and isinstance(rev_dest, str): game_state.add_revealed_exit(rev_cmd, rev_dest)
                     else: print(f"[WARN] Invalid reveal format in action '{command}': ({rev_cmd}, {rev_dest})")
            else: print(f"[WARN] Invalid reveal data type for action '{command}': {type(reveals_for_this_action)}")

        # State Changes (Placeholder)
        # if action_data.get('state_change'): action_data['state_change'](game_state)
        return True # Action handled
    else:
        return False # Action not found for this command


print("[action_handler.py] v2 Loaded (conditional sleeps, debug info).")