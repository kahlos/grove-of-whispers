# grove/core/game_loop.py
# v3: More debug prints added.

import random
import time
from typing import Optional, Dict, Any # Added Dict, Any

# Project imports
try: from .. import config
except ImportError: config = type('config', (), {'DEBUG': False})
from .game_state import GameState
from .input_handler import get_player_input, validate_input
from .movement_handler import handle_movement
from .action_handler import handle_action
from ..presentation.display import display_location, display_prompt
from ..utils.text_utils import wrap_text
from ..content.locations import locations
try: from ..audio.engine import AudioEngine
except ImportError: AudioEngine = None


def run_game(game_state: GameState, audio_engine: Optional[AudioEngine] = None):
    """Runs the main game loop until game_state.game_active is False."""
    last_known_mood = 'default'
    if audio_engine:
        initial_location_data = locations.get(game_state.current_location_id, {})
        initial_mood = initial_location_data.get('audio_mood', 'default')
        if config.DEBUG: print(f"[DEBUG] GameLoop: Initial audio mood set to '{initial_mood}'")
        audio_engine.update_parameters({'mood': initial_mood})
        last_known_mood = initial_mood

    turn_counter = 0 # Optional: For debugging specific turns

    # Main Game Loop
    while game_state.game_active:
        turn_counter += 1
        if config.DEBUG: print(f"\n=== Turn {turn_counter} | Location: [{game_state.current_location_id}] ===")

        # 1. Check Audio Mood Update
        current_location_data = locations.get(game_state.current_location_id, {})
        if not current_location_data: # Safety check
            print(f"[ERROR] Cannot find data for current location '{game_state.current_location_id}'! Trying recovery.")
            game_state.set_location('clearing') # Attempt to recover
            continue

        current_mood = current_location_data.get('audio_mood', 'default')
        if current_mood != last_known_mood and audio_engine:
            if config.DEBUG: print(f"[DEBUG] GameLoop: Mood Change -> '{current_mood}'")
            base_freq = 65.41
            if current_mood == 'woods_deep': base_freq = 55.0
            elif current_mood == 'forest_mysterious': base_freq = 61.74
            elif current_mood == 'stream': base_freq = 73.42
            audio_params = {'mood': current_mood, 'base_freq': base_freq}
            audio_engine.update_parameters(audio_params)
            last_known_mood = current_mood

        # 2. Display Location & Prompt
        display_location(game_state)
        valid_commands = display_prompt(game_state)

        # 3. Get Validated Input
        player_command = None
        while not player_command:
            raw_input = get_player_input()
            if raw_input == "quit": game_state.quit_game(); break
            player_command = validate_input(raw_input, valid_commands)
            if player_command and config.DEBUG: print(f"[DEBUG] GameLoop: Processing command '{player_command}'") # Print processed cmd
        if not game_state.game_active: break

        # 4. Process Command
        if not player_command: continue

        processed = handle_movement(player_command, game_state)
        if not processed:
            processed = handle_action(player_command, game_state)

        if not processed and config.DEBUG:
             print(wrap_text(f"[DEBUG] GameLoop: Valid cmd '{player_command}' was NOT handled."))

        if config.DEBUG: print(f"--- End Turn {turn_counter} ---")

    # End of loop


print("[game_loop.py] v3 Loaded with more debug prints.")