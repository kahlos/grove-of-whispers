# grove/presentation/display.py
# Functions for displaying game information to the player.

import random
import time
from typing import Dict, Set, Optional, List

# Project imports
from ..core.game_state import GameState
from ..content.locations import locations
from ..content.dynamics import generate_dynamic_text, generate_event_text
from ..utils.text_utils import wrap_text, slow_print


def display_location(game_state: GameState):
    """Generates and displays the description and events for the current location."""
    location_id = game_state.current_location_id
    location_data = locations.get(location_id)

    if not location_data:
        print(wrap_text(f"Critical Error: Location data missing for ID: '{location_id}'! Cannot display."))
        # Perhaps attempt recovery? For now, just print error.
        return

    # --- Dynamic Intro ---
    intro = location_data.get('dynamic_intro')
    if intro and isinstance(intro, list) and intro:
        print(wrap_text(f"\n{random.choice(intro)}"))
        time.sleep(random.uniform(0.6, 1.2))

    # --- Generate Description ---
    template = location_data.get('description_template', location_data.get('description', "[Description missing]"))
    pools = location_data.get('description_pools', {})
    final_description = generate_dynamic_text(template, pools)

    print(wrap_text(final_description))

    # --- Flavor Event Trigger ---
    event_text = generate_event_text(location_data)
    if event_text:
        time.sleep(random.uniform(0.8, 1.5)) # Pause before event
        print(wrap_text(f"\nSuddenly: {event_text}"))
        time.sleep(random.uniform(1.0, 1.8)) # Pause after event


def display_prompt(game_state: GameState) -> Set[str]:
    """Displays available exits and actions, returning the set of valid commands."""
    valid_commands: Set[str] = set()
    location_id = game_state.current_location_id
    location_data = locations.get(location_id)

    if not location_data:
        print("[Error displaying prompt: Location data missing]")
        valid_commands.add("quit")
        print("\n[Quit]")
        return valid_commands

    available_options: List[str] = []

    # --- Combined Exits (Standard + Revealed) ---
    all_exits = location_data.get('exits', {}).copy()
    # Get revealed exits from game state
    all_exits.update(game_state.revealed_exits_this_turn)

    if all_exits:
        exit_parts = []
        sorted_exits = sorted(all_exits.keys(), key=lambda x: {'n':0, 's':1, 'e':2, 'w':3, 'u':4, 'd':5}.get(x.lower(), 100))

        for command in sorted_exits:
            direction_hints = {'n':'North', 's':'South', 'e':'East', 'w':'West', 'u':'Up', 'd':'Down'}
            hint = direction_hints.get(command.lower())
            display_command = command.upper()
            exit_parts.append(f"[{display_command}] {hint}" if hint else f"[{display_command}]")
            valid_commands.add(command.lower())

        if exit_parts:
             available_options.append("Exits: " + ", ".join(exit_parts))

    # --- Actions ---
    actions = location_data.get('actions', {})
    if actions:
        action_parts = []
        sorted_actions = sorted(actions.keys())

        for command in sorted_actions:
            command_display = command.upper() if len(command) == 1 else command.capitalize()
            action_parts.append(f"[{command_display}]")
            valid_commands.add(command.lower()) # Use lowercase for internal matching

        if action_parts:
            available_options.append("Actions: " + ", ".join(action_parts))

    # --- Standard Commands ---
    available_options.append("[Quit]")
    valid_commands.add("quit")
    # Add other standard commands like 'help', 'look' later?

    # Print the combined prompt lines
    print("\n" + "\n".join(available_options))

    return valid_commands

def display_message(message: str, slow: bool = False, delay_min: float = 0.8, delay_max: float = 1.4):
     """Displays a simple message, optionally with slow_print."""
     if slow:
         slow_print(f"-- {message} --", delay_min=delay_min, delay_max=delay_max)
     else:
         print(wrap_text(f"-- {message} --"))
         time.sleep(random.uniform(delay_min, delay_max * 0.8)) # Shorter pause for regular message

def display_action_text(text: str):
    """Displays the descriptive text resulting from an action."""
    print("") # Add a newline before action text
    slow_print(text, delay_min=1.2, delay_max=2.0)


print("[display.py] Loaded.")