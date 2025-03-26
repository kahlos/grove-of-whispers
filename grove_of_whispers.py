# -----------------------------------------------------------------------------
# The Grove of Whispers - A Text-Based Mindfulness Adventure
# -----------------------------------------------------------------------------
# Block 1: Imports and Setup
# -----------------------------------------------------------------------------
import random
import time
import textwrap # For nicely formatting long description text


# -----------------------------------------------------------------------------
# Block 2: Data Pools for Dynamic Generation
# (Lists of words/phrases to inject variety into descriptions and events)
# -----------------------------------------------------------------------------

# Descriptive words
pool_adjectives_calm = ["peaceful", "serene", "sun-dappled", "quiet", "still", "tranquil", "hushed"]
pool_adjectives_mysterious = ["mysterious", "enigmatic", "shadowy", "misty", "ancient-feeling", "whispering"]
pool_adjectives_nature = ["verdant", "lush", "overgrown", "wild", "moss-covered", "flower-dotted"]

# Sensory details
pool_scents_forest = ["pine needles", "damp earth", "moss", "cool air", "flowering blossoms", "wet stone"]
pool_scents_water = ["clean water", "river mud", "wet rocks", "ozone", "water lilies"]
pool_sounds_forest = ["rustling leaves", "distant bird calls", "buzzing insects", "a snapping twig", "deep silence", "wind sighing"]
pool_sounds_water = ["gurgling water", "a gentle lapping", "a distant cascade", "croaking frogs", "splashing"]

# Minor features/observations
pool_minor_sights_forest = [
    "a vibrant patch of unusual fungus on a log",
    "an intricate spiderweb glistening with dew",
    "an unusually shaped fallen leaf",
    "a shy forest creature (like a squirrel or deer) watching briefly before darting away",
    "sunlight making shifting patterns on the ground",
    "a curiously twisted branch on an old tree",
    "animal tracks in the soft earth",
]
pool_minor_sights_water = [
    "the reflection of the sky on the water's surface",
    "smooth, colourful pebbles beneath the surface",
    "a small fish darting into hiding",
    "water striders dancing on the surface",
    "sunlight sparkling on ripples",
]

# Possible flavour events (location independent, or make location specific lists)
pool_flavor_events = [
    "A sudden gust of wind rustles everything around you, then fades.",
    "You hear a distinct, clear bird call, then silence.",
    "A strangely coloured butterfly flits past erratically.",
    "For a fleeting moment, you smell an unidentifiable sweet fragrance.",
    "The quality of light changes subtly, as if a cloud passed far overhead.",
    "You feel a brief, tingling sensation, like static electricity in the air.",
]

# Dynamic action results/messages
pool_breathe_insights = [
    "With the breath, a layer of mental fog seems to lift.",
    "You feel a little more grounded, more present in your body.",
    "The breath anchors you to this exact moment.",
    "A sense of simple okay-ness arises with the exhale.",
]
pool_listen_insights = [
    "The world seems richer, filled with layers of subtle sound.",
    "You distinguish a sound you hadn't consciously registered before.",
    "The silence between the sounds becomes noticeable and peaceful.",
    "Focusing on sound helps quiet the internal chatter for a moment.",
]
pool_feel_insights = [
    "The physical sensation brings you sharply into the present.",
    "Grounding through touch reduces the feeling of being adrift.",
    "You appreciate the simple reality of the physical world.",
]

# --- Dictionary to easily access pools by name ---
# (Makes referencing pools in location data cleaner)
all_data_pools = {
    "adj_calm": pool_adjectives_calm,
    "adj_mysterious": pool_adjectives_mysterious,
    "adj_nature": pool_adjectives_nature,
    "scent_forest": pool_scents_forest,
    "scent_water": pool_scents_water,
    "sound_forest": pool_sounds_forest,
    "sound_water": pool_sounds_water,
    "sight_forest": pool_minor_sights_forest,
    "sight_water": pool_minor_sights_water,
    "events": pool_flavor_events,
    "breathe_insight": pool_breathe_insights,
    "listen_insight": pool_listen_insights,
    "feel_insight": pool_feel_insights,
}
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Block 3: Modified Game Data (Using Templates)
# -----------------------------------------------------------------------------
locations = {
    'clearing': {
        'description_template': "You stand in a {adj} clearing. Ancient stones covered in moss form a rough circle in the center. The air is {adj_nature} and carries the scent of {scent}. You notice {sight}. A familiar restlessness urges you to keep moving.",
        'description_pools': { # Links placeholders to pool names in all_data_pools
            'adj': 'adj_calm',
            'adj_nature': ['still', 'warm', 'gentle'], # Can define inline lists too
            'scent': ['wildflowers', 'sun-warmed grass'] + pool_scents_forest, # Can combine pools
            'sight': pool_minor_sights_forest + ["bees buzzing industriously around flowers"]
        },
        'dynamic_intro': [ # Keep these too for variety
            "A gentle breeze rustles the leaves above.",
            "Sunlight warms your face.",
            "The quiet feels vast and deep.",
        ],
        'event_chance': 0.3, # 30% chance of a flavour event here
        'exits': {'n': 'dark_woods_entrance', 'e': 'gentle_slope_base'},
        'actions': {
            's': {
                'text': "You settle onto the large, mossy stone. It's cool and damp beneath your hand, surprisingly soft. Focusing on the texture, the urge to rush quiets down. You notice tiny details - dew drops, a ladybug.",
                'message': "A moment of stillness grounds you."
            },
            'b': {
                'text': "You stand still, taking a slow breath in... and out... Another... And one more... The inner chatter softens slightly.",
                'possible_messages': 'breathe_insight', # Reference a pool for message
                 # --- Dynamic Reveal Example ---
                'possible_reveals': [ # Choose ONE potential reveal effect
                    {'reveal': {'w': 'hidden_track_start'}, 'message': "Clarity sharpens. You spot a hidden path!"},
                    {'reveal': None, 'message': "You feel calmer, but see no new paths."},
                    # Add more potential outcomes here
                ]
            },
            'l': {
                'text': "You pause, closing your eyes to simply listen. The {sound}... and beneath it, a deeper quiet.",
                'description_pools': {'sound': pool_sounds_forest}, # Template within an action!
                'possible_messages': 'listen_insight',
            }
        }
    },
    'dark_woods_entrance': {
        'description_template': "The trees grow close here, casting {adj} shadows. The air is cooler, smelling of {scent}. The path ahead [N] looks uncertain. Moss hangs heavy. You see {sight} nearby. The clearing [S] is behind you.",
        'description_pools': {
             'adj': pool_adjectives_mysterious,
             'scent': pool_scents_forest,
             'sight': pool_minor_sights_forest,
        },
        'dynamic_intro': ["A twig snaps nearby.", "An owl hoots softly, unseen.", "A chill settles briefly."],
        'event_chance': 0.2,
        'exits': {'s': 'clearing', 'n': 'deep_woods'},
        'actions': {
             'f': { # Feel Moss
                 'text': "You reach out to the moss on a branch. It's {texture}, {temperature}. Focusing on the sensation anchors you.",
                 'description_pools': {
                    'texture': ['damp', 'surprisingly rough', 'cool and yielding'],
                    'temperature': ['cold', 'cool', 'surprisingly dry in one patch']
                 },
                 'possible_messages': 'feel_insight',
             },
             'b': {
                 'text': "Breathing consciously, you notice the cool air. Despite the shadows, a measure of calm returns.",
                 'possible_messages': 'breathe_insight',
                 # Could add possible reveal for a faint side path sometimes?
             }
        }
    },
     'deep_woods': {
        'description_template': "Deeper in the woods. It's much {adj_light}. It feels {adj_mood} and easy to get lost. Paths seem indistinct. The way back [S] is faintly visible.",
         'description_pools': {
            'adj_light': ['darker', 'dimmer', 'shadow-filled'],
            'adj_mood': ['confusing', 'disorienting', 'overgrown', 'suffocatingly quiet'],
         },
         'event_chance': 0.4, # Higher chance of unsettling events?
         'exits': {'s':'dark_woods_entrance'},
         'actions': {
             'b': {
                 'text': "Focusing on your breath... in... out... The rising panic softens. You feel your feet firmly on the ground.",
                 'possible_messages': 'breathe_insight',
                 # Conditional Reveal - Increased chance if calm/focused? (Needs state tracking later)
                 'possible_reveals': [
                     {'reveal': {'n': 'quiet_stream'}, 'message': "As calm settles, one path [N] seems slightly clearer."},
                     {'reveal': None, 'message': "You feel centered, but the paths remain confusing."},
                 ],
            },
             'o': {
                 'text': "Acknowledging thoughts ('I'm lost!', 'Which way?') without judgment, like watching clouds. They are just thoughts.",
                 'message': "Observing thoughts creates distance from them."
            }
        }
     },
     'quiet_stream': {
         'description_template': "You've found a small, {adj} stream flowing [E]. The water {sound} over {stones}. Sunlight filters through, making it less gloomy. Back [S] is the darker woods.",
         'description_pools': {
             'adj': ['quiet', 'clear', 'peaceful', 'chuckling'],
             'sound': pool_sounds_water,
             'stones': ['smooth pebbles', 'mossy rocks', 'flat stones']
         },
         'event_chance': 0.1,
         'exits': {'s': 'deep_woods', 'e': 'stream_bend'},
         'actions': {
            'l': {
                 'text': "You listen only to the stream. The gentle sounds seem to wash away distraction.",
                 'possible_messages': 'listen_insight',
             },
             'feel water': {
                 'text': "Dipping your fingers in, the water is {temperature}. It feels {sensation}.",
                  'description_pools': {
                      'temperature': ['cool', 'cold', 'surprisingly mild'],
                      'sensation': ['refreshing', 'very real', 'soothing']
                  },
                 'possible_messages': 'feel_insight',
             }
         }
     },

    # --- Add more dynamic locations using templates ---
    # 'gentle_slope_base', 'slope_top', 'hidden_track_start', 'ancient_tree'
    # need conversion to the template format as well.

    # --- Keep Endings Static For Now ---
    'valley_view': {
        'description': "The view is breathtaking... [[ You have found a moment of clarity. Thank you for playing! Type 'quit' to exit. ]]",
        'exits': {}, 'actions': {} # Minimal data for ending locations
    },
    'stream_bend': {
        'description': "The stream bends here... [[ You have found a moment of flow. Thank you for playing! Type 'quit' to exit. ]]",
        'exits': {}, 'actions': {}
    },
}
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Block 4: Game State Variables
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
# Block 5: Helper Functions
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


# (Handles dynamic description generation and event triggering)
def display_location(location_id):
    """Gets location data, generates dynamic description, and prints it."""
    global revealed_exits_this_turn
    revealed_exits_this_turn = {} # Reset on entering location

    location = locations.get(location_id)
    if not location:
        print(wrap_text(f"Error: Location not found! ID: '{location_id}'"))
        # Consider adding a fallback, e.g., move player to start or safe default
        return

    # --- Dynamic Intro ---
    if location.get('dynamic_intro'):
        print(wrap_text(f"\n{random.choice(location['dynamic_intro'])}"))
        time.sleep(random.uniform(0.6, 1.2))

    # --- Description Generation ---
    template = location.get('description_template', location.get('description')) # Fallback to static desc
    if not template:
        print(wrap_text("You are somewhere... but the details are hazy.")) # Error fallback
        return

    format_dict = {}
    pools_to_use = location.get('description_pools', {})

    # Populate format_dict with random choices from specified pools
    for placeholder, pool_ref in pools_to_use.items():
        chosen_value = ""
        if isinstance(pool_ref, str) and pool_ref in all_data_pools:
            # Pool name provided, choose from global pool
            chosen_value = random.choice(all_data_pools[pool_ref])
        elif isinstance(pool_ref, list):
            # Inline list provided, choose from it
            chosen_value = random.choice(pool_ref)
        else:
            # Placeholder exists but pool reference is invalid/missing
             chosen_value = f"<{placeholder}?>"
        # Mark missing elements
        format_dict[placeholder] = chosen_value

    # Format the template
    try:
        final_description = template.format(**format_dict)
    except KeyError as e:
        print(wrap_text(f"[DEBUG: Template formatting error - key {e}]"))
        final_description = template # Show raw template on error

    print(wrap_text(final_description))

    # --- Flavor Event Trigger ---
    event_chance = location.get('event_chance', 0) # Get chance, default 0
    if random.random() < event_chance:
        # Get available events - either location specific or global pool
        event_pool = location.get('possible_events', all_data_pools['events'])
        if event_pool: # Ensure there are events to choose from
            chosen_event = random.choice(event_pool)
            time.sleep(random.uniform(0.8, 1.5)) # Pause before event
            print(wrap_text(f"\nSuddenly: {chosen_event}"))
            time.sleep(random.uniform(1.0, 1.8)) # Pause after event

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
# Block 6: Main Game Loop
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
        action_text_template = action_data.get('text', "You perform the action.") # Get action text template

        # --- Format action text if it contains placeholders ---
        action_format_dict = {}
        action_pools_to_use = action_data.get('description_pools', {})
        for placeholder, pool_ref in action_pools_to_use.items():
            chosen_value = ""
            if isinstance(pool_ref, str) and pool_ref in all_data_pools:
                 chosen_value = random.choice(all_data_pools[pool_ref])
            elif isinstance(pool_ref, list):
                 chosen_value = random.choice(pool_ref)
            else:
                 chosen_value = f"<{placeholder}?>"
            action_format_dict[placeholder] = chosen_value

        try:
            final_action_text = action_text_template.format(**action_format_dict)
        except KeyError as e:
            print(wrap_text(f"[DEBUG: Action text formatting error - key {e}]"))
            final_action_text = action_text_template # Show raw template on error

        # Print action text with a pause
        print("") # Add a newline before action text
        slow_print(final_action_text, delay_min=1.2, delay_max=2.0)

        # --- Handle Dynamic Outcomes (Messages and Reveals) ---
        final_message = None
        reveals_for_this_action = None

        if 'possible_reveals' in action_data:
            # Choose one outcome from the list
            chosen_outcome = random.choice(action_data['possible_reveals'])
            final_message = chosen_outcome.get('message')
            reveals_for_this_action = chosen_outcome.get('reveal') # Could be None

        elif 'possible_messages' in action_data:
             # Choose a message from the specified pool
             pool_ref = action_data['possible_messages']
             if isinstance(pool_ref, str) and pool_ref in all_data_pools:
                 final_message = random.choice(all_data_pools[pool_ref])
             elif isinstance(pool_ref, list):
                 final_message = random.choice(pool_ref)
             # Keep static reveal if it exists alongside dynamic message
             reveals_for_this_action = action_data.get('reveal')

        else:
             # Fallback to static message and reveal
             final_message = action_data.get('message')
             reveals_for_this_action = action_data.get('reveal')

        # --- Display Message & Handle Reveals ---
        if final_message:
            time.sleep(random.uniform(0.8, 1.4))
            print(wrap_text(f"-- {final_message} --"))
            time.sleep(random.uniform(1.0, 1.5))

        if reveals_for_this_action:
            revealed_exits_this_turn.update(reveals_for_this_action)
            # print(f"[DEBUG] Revealed exits by action: {reveals_for_this_action}") # Optional debug

        # Handle potential state changes (placeholder)
        if action_data.get('state_change'):
            pass # state_changer = action_data['state_change']; state_changer()

        # Action completes the turn, let loop restart to show updates
        # No 'continue' needed here unless action should prevent re-display

    # --- Add this check for completeness at the end of the loop, before it repeats ---
    elif raw_input != "quit" and raw_input not in combined_exits:
        # If the input wasn't quit, wasn't an exit, wasn't an action... it was likely invalid.
        # The initial validation should catch most, but this is a fallback.
        # The 'invalid command' message is printed near the input prompt logic.
        # We just ensure the loop continues correctly.
        pass

    # If input was processed (or if it fell through somehow), the loop will restart
    # causing the location to be re-displayed along with updated prompts.

# --- End of Game ---
# (Code here is reached only when game_active becomes False)
print("\nGame ended.")
# -----------------------------------------------------------------------------