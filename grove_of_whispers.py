# -----------------------------------------------------------------------------
# The Grove of Whispers - A Text-Based Mindfulness Adventure
# -----------------------------------------------------------------------------

import random
import time
import textwrap # For nicely formatting long description text

# --- Game Data -------------------------------------------------------------
# This dictionary holds all the information about the different locations
# in the game.
#
# Structure:
# 'location_id': {
#     'description': "Text displayed when the player enters the location.",
#     'dynamic_intro': ["A list of phrases, one chosen randomly each time.", "Adds flavour."], # Optional
#     'exits': {'command': 'destination_id', ...}, # Regular movement
#     'actions': { # Mindful actions and examining things
#         'command': {
#             'text': "Description of performing the action.",
#             'reveal': {'command': 'destination_id', ...}, # Optional: New exits revealed by this action
#             'state_change': function, # Optional: For more complex effects later
#             'message': "Optional: A short message after the action text."
#         }, ...
#     }
# }
# -----------------------------------------------------------------------------

locations = {
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
    # --- Add more locations here ---
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
             # Could add a 'drink' action etc.
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
            # Add listening, feeling water actions?
         }
     },
     # --- Placeholder Endings ---
      'valley_view': {
        'description': "The view is breathtaking. You feel a sense of peace wash over you. Maybe the journey wasn't about reaching an 'end', but about how you walked the path?\n\n[[ You have found a moment of clarity. Thank you for playing! Type 'quit' to exit. ]]",
        'exits': {},
        'actions': {}
     },
      'stream_bend': {
        'description': "The stream bends around a large rock formation here. The gentle sounds and flowing water bring a sense of calm focus. Perhaps true presence is found in these simple moments, wherever you are?\n\n[[ You have found a moment of flow. Thank you for playing! Type 'quit' to exit. ]]",
        'exits': {},
        'actions': {}
     },


}

# --- Game State Variables --------------------------------------------------
current_location_id = 'clearing'
game_active = True
# Keep track of exits revealed by actions within the current location visit
revealed_exits_this_turn = {}

# --- Helper Functions ------------------------------------------------------

def wrap_text(text, width=80):
    """Wraps text for cleaner display."""
    return "\n".join(textwrap.wrap(text, width))

def display_location(location_id):
    """Gets location data, formats description, and prints it."""
    global revealed_exits_this_turn
    revealed_exits_this_turn = {} # Reset revealed exits when entering a new location

    location = locations.get(location_id)
    if not location:
        print("Error: Location not found!")
        return

    # Print dynamic intro phrase if available
    if location.get('dynamic_intro'):
        print(wrap_text(f"\n{random.choice(location['dynamic_intro'])}"))
        time.sleep(0.5) # Small pause for effect

    # Prepare and print main description, inserting random elements if needed
    desc = location['description']
    if '{fragrance}' in desc and location.get('fragrance_options'):
      fragrance = random.choice(location['fragrance_options'])
      desc = desc.format(fragrance=fragrance)
    # Add more random insertions here if needed using .format() or f-strings

    print(wrap_text(desc))

def display_prompt(location_id):
    """Displays available exits and actions."""
    location = locations.get(location_id)
    if not location:
        return ""

    available_options = []
    valid_inputs = set()

    # Regular Exits
    all_exits = location.get('exits', {}).copy()
    all_exits.update(revealed_exits_this_turn) # Add dynamically revealed exits

    if all_exits:
        exit_parts = []
        for command, dest_id in all_exits.items():
             # Basic direction hints
            direction_hints = {'n':'North', 's':'South', 'e':'East', 'w':'West', 'u':'Up', 'd':'Down'}
            hint = direction_hints.get(command.lower())
            if hint:
                exit_parts.append(f"[{command.upper()}] {hint}")
            else:
                 exit_parts.append(f"[{command.upper()}]") # For non-standard exits if needed
            valid_inputs.add(command.lower())
        available_options.append("Exits: " + ", ".join(exit_parts))

    # Mindful Actions
    if location.get('actions'):
        action_parts = []
        for command in location['actions'].keys():
            # Simple commands are single letters, longer ones we keep as is
            command_display = command.upper() if len(command) == 1 else command.capitalize()
            action_parts.append(f"[{command_display}]")
            valid_inputs.add(command.lower()) # Add full command string for multi-word actions
        available_options.append("Actions: " + ", ".join(action_parts))

    # Add standard quit command
    available_options.append("[Quit]")
    valid_inputs.add("quit")

    print("\n" + "\n".join(available_options))
    return valid_inputs


# --- Main Game Loop --------------------------------------------------------

print("\nWelcome to The Grove of Whispers")
print("===============================")
print("Type commands like 'N', 'S', 'E', 'W' to move, or mindful actions shown in [Brackets].")
print("Type 'Quit' to exit the game.")
print("-" * 30)
time.sleep(1) # Pause before starting

while game_active:
    display_location(current_location_id)
    valid_commands = display_prompt(current_location_id)

    # Get player input
    raw_input = input("> ").strip().lower()

    # Process input
    if not raw_input:
        continue # Ask again if they just press Enter

    # Check if input is valid
    if raw_input not in valid_commands:
        print(wrap_text("That doesn't seem like a valid option right now. Try one of the options listed in [Brackets]."))
        time.sleep(1)
        continue

    # Handle Quit
    if raw_input == "quit":
        print("\nMay you carry the quiet of the Grove with you. Goodbye.")
        game_active = False
        break

    # Handle Movement (check revealed exits first, then standard)
    location = locations[current_location_id]
    combined_exits = location.get('exits', {}).copy()
    combined_exits.update(revealed_exits_this_turn)

    if raw_input in combined_exits:
        destination_id = combined_exits[raw_input]
        if destination_id in locations:
            current_location_id = destination_id
            print(f"\n...") # Indicate moving
            time.sleep(random.uniform(0.8, 1.5)) # Short pause for travel feel
        else:
            print("Error: That path leads somewhere undefined!") # Should not happen if data is correct
        continue # Skip action check

    # Handle Actions
    if raw_input in location.get('actions', {}):
        action_data = location['actions'][raw_input]

        # Print action text
        print(wrap_text(f"\n{action_data['text']}"))
        time.sleep(1.5) # Pause after mindful action text

        # Optional short message
        if action_data.get('message'):
            print(wrap_text(f"-- {action_data['message']} --"))
            time.sleep(1)

        # Handle revealed exits (store them for the *next* prompt display)
        if action_data.get('reveal'):
            # We update a temporary dict for the current location visit.
            # This means the reveal only lasts while you are 'in scope'
            # A more persistent reveal would modify the main locations dict
            revealed_exits_this_turn.update(action_data['reveal'])
            # print("[DEBUG] Revealed exits:", revealed_exits_this_turn) # Optional debug line

        # Handle potential state changes (if implemented later)
        if action_data.get('state_change'):
            # Call the state change function
            action_data['state_change']() # Requires defining functions to modify game state

        continue # Action done for this turn

# --- End of Game -----------------------------------------------------------
# (The loop condition 'game_active' becomes False)