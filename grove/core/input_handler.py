# grove/core/input_handler.py
# v2: Uses conditional_sleep.

from typing import Set, Optional
from ..utils.text_utils import wrap_text, conditional_sleep # Import utility
# import time # Not needed directly
from .. import config # Import config

def get_player_input() -> str:
    """Gets stripped, lowercased input."""
    return input("> ").strip().lower()

def validate_input(raw_input: str, valid_commands: Set[str]) -> Optional[str]:
    """Validates input. Returns cleaned command or None."""
    if not raw_input:
        print(wrap_text("Silence... what do you choose to do?"))
        conditional_sleep(0.5) # Short pause, even in debug? Maybe remove.
        return None

    if raw_input in valid_commands:
        # *** Debug Print for valid input ***
        if config.DEBUG: print(f"[DEBUG Input] Valid command entered: '{raw_input}'")
        return raw_input

    potential_matches = [cmd for cmd in valid_commands if cmd.startswith(raw_input) and len(raw_input) >= 2]
    if len(potential_matches) == 1:
         print(wrap_text(f"Did you mean '{potential_matches[0].capitalize()}'? Try the full command."))
         conditional_sleep(1.0) # Conditional wait
         return None

    print(wrap_text("That doesn't seem valid now. Use choices in [Brackets]."))
    conditional_sleep(1.0) # Conditional wait
    return None

print("[input_handler.py] v2 Loaded (conditional sleeps).")