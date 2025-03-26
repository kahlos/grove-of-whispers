# grove/core/input_handler.py
# Handles getting and validating player input.

from typing import Set, Optional
from ..utils.text_utils import wrap_text
import time

def get_player_input() -> str:
    """Gets input from the player, strips whitespace, and lowercases it."""
    return input("> ").strip().lower()

def validate_input(raw_input: str, valid_commands: Set[str]) -> Optional[str]:
    """Checks if the input is valid. Returns cleaned input or None."""
    if not raw_input:
        print(wrap_text("Silence... what do you choose to do?"))
        time.sleep(1)
        return None # Indicate invalid input (empty)

    if raw_input in valid_commands:
        return raw_input # Input is perfectly valid

    # --- Add potential fuzzy matching or help ---
    # Simple check for partial commands (e.g., 'examine' when 'examine flowers' is valid)
    potential_matches = [cmd for cmd in valid_commands if cmd.startswith(raw_input) and len(raw_input) >= 2]
    if len(potential_matches) == 1:
         print(wrap_text(f"Did you mean '{potential_matches[0].capitalize()}'? Try typing the full command."))
         time.sleep(1)
         return None # Indicate invalid input

    # --- Standard invalid command message ---
    print(wrap_text("That doesn't seem like a valid option right now. Look for choices in [Brackets]."))
    time.sleep(1)
    return None # Indicate invalid input

print("[input_handler.py] Loaded.")