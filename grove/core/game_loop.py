# grove/core/game_loop.py
# Contains the main game loop function.

# Project imports
from .game_state import GameState
from .input_handler import get_player_input, validate_input
from .movement_handler import handle_movement
from .action_handler import handle_action
from ..presentation.display import display_location, display_prompt
from ..utils.text_utils import wrap_text # For potential fallback messages

def run_game(game_state: GameState):
    """Runs the main game loop until game_state.game_active is False."""

    while game_state.game_active:
        # 1. Display current location info
        display_location(game_state)

        # 2. Display available commands (prompt) and get valid ones
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

    # Loop ends when game_state.game_active is False

print("[game_loop.py] Loaded.")