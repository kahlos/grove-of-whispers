# grove/core/action_handler.py
# Handles processing mindful actions and interactions.

import random
from typing import Dict, Optional, Any

# Project imports
from .game_state import GameState
from ..content.locations import locations # Read-only access needed
from ..content.dynamics import (
    generate_dynamic_text, select_random_outcome, _get_random_from_pool
)
from ..presentation.display import display_action_text, display_message
from ..utils.text_utils import wrap_text # For potential error messages

def handle_action(command: str, game_state: GameState) -> bool:
    """
    Processes a non-movement action command.
    Returns True if the action was found and processed, False otherwise.
    """
    location_id = game_state.current_location_id
    location_data = locations.get(location_id)

    if not location_data:
        print(f"Error: Data missing for current location '{location_id}' during action.")
        return False # Cannot find actions

    available_actions = location_data.get('actions', {})

    if command in available_actions:
        action_data = available_actions[command]

        # --- Generate and display action text ---
        action_text_template = action_data.get('text', "You do that.")
        action_pools = action_data.get('description_pools', {})
        final_action_text = generate_dynamic_text(action_text_template, action_pools)
        display_action_text(final_action_text) # Display using presentation layer

        # --- Determine Outcome (Message and Reveal) ---
        final_message: Optional[str] = None
        reveals_for_this_action: Optional[Dict[str, str]] = None
        reveal_chance = action_data.get('reveal_chance', 1.0) # Default 100%

        if 'possible_reveals' in action_data:
            chosen_outcome = select_random_outcome(action_data['possible_reveals'])
            if chosen_outcome:
                # Allow messages within outcomes to be pool refs or strings
                message_ref = chosen_outcome.get('message')
                if message_ref:
                     # Use internal helper directly here or via dynamics.py function
                     final_message = _get_random_from_pool(message_ref, "action_msg")

                potential_reveal = chosen_outcome.get('reveal')
                # Apply reveal only if present and chance allows
                if potential_reveal and random.random() < reveal_chance:
                    reveals_for_this_action = potential_reveal

        elif 'possible_messages' in action_data:
            # Allow messages to be pool refs or lists of strings
            final_message = _get_random_from_pool(action_data['possible_messages'], "action_msg")
            # Check for static reveal alongside dynamic message
            potential_reveal = action_data.get('reveal')
            if potential_reveal and random.random() < reveal_chance:
                reveals_for_this_action = potential_reveal
        else:
            # Fallback to static message and reveal
            final_message = action_data.get('message')
            potential_reveal = action_data.get('reveal')
            if potential_reveal and random.random() < reveal_chance:
                reveals_for_this_action = potential_reveal

        # --- Display Message (using presentation layer) ---
        if final_message and final_message != "<action_msg?#>": # Don't display error placeholder
             # Convert to string just in case pool returns non-string accidentally
             if not isinstance(final_message, str): final_message = str(final_message)
             display_message(final_message, slow=True) # Use slower display for insightful messages

        # --- Apply Reveals to Game State ---
        if reveals_for_this_action:
             # We expect reveals_for_this_action to be like {'w': 'some_loc'}
             if isinstance(reveals_for_this_action, dict):
                 for rev_cmd, rev_dest in reveals_for_this_action.items():
                     if isinstance(rev_cmd, str) and isinstance(rev_dest, str):
                          game_state.add_revealed_exit(rev_cmd, rev_dest)
                     else:
                          print(f"[DEBUG] Invalid reveal format in action '{command}': {reveals_for_this_action}")
             else:
                 print(f"[DEBUG] Invalid reveal data type for action '{command}': {type(reveals_for_this_action)}")


        # --- Placeholder for state changes ---
        # if 'state_change_func' in action_data:
        #     state_change_func = action_data['state_change_func'] # Needs function references/names
        #     state_change_func(game_state)

        return True # Action found and processed

    else:
        # Command was not found in the available actions for this location
        return False # Action not found


print("[action_handler.py] Loaded.")