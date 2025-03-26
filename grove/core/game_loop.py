# grove/core/game_loop.py
# Contains the main game loop function.

# Standard library imports
from typing import Optional

# Add AudioEngine import
try:
    from ..audio.engine import AudioEngine
except ImportError:
    print("Warning: AudioEngine could not be imported. Audio will be disabled.")
    AudioEngine = None # Define as None to allow conditional checks

# Project imports
from .game_state import GameState
from .input_handler import get_player_input, validate_input
from .movement_handler import handle_movement
from .action_handler import handle_action
from ..content.locations import locations # Needed to get mood
from ..presentation.display import display_location, display_prompt
from ..utils.text_utils import wrap_text # For potential fallback messages

# --- Define a global or passed-in audio engine instance ---
# This is slightly less clean than managing it within a game class,
# but works for this structure. Be careful with global state.
# Alternatively, pass audio_engine as an argument to run_game.
audio_engine_instance: Optional[AudioEngine] = None

def run_game(game_state: GameState, audio_engine: Optional[AudioEngine] = None): # Pass engine instance
    """Runs the main game loop until game_state.game_active is False."""
    global audio_engine_instance # Access global if not passed
    if audio_engine:
         audio_engine_instance = audio_engine # Use passed instance

    # --- Determine initial mood BEFORE the 'if audio_engine_instance' check ---
    initial_location_data = locations.get(game_state.current_location_id, {})
    initial_mood = initial_location_data.get('audio_mood', 'default') # <<< INITIALIZE HERE
    last_known_mood = initial_mood # Initialize last_known_mood here too

    if audio_engine_instance:
        # Start audio with initial mood
        # Now update parameters if engine exists
        print(f"[DEBUG] Setting initial audio mood to '{initial_mood}'") # Debug message
        audio_engine_instance.update_parameters({'mood': initial_mood})
        # Base frequency could also be set here if needed

    while game_state.game_active:
        # --- Check for Location/Mood Change BEFORE display ---
        current_location_data = locations.get(game_state.current_location_id, {})
        # Use a default if audio_mood key is missing in a location
        current_mood = current_location_data.get('audio_mood', 'default')

        if current_mood != last_known_mood and audio_engine_instance:
            print(f"[DEBUG] Audio mood changing from '{last_known_mood}' to '{current_mood}'")
            # --- Add Parameters Here ---
            # Maybe adjust base frequency slightly based on mood too?
            # Example: lower frequency for 'woods_deep'
            base_freq = 65.41 # Default C2
            if current_mood == 'woods_deep':
                base_freq = 55.0 # A1
            elif current_mood == 'forest_mysterious':
                 base_freq = 61.74 # B1
            elif current_mood == 'stream':
                 base_freq = 73.42 # D2

            audio_params = {'mood': current_mood, 'base_freq': base_freq}
            audio_engine_instance.update_parameters(audio_params)
            last_known_mood = current_mood

        # 1. Display current location info
        display_location(game_state)

        # 2. Display prompt
        valid_commands = display_prompt(game_state)

        # 3. Get validated player input
        player_command = None
        while not player_command: # Loop until valid input is received or game quits
            raw_input = get_player_input()
            # Quit check inside loop for immediate exit
            if raw_input == "quit":
                 game_state.quit_game()
                 break # Exit validation loop

            player_command = validate_input(raw_input, valid_commands)
            # If validate_input returns None, loop continues asking for input

        if not game_state.game_active: # Check if quit happened during input
             break # Exit main game loop

        # 4. Process the valid command
        if not player_command: # Should not happen if loop logic is correct, but safety check
             print("[DEBUG] Loop exited validation without valid command or quit.")
             continue

        processed = False
        # Try movement first
        processed = handle_movement(player_command, game_state)

        # If not movement, try actions
        if not processed:
            processed = handle_action(player_command, game_state)

        # If command wasn't movement or a known action (should be caught by validation)
        if not processed and player_command != "quit":
             # This indicates an issue, maybe a valid command has no handler
             print(wrap_text(f"[DEBUG] Valid command '{player_command}' was not processed by handlers."))

        # Ensure movement/action handlers don't update mood directly,
        # rely on the check at the start of the next loop iteration.

    # Loop ends when game_state.game_active is False
    # Stopping audio is handled in main script's finally block

print("[game_loop.py] Loaded with audio control.")