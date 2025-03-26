# grove/core/game_state.py
# Defines the GameState class to hold all mutable game information.

from typing import Dict, Set, Optional

class GameState:
    """Holds the current mutable state of the game."""
    def __init__(self, start_location_id: str):
        self.current_location_id: str = start_location_id
        # Stores exits revealed by actions while in the current location
        self.revealed_exits_this_turn: Dict[str, str] = {}
        self.game_active: bool = True

        # --- Future State Variables ---
        # self.player_calm: int = 0
        # self.player_insights: Set[str] = set()
        # self.inventory: List[str] = []

    def add_revealed_exit(self, command: str, destination_id: str):
        """Adds a temporarily revealed exit for the current location."""
        self.revealed_exits_this_turn[command.lower()] = destination_id

    def clear_revealed_exits(self):
        """Clears revealed exits, typically called upon moving."""
        self.revealed_exits_this_turn = {}

    def set_location(self, location_id: str):
        """Updates the current location and clears revealed exits."""
        self.current_location_id = location_id
        self.clear_revealed_exits()
        # Potentially add validation here later to ensure location_id exists

    def quit_game(self):
        """Sets the flag to end the game loop."""
        self.game_active = False

# --- Initialization ---
def load_initial_state() -> Optional[GameState]:
    """Creates the initial game state."""
    # Potentially load from save file later
    try:
        # Basic check: does 'clearing' exist before creating state?
        from ..content.locations import locations
        if 'clearing' not in locations:
             print("ERROR: Initial state requires 'clearing' location, not found!")
             return None
        return GameState(start_location_id='clearing')
    except Exception as e:
        print(f"Error creating initial game state: {e}")
        return None


print("[game_state.py] Loaded.")