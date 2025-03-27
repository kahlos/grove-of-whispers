# grove/presentation/display.py
# v2: Updated to use location_visuals from visuals.py

import random
import time
from typing import Dict, Set, Optional, List

# Project imports
from ..core.game_state import GameState
# Import LOCATIONS for description templates and pools
from ..content.locations import locations
# Import VISUALS dictionary separately
try:
    from ..content.visuals import location_visuals
except ImportError:
    print("[WARN] Could not import location_visuals from visuals.py. No visuals will be shown.")
    location_visuals = {} # Define as empty dict to avoid errors
# Other content/utils
from ..content.dynamics import generate_dynamic_text, generate_event_text
from ..utils.text_utils import wrap_text, slow_print


def display_location(game_state: GameState):
    """Generates and displays the description, visual (from visuals.py), and events."""
    location_id = game_state.current_location_id
    location_data = locations.get(location_id) # Get data for descriptions/pools etc

    if not location_data:
        print(wrap_text(f"Critical Error: Location data missing for ID: '{location_id}'!"))
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

    print(wrap_text(final_description)) # Print descriptive text

    # --- Display Visual (from imported dictionary) ---
    # Lookup visual based on location_id in the separate visual data
    visual = location_visuals.get(location_id) # Use .get for safety
    if visual and isinstance(visual, str) and visual.strip():
        print("")
        print(visual) # Assumes visual string has correct newlines
        print("")
        time.sleep(0.3)

    # --- Flavor Event Trigger ---
    event_text = generate_event_text(location_data) # Uses location_data for event_chance etc.
    if event_text:
        time.sleep(random.uniform(0.8, 1.5))
        print(wrap_text(f"\nSuddenly: {event_text}"))
        time.sleep(random.uniform(1.0, 1.8))


# display_prompt remains the same
def display_prompt(game_state: GameState) -> Set[str]:
    valid_commands: Set[str] = set()
    location_id = game_state.current_location_id
    location_data = locations.get(location_id)
    if not location_data:
        print("[Error prompt: No location data]"); valid_commands.add("quit"); print("\n[Quit]"); return valid_commands

    available_options: List[str] = []
    all_exits = location_data.get('exits', {}).copy(); all_exits.update(game_state.revealed_exits_this_turn)
    if all_exits:
        exit_parts = []
        sorted_exits = sorted(all_exits.keys(), key=lambda x: {'n':0,'s':1,'e':2,'w':3,'u':4,'d':5}.get(x.lower(), 100))
        for command in sorted_exits:
            hint = {'n':'North','s':'South','e':'East','w':'West','u':'Up','d':'Down'}.get(command.lower())
            display_command = command.upper()
            exit_parts.append(f"[{display_command}] {hint}" if hint else f"[{display_command}]")
            valid_commands.add(command.lower())
        if exit_parts: available_options.append("Exits: " + ", ".join(exit_parts))

    actions = location_data.get('actions', {})
    if actions:
        action_parts = []
        sorted_actions = sorted(actions.keys())
        for command in sorted_actions:
            display = command.upper() if len(command) == 1 else command.capitalize()
            action_parts.append(f"[{display}]")
            valid_commands.add(command.lower())
        if action_parts: available_options.append("Actions: " + ", ".join(action_parts))

    available_options.append("[Quit]"); valid_commands.add("quit")
    print("\n" + "\n".join(available_options))
    return valid_commands

# display_message and display_action_text remain the same
def display_message(message: str, slow: bool = False, delay_min: float = 0.8, delay_max: float = 1.4):
     if slow: slow_print(f"-- {message} --", delay_min=delay_min, delay_max=delay_max)
     else: print(wrap_text(f"-- {message} --")); time.sleep(random.uniform(delay_min, delay_max * 0.8))

def display_action_text(text: str):
    print(""); slow_print(text, delay_min=1.2, delay_max=2.0)


print("[display.py] v2 Updated to import visuals.")