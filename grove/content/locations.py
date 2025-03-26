# grove/content/locations.py
# Defines the main 'locations' dictionary for the game map and interactions.

# Potentially import pool names if directly referencing them, but better
# to reference via strings and let dynamics.py handle pool lookup.

locations = {
    # --- Start location ---
    'clearing': {
        'description_template': "You stand in a {adj} clearing. Ancient stones covered in moss form a rough circle in the center. The air is {adj_nature} and carries the scent of {scent}. You notice {sight}. A familiar restlessness urges you to keep moving.",
        'description_pools': { # Refers to keys in all_data_pools (from pools.py)
            'adj': 'adj_calm',
            'adj_nature': ['still', 'warm', 'gentle'],
            'scent': ['wildflowers', 'sun-warmed grass', 'scent_forest'], # Can mix strings and pool refs
            'sight': 'sight_forest'
        },
        'audio_mood': 'clearing_calm',
        'dynamic_intro': ["A gentle breeze rustles the leaves above.", "Sunlight warms your face.", "The quiet feels vast and deep."],
        'event_chance': 0.25,
        'exits': {'n': 'dark_woods_entrance', 'e': 'gentle_slope_base'},
        'actions': {
            's': { # Sit
                'text': "You settle onto a large, mossy stone. It's {texture} beneath your hand. Focusing on the feeling, the urge to rush quiets. You notice tiny details - {sight_detail}.",
                'description_pools': {
                    'texture': ['cool and damp', 'surprisingly soft', 'rougher than expected'],
                    'sight_detail': ['dew drops sparkling', 'a ladybug exploring', 'the intricate structure of the moss']
                 },
                 'possible_messages': 'sit_insight',
            },
            'b': { # Breathe
                'text': "Standing still, you take a slow breath in... and out... Another... And one more... The inner chatter softens slightly.",
                'possible_messages': 'breathe_insight',
                'possible_reveals': [ # Outcomes selected randomly
                    {'reveal': {'w': 'hidden_track_start'}, 'message': "Clarity sharpens. You spot a hidden path westward!"},
                    {'reveal': None, 'message': "You feel calmer, centered, but see no new paths yet."},
                    {'reveal': None, 'message': "A simple breath, a simple moment."},
                ],
                'reveal_chance': 0.6 # Chance applied *if* chosen outcome has a reveal
            },
            'l': { # Listen
                'text': "Pausing, you close your eyes to simply listen. The {sound}... and beneath it, a deeper quiet.",
                'description_pools': {'sound': 'sound_forest'},
                'possible_messages': 'listen_insight',
            }
        }
    },
    # --- Other locations ---
    'dark_woods_entrance': {
        'description_template': "The trees grow close here, casting {adj_mood} shadows. The air is cooler, smelling of {scent}. The path ahead [N] looks {adj_light}. Moss hangs heavy. You see {sight} nearby. The clearing [S] is behind you.",
        'description_pools': {
             'adj_mood': 'adj_mysterious', 'scent': 'scent_forest',
             'adj_light': ['uncertain', 'dark', 'overgrown'], 'sight': 'sight_forest',
        },
        'audio_mood': 'forest_neutral',
        'dynamic_intro': ["A twig snaps nearby.", "An owl hoots softly, unseen.", "A chill settles briefly."],
        'event_chance': 0.2,
        'exits': {'s': 'clearing', 'n': 'deep_woods'},
        'actions': {
             'f': { # Feel Moss
                 'text': "You reach out to the moss on a branch. It's {texture}, {temperature}. Focusing on the sensation anchors you.",
                 'description_pools': { 'texture': ['damp', 'surprisingly rough', 'cool and yielding', 'dry and brittle'], 'temperature': ['cold', 'cool', 'clammy'] },
                 'possible_messages': 'feel_insight',
             },
             'b': { 'text': "Breathing consciously, you notice the cool air. Despite the shadows, a measure of calm returns.", 'possible_messages': 'breathe_insight', }
        }
    },
    'deep_woods': {
        'description_template': "Deeper in the woods. It's much {adj_light}. It feels {adj_mood} and easy to get lost. Tangled paths twist. You notice {sight}. The way back [S] is faintly visible.",
         'description_pools': { 'adj_light': 'adj_light', 'adj_mood': 'adj_moody', 'sight': 'sight_forest' },
         'audio_mood': 'woods_deep',
         'event_chance': 0.4,
         'exits': {'s': 'dark_woods_entrance'},
         'actions': {
             'b': { # Breathe reveals exit N here
                 'text': "Focusing on your breath... in... out... The rising {feeling} softens. You feel your feet firmly on the ground.",
                  'description_pools': { 'feeling': ['panic', 'confusion', 'anxiety', 'sense of being lost'] },
                 'possible_messages': 'breathe_insight',
                 'possible_reveals': [
                     {'reveal': {'n': 'quiet_stream'}, 'message': "As calm settles, one path northward [N] seems slightly clearer."},
                     {'reveal': None, 'message': "You feel centered, but the paths remain confusing."},
                 ],
                 'reveal_chance': 0.7
            },
             'o': { # Observe Thoughts
                 'text': "Acknowledging thoughts ('I'm lost!', 'Which way?') without judgment, like watching {metaphor}. They are just thoughts.",
                  'description_pools': { 'metaphor': ['clouds pass', 'leaves float by on a stream', 'bubbles rising and popping'] },
                 'message': "Observing thoughts creates distance from them."
            },
             'l': {
                'text': "You stop and listen intently. Only {sound} breaks the deep silence.",
                 'description_pools': {'sound': ['faint rustling', 'your own heartbeat', 'a distant, unidentifiable noise']},
                'possible_messages': 'listen_insight',
             }
        }
     },
    # ... (Include ALL your other location definitions here, including slope_base, slope_top, etc.) ...
    'gentle_slope_base': {
        'description_template': "A wide, {adj} slope rises gently to the [E]ast. Small, {adj_nature} flowers dot the hillside under the {weather} sky. You can hear faint {sound} from further up. The clearing is back to the [W]est.",
        'description_pools': { 'adj': ['grassy', 'sunlit', 'gentle'], 'adj_nature': 'adj_nature', 'weather': ['warm sun', 'blue sky', 'partly cloudy sky'], 'sound': 'sound_water' },
        'audio_mood': 'clearing_calm',
        'dynamic_intro': ["The warmth here feels inviting.", "A pleasant scent of grass and flowers hangs in the air."],
        'event_chance': 0.15,
        'exits': {'w': 'clearing', 'e': 'slope_top'},
        'actions': {
             'l': {
                'text': "You focus on the sound of water. It seems to be coming from over the crest [E]. It's a {adj_sound} sound.",
                 'description_pools': {'adj_sound': ['gentle', 'soothing', 'faint but clear']}, 'possible_messages': 'listen_insight',
             },
             'examine flowers': {
                'text': "Kneeling down, you look closely at the tiny wildflowers. Their colours are {color_detail}, their shapes intricate. Simple beauty.",
                'description_pools': {'color_detail': ['vibrant blues and yellows', 'delicate whites and pinks', 'a surprising mix of deep purples']},
                'message': "Appreciating the small details.",
             }
        }
    },
    'slope_top': {
        'description_template': "You reach the top of the slope. Before you lies a {adj_view} vista overlooking a valley [E]. A small, {adj_spring} spring bubbles from {rocks} here, feeding a stream that flows down. Path back down is [W]. You see {sight}.",
        'description_pools': { 'adj_view': ['beautiful', 'expansive', 'peaceful', 'hazy but vast'], 'adj_spring': ['clear', 'bubbling', 'quiet'], 'rocks': ['mossy rocks', 'smooth grey stones', 'a fissure in the earth'], 'sight': ['sight_general', 'sight_water'] },
        'audio_mood': 'stream', 
         'dynamic_intro': ["A refreshing breeze blows here.", "The sound of the spring is calming."], 'event_chance': 0.1,
         'exits': {'w':'gentle_slope_base', 'e': 'valley_view'},
         'actions': {
             'examine spring': {
                 'text': "Kneeling by the spring, the water is {adj_water}, bubbling gently over {pebbles}. Watching the flow is mesmerizing.",
                 'description_pools': { 'adj_water': ['crystal clear', 'cool', 'sparkling'], 'pebbles': ['smooth pebbles', 'colourful stones', 'dark sand'] },
                 'possible_messages': ['Simple beauty.', 'Lost in the gentle motion.', 'A moment of pure presence.'],
             },
             'drink': { 'text': "You cup your hands and take a sip of the cool, clear water. It tastes {taste}.", 'description_pools': {'taste': ['fresh and clean', 'earthy', 'like pure stone']}, 'message': "Refreshing." },
             'b': { 'text': "Taking a breath here, feeling the open space around you, brings a sense of {feeling}.", 'description_pools': {'feeling': ['calm', 'perspective', 'openness']}, 'possible_messages': 'breathe_insight' }
         }
    },
    'hidden_track_start': {
        'description_template': "Pushing aside a {bush_type} bush reveals a faint, narrow track heading [W]est into a {adj_density} part of the woods. It smells of {scent}. The clearing is back [E].",
        'description_pools': { 'bush_type': ['flowering', 'thorny', 'dense leafy'], 'adj_density': ['denser', 'quieter', 'more shadowed'], 'scent': ['scent_forest', 'crushed leaves']},
        'audio_mood': 'forest_mysterious',
        'dynamic_intro': ["The air here feels still and expectant.", "It's noticeably quieter here than the clearing."], 'event_chance': 0.3,
        'exits': {'e': 'clearing', 'w': 'ancient_tree'},
        'actions': {
             'f': { # Feel ground
                'text': "You kneel and feel the path. It's {texture}, packed down {firmness}. You notice {detail}.",
                 'description_pools': { 'texture': ['soft earth', 'covered in old leaves', 'slightly muddy'], 'firmness': ['slightly', 'firmly in places', 'very lightly'], 'detail': ['the imprint of a deer hoof', 'a patch of bright green moss', 'nothing much of note'] },
                 'possible_messages': 'feel_insight',
             },
             'l': { 'text': "Listening... it's very quiet. Just the {sound}.", 'description_pools': {'sound': ['faintest whisper of wind', 'distant woods sounds', 'sound of your own quiet breathing']}, 'possible_messages': 'listen_insight', }
        }
    },
    'ancient_tree': {
        'description_template': "The narrow track ends at the base of an enormous, ancient tree. Its bark is {bark_adj}, and branches reach high above. It feels {feeling} here. The track leads back [E]. {sight}",
        'description_pools': { 'bark_adj': ['deeply furrowed', 'rough and gnarled', 'covered in mosses and lichens'], 'feeling': ['wise and peaceful', 'solemn and quiet', 'powerfully still', 'timeless'], 'sight': 'sight_forest' },
        'audio_mood': 'forest_mysterious',
         'dynamic_intro': ["Sunlight filters magically through the high canopy.", "The air is cool and still around the great trunk."], 'event_chance': 0.1,
         'exits': {'e':'hidden_track_start'},
         'actions': {
             'touch tree': {
                 'text': "You place your hand on the {texture} bark. It feels {sensation}, radiating a quiet strength. You feel a connection to its long, slow existence.",
                 'description_pools': { 'texture': ['rough, sturdy', 'cool, mossy', 'surprisingly smooth in patches'], 'sensation': ['solid and ancient', 'alive yet still', 'calm and reassuring'] },
                 'possible_messages': ['A feeling of deep time and resilience.', 'Grounded by immense stillness.'],
             },
             's': { # Sit
                 'text': "You sit at the base of the tree, leaning against its trunk. The peace here is profound. You simply observe {observation}.",
                 'description_pools': { 'observation': ['the light filtering through the leaves', 'tiny insects crawling on the bark', 'the gentle sway of branches far above'] }, 'possible_messages': 'sit_insight',
             },
             'b': { 'text': "Breathing slowly in the presence of this ancient being feels restorative.", 'possible_messages': 'breathe_insight', }
         }
    },
     'quiet_stream': {
        'description_template': "You've found a small, {adj} stream flowing [E]. The water {sound} over {stones}. Sunlight filters through here, making it less gloomy. {sight}. The path back [S] is clear.",
        'description_pools': { 'adj': ['quiet', 'clear', 'peaceful', 'chuckling', 'meandering'], 'sound': 'sound_water', 'stones': ['smooth pebbles', 'mossy rocks', 'flat stones', 'sparkling sand'], 'sight': 'sight_water', },
        'audio_mood': 'stream',
        'dynamic_intro': ["The sound of water is soothing here.", "It feels cooler near the stream."], 'event_chance': 0.15,
        'exits': {'s': 'deep_woods', 'e': 'stream_bend'},
        'actions': {
            'l': { 'text': "Listening only to the stream, the {sound_detail} seems to wash away distraction.", 'description_pools': {'sound_detail': ['soft gurgling', 'occasional splash', 'steady flow']}, 'possible_messages': 'listen_insight', },
            'feel water': { 'text': "Dipping your fingers in, the water is {temperature}. It feels {sensation}.", 'description_pools': { 'temperature': ['cool', 'cold', 'surprisingly mild'], 'sensation': ['refreshing', 'very real', 'soothing', 'alive'] }, 'possible_messages': 'feel_insight', },
            'skip stone': { 'text': "You find a perfectly smooth, flat stone. With a flick of the wrist, you send it skipping across the water... {skips}!", 'description_pools': { 'skips': ['once, twice... ploop', 'three satisfying skips!', 'a clumsy splash', 'four, maybe five skips! Wow'] }, 'message': "A moment of playful focus." }
         }
     },
     # --- Endings ---
     'valley_view': {
        'description': "The view from the cliff edge is breathtaking... [[ You have found a moment of clarity. Thank you for playing! Type 'quit' to exit. ]]",
        'audio_mood': 'clearing_calm',
        'exits': {}, 'actions': {}
     },
     'stream_bend': {
        'description': "The stream bends here... [[ You have found a moment of flow. Thank you for playing! Type 'quit' to exit. ]]",
        'audio_mood': 'stream',
        'exits': {}, 'actions': {}
     },
}


# Basic validation
if not isinstance(locations, dict):
    raise TypeError("Locations data did not load correctly as a dictionary.")
if 'clearing' not in locations:
    raise ValueError("Essential starting location 'clearing' is missing from locations data.")

print("[locations.py] Loaded with audio moods.")