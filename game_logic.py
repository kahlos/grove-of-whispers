# game_logic.py
# Contains functions for game mechanics like displaying text, locations, prompts.

import random
import time
import textwrap
from typing import Dict, Set, Any, Optional, List # For type hinting

# Import data from game_data.py
try:
    from game_data import locations, all_data_pools
except ImportError:
    print("Error: Failed to import 'locations' and 'all_data_pools' from game_data.py!")
    print("Make sure game_data.py is in the same directory.")
    # Assign empty dicts to prevent crashes, but the game won't work properly.
    locations = {}
    all_data_pools = {}


# --- Text Formatting and Display ---

def wrap_text(text: str, width: int = 80) -> str:
    """Wraps text for cleaner display."""
    return "\n".join(textwrap.wrap(text, width))

def slow_print(text: str, delay_min: float = 1.5, delay_max: float = 2.5, width: int = 80):
    """Prints text wrapped and with a noticeable pause."""
    print(wrap_text(text, width))
    time.sleep(random.uniform(delay_min, delay_max))


# --- Core Game Functions ---

def introduction():
    """Displays the introductory text and integrated tutorial."""
    print("\n" * 2) # Add some space at the start
    slow_print("...")
    slow_print("Your mind feels... scattered. Like leaves caught in a whirlwind.")
    slow_print("Thoughts race, plans tangle, memories flicker without focus.")
    slow_print("You don't know how you got here, but...")
    slow_print("...here you are.")
    time.sleep(1.0)
    slow_print("Welcome to The Grove of Whispers.", delay_min=1.0, delay_max=1.5)

    print("\n" + "-" * 30 + "\n") # Separator

    slow_print("This place is... different. It seems to respond not just to your steps, but to your attention.", delay_max=2.8)
    slow_print("Moving around is simple. Type commands like 'N', 'S', 'E', 'W' when you see exits listed like [N] North.", delay_max=2.8)
    slow_print("But rushing forward might not always reveal the clearest path.", delay_max=3.0)

    print("\n" + "-" * 30 + "\n")

    slow_print("Sometimes, the Grove invites you to pause. You might see options like:")
    time.sleep(0.5)
    slow_print("`[B] Breathe` - A reminder to take a conscious breath. Try it now, even just one. In... and out. Notice how the Grove responds when you choose this in the game.", delay_max=3.5)
    time.sleep(0.8)
    slow_print("`[L] Listen` - Focus only on the sounds described. What details emerge when you truly pay attention?", delay_max=3.0)
    time.sleep(0.8)
    slow_print("`[F] Feel` - Ground yourself in the sensations of touch described. The texture of moss, the coolness of water, the earth beneath your feet.", delay_max=3.5)
    time.sleep(0.8)
    slow_print("`[S] Sit` or `[Stillness]` - Sometimes, simply being still and observing reveals more than movement.", delay_max=3.0)
    time.sleep(0.8)
    slow_print("Other actions might appear too, like `[Examine Flowers]` or `[Touch Tree]`. Use the text in the brackets as your command. Type it exactly.", delay_max=3.5)

    print("\n" + "-" * 30 + "\n")

    slow_print("There is no 'winning' here in the usual sense. The journey *is* the purpose.", delay_max=3.0)
    slow_print("Pay attention. Be present. See what unfolds.", delay_max=2.5)
    time.sleep(0.5)
    slow_print("If you ever wish to leave the Grove, simply type 'Quit'.")

    print("\n" + "-" * 30 + "\n")
    input("Press Enter when you are ready to begin...")


def display_location(location_id: str, revealed_exits: Dict[str, str]):
    """Gets location data, generates dynamic description, prints it, and triggers events."""
    location = locations.get(location_id)
    if not location:
        print(wrap_text(f"Critical Error: Location data missing for ID: '{location_id}'! Cannot proceed."))
        # In a more robust system, you might try to move the player to a default safe location.
        return # Or raise an exception

    # --- Dynamic Intro ---
    if location.get('dynamic_intro'):
        print(wrap_text(f"\n{random.choice(location['dynamic_intro'])}"))
        time.sleep(random.uniform(0.6, 1.2))

    # --- Description Generation ---
    template = location.get('description_template', location.get('description', "Description is missing."))
    format_dict = {}
    pools_to_use = location.get('description_pools', {})

    # Populate format_dict with random choices from specified pools
    for placeholder, pool_ref in pools_to_use.items():
        chosen_value = _get_random_from_pool(pool_ref, placeholder)
        format_dict[placeholder] = chosen_value

    # Format the template
    try:
        # Use .safe_substitute if using string.Template, or handle KeyError with .format
        final_description = template.format(**format_dict)
    except KeyError as e:
        print(wrap_text(f"[DEBUG: Description template formatting error - Missing key {e}]"))
        final_description = template # Show raw template on error
    except Exception as e:
         print(wrap_text(f"[DEBUG: Unexpected description formatting error: {e}]"))
         final_description = template

    print(wrap_text(final_description))

    # --- Flavor Event Trigger ---
    event_chance = location.get('event_chance', 0)
    if random.random() < event_chance:
        # Default to global event pool if no specific one defined
        event_pool_ref = location.get('possible_events', 'events')
        event_text = _get_random_from_pool(event_pool_ref, "event")
        if event_text and event_text != "<event?>": # Check if we got a valid event
            time.sleep(random.uniform(0.8, 1.5)) # Pause before event
            print(wrap_text(f"\nSuddenly: {event_text}"))
            time.sleep(random.uniform(1.0, 1.8)) # Pause after event


def display_prompt(location_id: str, revealed_exits: Dict[str, str]) -> Set[str]:
    """Displays available exits and actions, returning the set of valid command inputs."""
    valid_inputs: Set[str] = set()
    location = locations.get(location_id)
    if not location:
        print("[Error displaying prompt: Location data missing]")
        valid_inputs.add("quit") # Ensure quit is always possible
        print("\n[Quit]")
        return valid_inputs

    available_options: List[str] = []

    # --- Combined Exits (Standard + Revealed) ---
    all_exits = location.get('exits', {}).copy()
    all_exits.update(revealed_exits) # Add dynamically revealed exits

    if all_exits:
        exit_parts = []
        # Sort for consistent order (N, S, E, W, U, D, others alpha)
        sorted_exits = sorted(all_exits.keys(), key=lambda x: {'n':0, 's':1, 'e':2, 'w':3, 'u':4, 'd':5}.get(x.lower(), 100))

        for command in sorted_exits:
            # No need for destination_id here, just the command
            direction_hints = {'n':'North', 's':'South', 'e':'East', 'w':'West', 'u':'Up', 'd':'Down'}
            hint = direction_hints.get(command.lower())
            display_command = command.upper()

            exit_parts.append(f"[{display_command}] {hint}" if hint else f"[{display_command}]")
            valid_inputs.add(command.lower())

        if exit_parts:
             available_options.append("Exits: " + ", ".join(exit_parts))

    # --- Mindful Actions & Interactions ---
    actions = location.get('actions', {})
    if actions:
        action_parts = []
        # Sort action commands alphabetically for consistency
        sorted_actions = sorted(actions.keys())

        for command in sorted_actions:
            command_display = command.upper() if len(command) == 1 else command.capitalize()
            action_parts.append(f"[{command_display}]")
            valid_inputs.add(command.lower()) # Use lowercase for internal matching

        if action_parts:
            available_options.append("Actions: " + ", ".join(action_parts))

    # Add standard quit command
    available_options.append("[Quit]")
    valid_inputs.add("quit")

    # Print the combined prompt lines
    print("\n" + "\n".join(available_options))

    return valid_inputs


def process_action(action_data: Dict[str, Any]) -> Dict:
    """Processes an action, handles dynamic text/messages/reveals, returns results."""
    results = {'message': None, 'reveal': None}
    action_text_template = action_data.get('text', "You perform the action.")

    # --- Format action text if it contains placeholders ---
    action_format_dict = {}
    action_pools_to_use = action_data.get('description_pools', {})
    for placeholder, pool_ref in action_pools_to_use.items():
        chosen_value = _get_random_from_pool(pool_ref, placeholder)
        action_format_dict[placeholder] = chosen_value

    try:
        final_action_text = action_text_template.format(**action_format_dict)
    except KeyError as e:
        print(wrap_text(f"[DEBUG: Action text formatting error - key {e}]"))
        final_action_text = action_text_template # Show raw template on error
    except Exception as e:
         print(wrap_text(f"[DEBUG: Unexpected action formatting error: {e}]"))
         final_action_text = action_text_template

    # Print action text with a pause
    print("") # Add a newline before action text
    slow_print(final_action_text, delay_min=1.2, delay_max=2.0)

    # --- Handle Dynamic Outcomes ---
    reveal_chance = action_data.get('reveal_chance', 1.0) # Default to 100% if defined

    if 'possible_reveals' in action_data:
        chosen_outcome = random.choice(action_data['possible_reveals'])
        results['message'] = _get_random_from_pool(chosen_outcome.get('message'), "action_msg") # Allow messages to be pools too
        potential_reveal = chosen_outcome.get('reveal')
        if potential_reveal and random.random() < reveal_chance:
             results['reveal'] = potential_reveal # Apply reveal based on chance

    elif 'possible_messages' in action_data:
        results['message'] = _get_random_from_pool(action_data['possible_messages'], "action_msg")
        # Keep static reveal if it exists alongside dynamic message
        potential_reveal = action_data.get('reveal')
        if potential_reveal and random.random() < reveal_chance:
            results['reveal'] = potential_reveal

    else:
         # Fallback to static message and reveal (respecting chance)
         results['message'] = action_data.get('message')
         potential_reveal = action_data.get('reveal')
         if potential_reveal and random.random() < reveal_chance:
             results['reveal'] = potential_reveal

    # Ensure message is a string if randomly chosen from a list/pool
    if isinstance(results['message'], list): # If _get_random_from_pool returned list itself due to error
         results['message'] = random.choice(results['message']) if results['message'] else None
    elif not isinstance(results['message'], (str, type(None))): # Handle unexpected types
        results['message'] = str(results['message'])


    # --- Display Message ---
    if results['message']:
        time.sleep(random.uniform(0.8, 1.4))
        print(wrap_text(f"-- {results['message']} --"))
        time.sleep(random.uniform(1.0, 1.5))

    return results


# --- Internal Helper ---
def _get_random_from_pool(pool_ref: Any, placeholder_name: str = "value") -> str:
    """Internal helper to safely get a random string from a pool reference."""
    chosen_value = f"<{placeholder_name}?>"
    
    # Default error string
    if isinstance(pool_ref, str) and pool_ref in all_data_pools:
        pool = all_data_pools[pool_ref]
        if pool and isinstance(pool, list):
            chosen_value = random.choice(pool)
        else:
             print(f"[DEBUG: Pool '{pool_ref}' referenced by '{placeholder_name}' is empty or not a list in all_data_pools]")
    elif isinstance(pool_ref, list) and pool_ref:
        chosen_value = random.choice(pool_ref) # Inline list provided
    elif isinstance(pool_ref, str): # Static string provided directly, not a pool name
         chosen_value = pool_ref
    elif pool_ref is None:
        chosen_value = "" # Allow None to mean empty string replacement
    # else: pool_ref is invalid or an empty list was passed directly

    # Ensure return is always a string
    return str(chosen_value) if chosen_value is not None else ""

# -----------------------------------------------------------------------------
print("[game_logic.py] Loaded.") # Confirmation message
# -----------------------------------------------------------------------------