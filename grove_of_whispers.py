# -----------------------------------------------------------------------------
# The Grove of Whispers - A Text-Based Mindfulness Adventure
# -----------------------------------------------------------------------------
# Block 1: Imports and Setup
# -----------------------------------------------------------------------------
import random
import time
import textwrap # For nicely formatting long description text

# (Ensure these imports are at the top of your file)

# -----------------------------------------------------------------------------
# Block 2: Game Data
# (This section holds the world map. It can be expanded significantly
# or potentially moved to a separate data file later for complex games.)
# -----------------------------------------------------------------------------
locations = {
    # --- Your existing locations dictionary goes here ---
    # 'clearing': { ... },
    # 'dark_woods_entrance': { ... },
    # etc.
    # ...
# --- Add more locations here ---
    'clearing': {
        'description': "You stand at the edge of a sun-dappled clearing. Ancient stones covered in moss form a rough circle in the center. The air hums with the sound of bees, and the scent of wildflowers is {fragrance}. A familiar restlessness urges you to keep moving, to find the 'end'.",
        'dynamic_intro': [
            "A gentle breeze rustles the leaves above.",
            "Sunlight warms your face.",
            "The quiet feels vast and deep.",
            "A distant bird calls out a short, clear note."
        ],
        'fragrance_options': ["strong", "delicate", "sweet", "faint but clear"], # Randomly chosen detail
        'exits': {'n': 'dark_woods_entrance', 'e': 'gentle_slope_base'},
        'actions': {
            's': { # Sit on stone
                'text': "You settle onto the large, mossy stone. It's cool and damp beneath your hand, surprisingly soft. You focus on the feeling, the texture. The urge to rush quiets down for a moment. Looking closely at the moss, you see tiny droplets of dew sparkling like jewels, and a ladybug diligently exploring its miniature green world. The world feels a little more real, more solid.",
                'reveal': None,
                'message': "A moment of stillness."
            },
            'b': { # Breathe
                'text': "You stand still. You close your eyes (or soften your gaze) and take a slow breath in... and out... letting the tension go. Another breath... feeling your feet on the earth... And one more... noticing the air on your skin. The buzzing urgency in your chest softens. When you open your eyes, the sunlight seems warmer, the colours brighter.",
                'reveal': {'w': 'hidden_track_start'}, # Reveals the hidden West track
                'message': "Clarity sharpens slightly. You notice a potential path you missed before."
            },
            'l': { # Listen
                'text': "You close your eyes and listen. The buzzing of bees nearby, the rustle of leaves in the breeze, the distant bird call... and beneath it all, a deeper silence. You focus on just the sounds, letting them wash over you without needing to name them.",
                'reveal': None,
                'message': "The world seems fuller, more layered."
             }
        }
    },
    'dark_woods_entrance': {
        'description': "The trees here grow closer together, casting deep shadows. The air is cooler. The path ahead [N] looks dark and uncertain. Moss hangs heavy from branches. The clearing is visible behind you [S].",
        'dynamic_intro': [
            "A twig snaps nearby.",
            "The smell of damp earth is strong.",
            "A chill crawls up your spine for a moment, then fades."
            ],
        'exits': {'s': 'clearing', 'n': 'deep_woods'}, # 'n' leads deeper
        'actions': {
             'f': { # Feel
                 'text': "You reach out and touch the moss hanging from a low branch. It's surprisingly cold, wet, and slightly rough. You feel the dampness seeping into your fingertips, anchoring you to this spot.",
                 'reveal': None,
                 'message': "Grounded in the present sensation."
             },
            'b': {
                 'text': "You take a conscious breath, noticing the cool air entering your nostrils and the slightly warmer air leaving. Despite the shadows, a sense of calm holds steady.",
                 'reveal': None,
                 'message': "Steady."
            }
        }
    },
    'gentle_slope_base': {
        'description': "A wide, grassy slope rises gently to the [E]ast. Small, colourful flowers dot the hillside. The sun feels warm here. You can hear the faint sound of running water from further up. The clearing is back to the [W]est.",
        'exits': {'w': 'clearing', 'e': 'slope_top'}, # 'e' goes up
        'actions': {
             'l': { # Listen
                'text': "You focus on the sound of running water. It seems to be coming from over the crest of the slope [E]. It's a gentle, soothing sound.",
                'reveal': None,
                'message': "Curiosity piqued by the sound."
             }
        }
    },
    'hidden_track_start': {
        'description': "Pushing aside a flowering bush reveals a faint, narrow track leading [W]est into a denser part of the woods, seemingly less travelled. The clearing is back to the [E]ast.",
        'dynamic_intro': ["The air here feels still and expectant.", "It smells of crushed leaves."],
        'exits': {'e': 'clearing', 'w': 'ancient_tree'}, # 'w' follows track
        'actions': {
             'f': { # Feel ground
                'text': "You kneel and feel the path. It's soft earth, packed down slightly, but not heavily used. You notice the imprint of a deer hoof.",
                'reveal': None,
                'message': "A sense of connection to the natural world."
             }
        }
    },
    'deep_woods': {
        'description': "You are deeper in the woods. It's much darker. It's easy to feel lost. Paths seem to lead everywhere and nowhere. Maybe taking a moment to center yourself would help? The way back [S] is faintly visible.",
        'exits': {'s':'dark_woods_entrance'},
        'actions': {
             'b': {
                 'text': "Breathing slowly, you focus on the feeling of your feet on the ground. The panic of being lost subsides slightly. As your eyes adjust, one path to the [N] seems slightly more defined than the others.",
                 'reveal': {'n': 'quiet_stream'}, # Only revealed by breathing
                 'message': "With calm comes clarity."
            },
             'o': { # Observe Thoughts - Example
                 'text': "Thoughts like 'I'm lost!', 'Which way is right?', 'Did I make a mistake?' bubble up. You acknowledge them without judgement, like watching clouds pass in the sky. They are just thoughts, not commands.",
                 'reveal': None,
                 'message': "Watching thoughts instead of being swept away by them."
            }
        }
    },
    'slope_top': {
        'description': "You reach the top of the slope. Before you lies a beautiful vista overlooking a valley [E]. A small, clear spring bubbles up from rocks here [Examine spring], feeding a stream that flows down the hill. The path back down is [W].",
         'exits': {'w':'gentle_slope_base', 'e': 'valley_view'}, # 'e' not fully implemented yet
         'actions': {
             'examine spring': { # Multi-word action example
                 'text': "You kneel by the spring. The water is crystal clear, bubbling gently over smooth pebbles. Watching the water flow is mesmerizing and calming.",
                 'reveal': None,
                 'message': "Simple beauty."
             }
         }
    },
    'ancient_tree': {
        'description': "The narrow track ends at the base of an enormous, ancient tree. Its bark is deeply furrowed, and its branches reach high above. It feels wise and peaceful here. The track leads back [E].",
         'exits': {'e':'hidden_track_start'},
         'actions': {
             'touch tree': {
                 'text': "You place your hand on the rough, sturdy bark. It feels solid and ancient, radiating a quiet strength. You feel a connection to its long, slow existence.",
                 'reveal': None,
                 'message': "A feeling of deep time and resilience."
             },
             's': {
                 'text': "You sit at the base of the tree, leaning against its trunk. The peace here is profound. You simply watch the light filtering through the leaves above.",
                 'reveal': None,
                 'message': "Resting in presence."
             }
         }
     },
     'quiet_stream': {
        'description': "Following the clearer path led you to a small, quiet stream flowing [E]. The water chuckles over stones. Sunlight filters through the canopy here, making it less gloomy. The path back [S] is clear.",
         'exits': {'s':'deep_woods', 'e':'stream_bend'}, # 'e' not implemented yet
         'actions': {
             # Can add actions like Listen ('L'), Feel Water ('Feel water')
             'l': {
                 'text': "You pause and listen only to the stream. The soft gurgling, the occasional splash... it seems to wash away distracting thoughts.",
                 'reveal': None,
                 'message': "Lost in the sound."
             },
              'feel water': {
                 'text': "You dip your fingers into the stream. The water is cool and flows smoothly over your skin. It feels refreshing and very real.",
                 'reveal': None,
                 'message': "A moment of clear sensation."
             }
         }
     },
     # --- Placeholder Endings/Future Areas ---
      'valley_view': {
        'description': "The view is breathtaking. Miles of forest stretch out below, bathed in gentle sunlight. You feel a sense of expansive peace wash over you. Maybe the journey wasn't about *reaching* an 'end', but about *how* you walked the path?\n\n[[ You have found a moment of clarity. Thank you for playing! Type 'quit' to exit. ]]",
        'exits': {},
        'actions': {}
     },
      'stream_bend': {
        'description': "The stream bends around a large, mossy rock formation here. The gentle sounds and the constant, steady flow of water bring a sense of calm focus. Perhaps true presence is found not by searching, but by noticing these simple moments, wherever you are?\n\n[[ You have found a moment of flow. Thank you for playing! Type 'quit' to exit. ]]",
        'exits': {},
        'actions': {}
     },
}

# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Block 3: Game State Variables
# (These track the player's current situation.)
# -----------------------------------------------------------------------------
current_location_id = 'clearing' # Start the player in the clearing
game_active = True
revealed_exits_this_turn = {} # Track temporary reveals
# --- Potential future state variables ---
# calm_level = 0
# discovered_insights = set()
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Block 4: Helper Functions
# (Functions for text formatting, displaying location info, prompts,
# and the new game introduction.)
# -----------------------------------------------------------------------------

def wrap_text(text, width=80):
    """Wraps text for cleaner display."""
    return "\n".join(textwrap.wrap(text, width))

def slow_print(text, delay_min=1.5, delay_max=2.5, width=80):
    """Prints text wrapped and with a noticeable pause."""
    print(wrap_text(text, width))
    time.sleep(random.uniform(delay_min, delay_max))

def introduction():
    """Displays the introductory text and integrated tutorial."""
    print("\n" * 2) # Add some space at the start
    slow_print("...")
    slow_print("Your mind feels... scattered. Like leaves caught in a whirlwind.")
    slow_print("Thoughts race, plans tangle, memories flicker without focus.")
    slow_print("You don't know how you got here, but...")
    slow_print("...here you are.")
    slow_print("Welcome to The Grove of Whispers.")

    print("-" * 30) # Separator

    slow_print("This place is... different. It seems to respond not just to your steps, but to your attention.")
    slow_print("Moving around is simple. Type commands like 'N', 'S', 'E', 'W' when you see exits listed like [N] North.")
    slow_print("But rushing forward might not always reveal the clearest path.")

    print("-" * 30)

    slow_print("Sometimes, the Grove invites you to pause. You might see options like:")
    slow_print("`[B] Breathe` - A reminder to take a conscious breath. Try it now, even just one. In... and out. Notice how the Grove responds when you choose this in the game.")
    time.sleep(1.0) # Slightly shorter pause for bullet points
    slow_print("`[L] Listen` - Focus only on the sounds described. What details emerge when you truly pay attention?")
    time.sleep(1.0)
    slow_print("`[F] Feel` - Ground yourself in the sensations of touch described. The texture of moss, the coolness of water, the earth beneath your feet.")
    time.sleep(1.0)
    slow_print("`[S] Sit` or `[Stillness]` - Sometimes, simply being still and observing reveals more than movement.")
    time.sleep(1.0)
    slow_print("Other actions might appear too, like `[Examine]` or `[Touch Tree]`. Use the text in the brackets as your command.")

    print("-" * 30)

    slow_print("There is no 'winning' here in the usual sense. The journey *is* the purpose.")
    slow_print("Pay attention. Be present. See what unfolds.")
    slow_print("If you ever wish to leave the Grove, simply type 'Quit'.")

    print("-" * 30)
    input("Press Enter when you are ready to begin...")


def display_location(location_id):
    """Gets location data, formats description, and prints it."""
    global revealed_exits_this_turn
    revealed_exits_this_turn = {} # Reset revealed exits when entering a new location

    location = locations.get(location_id)
    if not location:
        print(wrap_text("Error: Location not found! ID: " + location_id))
        return

    # Print dynamic intro phrase if available
    if location.get('dynamic_intro'):
        # Use a slightly shorter, varied pause for dynamic intros
        print(wrap_text(f"\n{random.choice(location['dynamic_intro'])}"))
        time.sleep(random.uniform(0.6, 1.2))

    # Prepare and print main description, inserting random elements if needed
    desc = location['description']
    try:
        # Use dictionary for formatting replacements to handle missing keys gracefully
        format_params = {}
        if '{fragrance}' in desc and location.get('fragrance_options'):
            format_params['fragrance'] = random.choice(location['fragrance_options'])
        # Add more {key} and options here if needed

        # Format the description, filling in only the keys provided
        formatted_desc = desc.format(**format_params)
    except KeyError as e:
        # If formatting fails unexpectedly, print the raw description and an error
        print(wrap_text(f"[DEBUG: Formatting Error - Missing key {e}]"))
        formatted_desc = desc

    print(wrap_text(formatted_desc))


def display_prompt(location_id):
    """Displays available exits and actions."""
    location = locations.get(location_id)
    if not location:
        return "", set() # Return empty set for valid inputs

    available_options = []
    valid_inputs = set()

    # --- Combined Exits (Standard + Revealed) ---
    all_exits = location.get('exits', {}).copy()
    all_exits.update(revealed_exits_this_turn) # Add dynamically revealed exits

    if all_exits:
        exit_parts = []
        # Sort for consistent order (N, S, E, W, etc.)
        sorted_exits = sorted(all_exits.keys(), key=lambda x: {'n':0, 's':1, 'e':2, 'w':3, 'u':4, 'd':5}.get(x.lower(), 99))

        for command in sorted_exits:
            dest_id = all_exits[command]
            # Basic direction hints
            direction_hints = {'n':'North', 's':'South', 'e':'East', 'w':'West', 'u':'Up', 'd':'Down'}
            hint = direction_hints.get(command.lower())
            display_command = command.upper() # Keep commands clear

            if hint:
                exit_parts.append(f"[{display_command}] {hint}")
            else:
                 # For non-standard exits (like a specific door ID maybe)
                 exit_parts.append(f"[{display_command}]")
            valid_inputs.add(command.lower())

        if exit_parts: # Only add the "Exits: " line if there are any
             available_options.append("Exits: " + ", ".join(exit_parts))

    # --- Mindful Actions & Interactions ---
    if location.get('actions'):
        action_parts = []
        # Sort action commands alphabetically for consistency
        sorted_actions = sorted(location['actions'].keys())

        for command in sorted_actions:
            # Display single letters Uppercase, multi-word capitalized
            command_display = command.upper() if len(command) == 1 else command.capitalize()
            action_parts.append(f"[{command_display}]")
            valid_inputs.add(command.lower()) # Add full command string

        if action_parts: # Only add the "Actions: " line if there are any
            available_options.append("Actions: " + ", ".join(action_parts))

    # Add standard quit command (always available)
    available_options.append("[Quit]")
    valid_inputs.add("quit")

    # Print the combined prompt lines
    if available_options:
        print("\n" + "\n".join(available_options))
    else: # Should only happen in error cases or poorly defined locations
        print("\n[Quit]") # Ensure quit is always an option

    return valid_inputs


# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Block 5: Main Game Loop
# (This runs the game turn by turn.)
# -----------------------------------------------------------------------------

# --- Start the Game ---
introduction() # <<< NEW: Call the introduction function here

while game_active:
    display_location(current_location_id)
    valid_commands = display_prompt(current_location_id)

    # Get player input
    raw_input = input("> ").strip().lower()

    # Process input
    if not raw_input:
        print(wrap_text("Silence... what do you choose to do?"))
        time.sleep(1)
        continue # Ask again if they just press Enter

    # Check if input is valid
    if raw_input not in valid_commands:
        # Handle slightly differently if they typed part of a multi-word command
        potential_matches = [cmd for cmd in valid_commands if isinstance(cmd, str) and cmd.startswith(raw_input)]
        if len(potential_matches) == 1 and len(raw_input) > 1: # Simple auto-complete suggestion if unique prefix
            print(wrap_text(f"Did you mean '{potential_matches[0].capitalize()}'? Try typing the full command."))
        else:
            print(wrap_text("That doesn't seem like a valid option right now. Look for choices in [Brackets]."))
        time.sleep(1)
        continue

    # Handle Quit
    if raw_input == "quit":
        print("\nMay you carry the quiet of the Grove with you. Goodbye.")
        game_active = False
        break # Exit the while loop

    # --- Handle Movement ---
    location = locations[current_location_id] # Get current location data
    combined_exits = location.get('exits', {}).copy()
    combined_exits.update(revealed_exits_this_turn) # Include temporary reveals

    if raw_input in combined_exits:
        destination_id = combined_exits[raw_input]
        if destination_id in locations:
            current_location_id = destination_id
            print(f"\n...") # Indicate moving
            # Slightly longer, varied pause for travel simulation
            time.sleep(random.uniform(1.0, 2.0))
        else:
            # This is a data error in the `locations` dictionary
            print(wrap_text(f"Error: The path marked '{raw_input.upper()}' leads somewhere undefined ('{destination_id}')!"))
            time.sleep(1.5)
        continue # Move processed, start next turn loop

    # --- Handle Actions ---
    if raw_input in location.get('actions', {}):
        action_data = location['actions'][raw_input]

        # Print action text with a pause
        print("") # Add a newline before action text
        slow_print(action_data['text'], delay_min=1.2, delay_max=2.0)

        # Optional short message after action text
        if action_data.get('message'):
            # Pause slightly before the message for emphasis
            time.sleep(random.uniform(0.8, 1.4))
            print(wrap_text(f"-- {action_data['message']} --"))
            time.sleep(random.uniform(1.0, 1.5)) # Pause after the message

        # Handle revealed exits
        if action_data.get('reveal'):
            newly_revealed = action_data['reveal']
            # Store them for the *next* prompt display within this location visit
            revealed_exits_this_turn.update(newly_revealed)
            # print(f"[DEBUG] Revealed exits: {newly_revealed}") # Optional debug

        # Handle potential state changes (if/when implemented)
        if action_data.get('state_change'):
            # Requires defining functions to modify game state, e.g.,
            # state_changer = action_data['state_change']
            # state_changer() # Call the function
             pass # Placeholder for now

        # After action, loop might sometimes implicitly continue or prompt again?
        # For now, action completes the turn. Re-display location and prompt below.
        # No 'continue' here - let the loop proceed to re-display and prompt

    # If input was processed (or if it fell through somehow), the loop will restart
    # causing the location to be re-displayed along with updated prompts.

# --- End of Game ---
# (Code here is reached only when game_active becomes False)
print("\nGame ended.")
# -----------------------------------------------------------------------------