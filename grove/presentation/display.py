# grove/presentation/display.py
# v3: Conditional delays, more debug output.

import random
# import time # Now using conditional_sleep from text_utils
from typing import Dict, Set, Optional, List

# Project imports
from ..core.game_state import GameState
from ..content.locations import locations
try: from ..content.visuals import location_visuals
except ImportError: location_visuals = {}
from ..content.dynamics import generate_dynamic_text, generate_event_text
from ..utils.text_utils import wrap_text, slow_print, conditional_sleep # Import conditional_sleep
from .. import config # Import config

def display_location(game_state: GameState):
    """Generates and displays the description, visual, and events."""
    location_id = game_state.current_location_id
    location_data = locations.get(location_id)

    if not location_data: print(wrap_text(f"Critical Error: Loc data missing ID:'{location_id}'!")); return

    # *** Added Debug Print ***
    if config.DEBUG: print(f"\n--- Displaying Location: [{location_id}] ---")

    # Dynamic Intro
    intro = location_data.get('dynamic_intro')
    if intro and isinstance(intro, list) and intro:
        print(wrap_text(f"\n{random.choice(intro)}"))
        conditional_sleep(0.6, 1.2) # Use conditional sleep

    # Generate Description
    template = location_data.get('description_template', location_data.get('description', "[Desc missing]"))
    pools = location_data.get('description_pools', {})
    final_description = generate_dynamic_text(template, pools)
    print(wrap_text(final_description))

    # Display Visual
    visual = location_visuals.get(location_id)
    if visual and isinstance(visual, str) and visual.strip():
        print("") ; print(visual) ; print("")
        conditional_sleep(0.3) # Use conditional sleep

    # Flavor Event
    event_text = generate_event_text(location_data)
    if event_text:
        conditional_sleep(0.8, 1.5) # Use conditional sleep
        print(wrap_text(f"\nSuddenly: {event_text}"))
        conditional_sleep(1.0, 1.8) # Use conditional sleep


def display_prompt(game_state: GameState) -> Set[str]:
    """Displays available exits and actions, returns valid commands."""
    valid_commands: Set[str] = set()
    location_id = game_state.current_location_id
    location_data = locations.get(location_id)

    if not location_data: print("[Error prompt]"); valid_commands.add("quit"); print("\n[Quit]"); return valid_commands

    available_options: List[str] = []
    # Combined Exits
    all_exits = location_data.get('exits', {}).copy()
    all_exits.update(game_state.revealed_exits_this_turn) # Include revealed
    # *** Debug Print for Revealed Exits ***
    if config.DEBUG and game_state.revealed_exits_this_turn:
        print(f"[DEBUG DisplayPrompt] Revealed this turn: {game_state.revealed_exits_this_turn}")

    if all_exits:
        exit_parts = []
        sorted_exits = sorted(all_exits.keys(), key=lambda x: {'n':0,'s':1,'e':2,'w':3,'u':4,'d':5}.get(x.lower(), 100))
        for command in sorted_exits:
            hint = {'n':'North','s':'South','e':'East','w':'West','u':'Up','d':'Down'}.get(command.lower())
            display = command.upper()
            exit_parts.append(f"[{display}] {hint}" if hint else f"[{display}]")
            valid_commands.add(command.lower())
        if exit_parts: available_options.append("Exits: " + ", ".join(exit_parts))

    # Actions
    actions = location_data.get('actions', {})
    if actions:
        action_parts = []
        sorted_actions = sorted(actions.keys())
        for command in sorted_actions:
            display = command.upper() if len(command) == 1 else command.capitalize()
            action_parts.append(f"[{display}]")
            valid_commands.add(command.lower())
        if action_parts: available_options.append("Actions: " + ", ".join(action_parts))

    # Standard
    available_options.append("[Quit]"); valid_commands.add("quit")
    print("\n" + "\n".join(available_options))

    # *** Debug Print Valid Commands ***
    if config.DEBUG: print(f"[DEBUG DisplayPrompt] Valid cmds: {valid_commands}")
    return valid_commands

def display_message(message: str, slow: bool = False, delay_min: float = 0.8, delay_max: float = 1.4):
     """Displays message. Pauses unless config.DEBUG."""
     if slow: # slow_print handles debug check internally
         slow_print(f"-- {message} --", delay_min=delay_min, delay_max=delay_max)
     else:
         print(wrap_text(f"-- {message} --"))
         conditional_sleep(delay_min * 0.8, delay_max * 0.8) # Use conditional sleep for faster variant

def display_action_text(text: str):
    """Displays action text. Pauses unless config.DEBUG."""
    print("")
    slow_print(text, delay_min=1.2, delay_max=2.0) # slow_print handles debug check


print("[display.py] v3 Loaded (uses conditional sleeps, debug info).")