# grove/core/game_loop.py
# v2: Contains main game loop, now checks config.DEBUG.

# Standard library imports
import random
import time
from typing import Optional # Explicitly import Optional

# Project imports
try:
    from .. import config # Import global config
except ImportError:
    class config: DEBUG = False # Dummy config if run standalone
# Core components
from .game_state import GameState
from .input_handler import get_player_input, validate_input
from .movement_handler import handle_movement
from .action_handler import handle_action
# Presentation
from ..presentation.display import display_location, display_prompt
from ..utils.text_utils import wrap_text
# Content (for audio mood lookup)
from ..content.locations import locations
# Audio (Optional)
try:
    from ..audio.engine import AudioEngine
except ImportError:
    AudioEngine = None # Allow running without audio


def run_game(game_state: GameState, audio_engine: Optional[AudioEngine] = None):
    """Runs the main game loop until game_state.game_active is False."""

    last_known_mood = 'default' # Initialize outside conditional block
    if audio_engine:
        # Set initial audio mood
        initial_location_data = locations.get(game_state.current_location_id, {})
        initial_mood = initial_location_data.get('audio_mood', 'default')
        if config.DEBUG: print(f"[DEBUG] Setting initial audio mood to '{initial_mood}'") # Use config flag
        audio_engine.update_parameters({'mood': initial_mood})
        last_known_mood = initial_mood

    # Main Game Loop
    while game_state.game_active:
        # 1. Check Audio Mood Update
        current_location_data = locations.get(game_state.current_location_id, {})
        current_mood = current_location_data.get('audio_mood', 'default')
        if current_mood != last_known_mood and audio_engine:
            # Use config flag for printing
            if config.DEBUG: print(f"[DEBUG] Audio mood changing from '{last_known_mood}' to '{current_mood}'")
            base_freq = 65.41 # Default base
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
            if raw_input == "quit": game_state.quit_game(); break # Quit immediately
            player_command = validate_input(raw_input, valid_commands)
        if not game_state.game_active: break # Exit loop if quit

        # 4. Process Command (Movement then Action)
        if not player_command: continue # Should only happen if loop broke weirdly

        processed = handle_movement(player_command, game_state)
        if not processed:
            processed = handle_action(player_command, game_state)

        # Fallback Debug if command was valid but not processed
        if not processed and config.DEBUG: # Check flag
            print(wrap_text(f"[DEBUG] Valid cmd '{player_command}' was not handled by movement or action."))

    # End of game loop (game_state.game_active is False)


print("[game_loop.py] v2 Loaded with config.DEBUG checks.")