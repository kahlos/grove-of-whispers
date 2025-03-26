# game_data.py
# Holds all the static game data: locations, pools for dynamic content.
import random # Needed if pools are dynamically combined, good practice to include

# -----------------------------------------------------------------------------
# Data Pools for Dynamic Generation
# -----------------------------------------------------------------------------
pool_adjectives_calm = ["peaceful", "serene", "sun-dappled", "quiet", "still", "tranquil", "hushed"]
pool_adjectives_mysterious = ["mysterious", "enigmatic", "shadowy", "misty", "ancient-feeling", "whispering"]
pool_adjectives_nature = ["verdant", "lush", "overgrown", "wild", "moss-covered", "flower-dotted"]
pool_adjectives_light = ['dim', 'shadow-filled', 'darker', 'gloomy', 'dusky']
pool_adjectives_moody = ['confusing', 'disorienting', 'overgrown', 'suffocatingly quiet', 'lonely', 'forgotten']

pool_scents_forest = ["pine needles", "damp earth", "moss", "cool air", "flowering blossoms", "wet stone", "fallen leaves"]
pool_scents_water = ["clean water", "river mud", "wet rocks", "ozone", "water lilies", "damp moss"]
pool_scents_general = ["fresh air", "distant rain", "sun-baked earth"]

pool_sounds_forest = ["rustling leaves", "distant bird calls", "buzzing insects", "a snapping twig", "deep silence", "wind sighing", "a squirrel chattering"]
pool_sounds_water = ["gurgling water", "a gentle lapping", "a distant cascade", "croaking frogs", "splashing", "water dripping"]
pool_sounds_general = ["faint wind", "utter silence", "your own breathing"]

pool_minor_sights_forest = [
    "a vibrant patch of unusual fungus on a log", "an intricate spiderweb glistening with dew", "an unusually shaped fallen leaf",
    "a shy forest creature watching briefly before darting away", "sunlight making shifting patterns on the ground",
    "a curiously twisted branch on an old tree", "animal tracks in the soft earth", "a woodpecker hole high on a trunk",
    "a cluster of tiny wildflowers you almost missed",
]
pool_minor_sights_water = [
    "the reflection of the sky on the water's surface", "smooth, colourful pebbles beneath the surface",
    "a small fish darting into hiding", "water striders dancing on the surface", "sunlight sparkling on ripples",
    "a dragon fly hovering nearby", "foam collecting near the bank",
]
pool_minor_sights_general = ["a strangely shaped cloud", "the texture of the ground beneath you", "a single feather lying on the path"]

pool_flavor_events = [
    "A sudden gust of wind rustles everything around you, then fades.", "You hear a distinct, clear bird call, then silence.",
    "A strangely coloured butterfly flits past erratically.", "For a fleeting moment, you smell an unidentifiable sweet fragrance.",
    "The quality of light changes subtly, as if a cloud passed far overhead.", "You feel a brief, tingling sensation, like static electricity in the air.",
    "A faint echo seems to whisper just out of hearing.", "A single leaf detaches and spirals slowly down before you.",
]

pool_breathe_insights = [
    "With the breath, a layer of mental fog seems to lift.", "You feel a little more grounded, more present in your body.",
    "The breath anchors you to this exact moment.", "A sense of simple okay-ness arises with the exhale.",
    "Each breath is a fresh start.", "You notice the subtle movement of your body as you breathe.",
]
pool_listen_insights = [
    "The world seems richer, filled with layers of subtle sound.", "You distinguish a sound you hadn't consciously registered before.",
    "The silence between the sounds becomes noticeable and peaceful.", "Focusing on sound helps quiet the internal chatter for a moment.",
    "Listening deeply connects you to the environment.",
]
pool_feel_insights = [
    "The physical sensation brings you sharply into the present.", "Grounding through touch reduces the feeling of being adrift.",
    "You appreciate the simple reality of the physical world.", "Focusing on touch is an anchor in the now.",
]
pool_sit_insights = [
    "Simply sitting and observing, stillness arises.", "The urge to *do* something fades slightly.",
    "You notice the constant small movements in the 'still' world around you.",
    "There is peace in non-doing.",
]

all_data_pools = {
    "adj_calm": pool_adjectives_calm, "adj_mysterious": pool_adjectives_mysterious, "adj_nature": pool_adjectives_nature,
    "adj_light": pool_adjectives_light, "adj_moody": pool_adjectives_moody,
    "scent_forest": pool_scents_forest, "scent_water": pool_scents_water, "scent_general": pool_scents_general,
    "sound_forest": pool_sounds_forest, "sound_water": pool_sounds_water, "sound_general": pool_sounds_general,
    "sight_forest": pool_minor_sights_forest, "sight_water": pool_minor_sights_water, "sight_general": pool_minor_sights_general,
    "events": pool_flavor_events,
    "breathe_insight": pool_breathe_insights, "listen_insight": pool_listen_insights,
    "feel_insight": pool_feel_insights, "sit_insight": pool_sit_insights,
    # Combine pools for convenience
    "sight_any": pool_minor_sights_forest + pool_minor_sights_water + pool_minor_sights_general,
    "scent_any": pool_scents_forest + pool_scents_water + pool_scents_general,
    "sound_any": pool_sounds_forest + pool_sounds_water + pool_sounds_general,
}

# -----------------------------------------------------------------------------
# Locations Data (Using Templates and Pools)
# -----------------------------------------------------------------------------
locations = {
    'clearing': {
        'description_template': "You stand in a {adj} clearing. Ancient stones covered in moss form a rough circle in the center. The air is {adj_nature} and carries the scent of {scent}. You notice {sight}. A familiar restlessness urges you to keep moving.",
        'description_pools': {
            'adj': 'adj_calm',
            'adj_nature': ['still', 'warm', 'gentle'],
            'scent': ['wildflowers', 'sun-warmed grass'] + all_data_pools['scent_forest'],
            'sight': 'sight_forest'
        },
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
                'possible_reveals': [
                    {'reveal': {'w': 'hidden_track_start'}, 'message': "Clarity sharpens. You spot a hidden path westward!"},
                    {'reveal': None, 'message': "You feel calmer, centered, but see no new paths yet."},
                    {'reveal': None, 'message': "A simple breath, a simple moment."},
                ],
                'reveal_chance': 0.6 # Chance the reveal happens if chosen outcome has one
            },
            'l': { # Listen
                'text': "Pausing, you close your eyes to simply listen. The {sound}... and beneath it, a deeper quiet.",
                'description_pools': {'sound': 'sound_forest'},
                'possible_messages': 'listen_insight',
            }
        }
    },
    'dark_woods_entrance': {
        'description_template': "The trees grow close here, casting {adj_mood} shadows. The air is cooler, smelling of {scent}. The path ahead [N] looks {adj_light}. Moss hangs heavy. You see {sight} nearby. The clearing [S] is behind you.",
        'description_pools': {
             'adj_mood': 'adj_mysterious',
             'scent': 'scent_forest',
             'adj_light': ['uncertain', 'dark', 'overgrown'],
             'sight': 'sight_forest',
        },
        'dynamic_intro': ["A twig snaps nearby.", "An owl hoots softly, unseen.", "A chill settles briefly."],
        'event_chance': 0.2,
        'exits': {'s': 'clearing', 'n': 'deep_woods'},
        'actions': {
             'f': { # Feel Moss
                 'text': "You reach out to the moss on a branch. It's {texture}, {temperature}. Focusing on the sensation anchors you.",
                 'description_pools': {
                    'texture': ['damp', 'surprisingly rough', 'cool and yielding', 'dry and brittle'],
                    'temperature': ['cold', 'cool', 'clammy']
                 },
                 'possible_messages': 'feel_insight',
             },
             'b': { # Breathe
                 'text': "Breathing consciously, you notice the cool air. Despite the shadows, a measure of calm returns.",
                 'possible_messages': 'breathe_insight',
             }
        }
    },
    'deep_woods': {
        'description_template': "Deeper in the woods. It's much {adj_light}. It feels {adj_mood} and easy to get lost. Tangled paths twist. You notice {sight}. The way back [S] is faintly visible.",
         'description_pools': {
            'adj_light': 'adj_light',
            'adj_mood': 'adj_moody',
            'sight': 'sight_forest',
         },
         'event_chance': 0.4,
         'exits': {'s': 'dark_woods_entrance'}, # Exit 'N' only revealed by action 'b' below
         'actions': {
             'b': { # Breathe
                 'text': "Focusing on your breath... in... out... The rising {feeling} softens. You feel your feet firmly on the ground.",
                  'description_pools': {
                    'feeling': ['panic', 'confusion', 'anxiety', 'sense of being lost']
                  },
                 'possible_messages': 'breathe_insight',
                 'possible_reveals': [
                     {'reveal': {'n': 'quiet_stream'}, 'message': "As calm settles, one path northward [N] seems slightly clearer."},
                     {'reveal': None, 'message': "You feel centered, but the paths remain confusing."},
                 ],
                 'reveal_chance': 0.7 # High chance of revealing the path if you breathe here
            },
             'o': { # Observe Thoughts
                 'text': "Acknowledging thoughts ('I'm lost!', 'Which way?') without judgment, like watching {metaphor}. They are just thoughts.",
                  'description_pools': {
                      'metaphor': ['clouds pass', 'leaves float by on a stream', 'bubbles rising and popping']
                  },
                 'message': "Observing thoughts creates distance from them."
            },
             'l': { # Listen
                'text': "You stop and listen intently. Only {sound} breaks the deep silence.",
                 'description_pools': {'sound': ['faint rustling', 'your own heartbeat', 'a distant, unidentifiable noise']},
                'possible_messages': 'listen_insight',
             }
        }
     },
    'gentle_slope_base': { # *** This is the location needed to fix the bug ***
        'description_template': "A wide, {adj} slope rises gently to the [E]ast. Small, {adj_nature} flowers dot the hillside under the {weather} sky. You can hear faint {sound} from further up. The clearing is back to the [W]est.",
        'description_pools': {
            'adj': ['grassy', 'sunlit', 'gentle'],
            'adj_nature': pool_adjectives_nature,
            'weather': ['warm sun', 'blue sky', 'partly cloudy sky'],
            'sound': pool_sounds_water,
        },
        'dynamic_intro': ["The warmth here feels inviting.", "A pleasant scent of grass and flowers hangs in the air."],
        'event_chance': 0.15,
        'exits': {'w': 'clearing', 'e': 'slope_top'},
        'actions': {
             'l': { # Listen
                'text': "You focus on the sound of water. It seems to be coming from over the crest [E]. It's a {adj_sound} sound.",
                 'description_pools': {'adj_sound': ['gentle', 'soothing', 'faint but clear']},
                 'possible_messages': 'listen_insight',
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
        'description_pools': {
             'adj_view': ['beautiful', 'expansive', 'peaceful', 'hazy but vast'],
             'adj_spring': ['clear', 'bubbling', 'quiet'],
             'rocks': ['mossy rocks', 'smooth grey stones', 'a fissure in the earth'],
             'sight': pool_minor_sights_general + pool_minor_sights_water,
        },
         'dynamic_intro': ["A refreshing breeze blows here.", "The sound of the spring is calming."],
         'event_chance': 0.1,
         'exits': {'w':'gentle_slope_base', 'e': 'valley_view'},
         'actions': {
             'examine spring': {
                 'text': "Kneeling by the spring, the water is {adj_water}, bubbling gently over {pebbles}. Watching the flow is mesmerizing.",
                 'description_pools': {
                     'adj_water': ['crystal clear', 'cool', 'sparkling'],
                     'pebbles': ['smooth pebbles', 'colourful stones', 'dark sand']
                 },
                 'possible_messages': ['Simple beauty.', 'Lost in the gentle motion.', 'A moment of pure presence.'], # Can use inline lists for simple random messages
             },
             'drink': {
                  'text': "You cup your hands and take a sip of the cool, clear water. It tastes {taste}.",
                  'description_pools': {'taste': ['fresh and clean', 'earthy', 'like pure stone']},
                  'message': "Refreshing."
             },
             'b': {
                 'text': "Taking a breath here, feeling the open space around you, brings a sense of {feeling}.",
                  'description_pools': {'feeling': ['calm', 'perspective', 'openness']},
                 'possible_messages': 'breathe_insight',
             }
         }
    },
    'hidden_track_start': {
        'description_template': "Pushing aside a {bush_type} bush reveals a faint, narrow track heading [W]est into a {adj_density} part of the woods. It smells of {scent}. The clearing is back [E].",
        'description_pools': {
            'bush_type': ['flowering', 'thorny', 'dense leafy'],
            'adj_density': ['denser', 'quieter', 'more shadowed'],
            'scent': pool_scents_forest + ['crushed leaves'],
        },
        'dynamic_intro': ["The air here feels still and expectant.", "It's noticeably quieter here than the clearing."],
        'event_chance': 0.3,
        'exits': {'e': 'clearing', 'w': 'ancient_tree'},
        'actions': {
             'f': { # Feel ground
                'text': "You kneel and feel the path. It's {texture}, packed down {firmness}. You notice {detail}.",
                 'description_pools': {
                     'texture': ['soft earth', 'covered in old leaves', 'slightly muddy'],
                     'firmness': ['slightly', 'firmly in places', 'very lightly'],
                     'detail': ['the imprint of a deer hoof', 'a patch of bright green moss', 'nothing much of note']
                 },
                 'possible_messages': 'feel_insight',
             },
             'l': {
                 'text': "Listening... it's very quiet. Just the {sound}.",
                 'description_pools': {'sound': ['faintest whisper of wind', 'distant woods sounds', 'sound of your own quiet breathing']},
                 'possible_messages': 'listen_insight',
             }
        }
    },
    'ancient_tree': {
        'description_template': "The narrow track ends at the base of an enormous, ancient tree. Its bark is {bark_adj}, and branches reach high above. It feels {feeling} here. The track leads back [E]. {sight}",
        'description_pools': {
            'bark_adj': ['deeply furrowed', 'rough and gnarled', 'covered in mosses and lichens'],
            'feeling': ['wise and peaceful', 'solemn and quiet', 'powerfully still', 'timeless'],
            'sight': pool_minor_sights_forest,
        },
         'dynamic_intro': ["Sunlight filters magically through the high canopy.", "The air is cool and still around the great trunk."],
         'event_chance': 0.1,
         'exits': {'e':'hidden_track_start'},
         'actions': {
             'touch tree': {
                 'text': "You place your hand on the {texture} bark. It feels {sensation}, radiating a quiet strength. You feel a connection to its long, slow existence.",
                 'description_pools': {
                     'texture': ['rough, sturdy', 'cool, mossy', 'surprisingly smooth in patches'],
                     'sensation': ['solid and ancient', 'alive yet still', 'calm and reassuring'],
                 },
                 'possible_messages': ['A feeling of deep time and resilience.', 'Grounded by immense stillness.'],
             },
             's': { # Sit
                 'text': "You sit at the base of the tree, leaning against its trunk. The peace here is profound. You simply observe {observation}.",
                 'description_pools': {
                     'observation': ['the light filtering through the leaves', 'tiny insects crawling on the bark', 'the gentle sway of branches far above']
                 },
                 'possible_messages': 'sit_insight',
             },
             'b': {
                'text': "Breathing slowly in the presence of this ancient being feels restorative.",
                'possible_messages': 'breathe_insight',
             }
         }
    },
     'quiet_stream': {
        'description_template': "You've found a small, {adj} stream flowing [E]. The water {sound} over {stones}. Sunlight filters through here, making it less gloomy. {sight}. The path back [S] is clear.",
        'description_pools': {
            'adj': ['quiet', 'clear', 'peaceful', 'chuckling', 'meandering'],
            'sound': pool_sounds_water,
            'stones': ['smooth pebbles', 'mossy rocks', 'flat stones', 'sparkling sand'],
            'sight': pool_minor_sights_water,
        },
        'dynamic_intro': ["The sound of water is soothing here.", "It feels cooler near the stream."],
        'event_chance': 0.15,
        'exits': {'s':'deep_woods', 'e':'stream_bend'},
        'actions': {
            'l': {
                 'text': "Listening only to the stream, the {sound_detail} seems to wash away distraction.",
                 'description_pools': {'sound_detail': ['soft gurgling', 'occasional splash', 'steady flow']},
                 'possible_messages': 'listen_insight',
             },
              'feel water': {
                 'text': "Dipping your fingers in, the water is {temperature}. It feels {sensation}.",
                  'description_pools': {
                      'temperature': ['cool', 'cold', 'surprisingly mild'],
                      'sensation': ['refreshing', 'very real', 'soothing', 'alive']
                  },
                 'possible_messages': 'feel_insight',
             },
             'skip stone': { # Example fun, slightly mindful action
                  'text': "You find a perfectly smooth, flat stone. With a flick of the wrist, you send it skipping across the water... {skips}!",
                  'description_pools': { 'skips': ['once, twice... ploop', 'three satisfying skips!', 'a clumsy splash', 'four, maybe five skips! Wow'] },
                  'message': "A moment of playful focus."
             }
         }
     },
     # --- Placeholder Endings (remain static) ---
     'valley_view': {
        'description': "The view from the cliff edge is breathtaking. Miles of forest stretch out below, bathed in gentle sunlight. You feel a sense of expansive peace wash over you. Maybe the journey wasn't about *reaching* an 'end', but about *how* you walked the path?\n\n[[ You have found a moment of clarity. Thank you for playing! Type 'quit' to exit. ]]",
        'exits': {}, 'actions': {}
     },
      'stream_bend': {
        'description': "The stream bends around a large, mossy rock formation here. The gentle sounds and the constant, steady flow of water bring a sense of calm focus. Perhaps true presence is found not by searching, but by noticing these simple moments, wherever you are?\n\n[[ You have found a moment of flow. Thank you for playing! Type 'quit' to exit. ]]",
        'exits': {}, 'actions': {}
     },
}

# -----------------------------------------------------------------------------
# Validation (Optional but recommended for larger projects)
# You could add code here to automatically check:
# - All destination IDs in exits/reveals exist as keys in `locations`.
# - All pool references in `description_pools` exist in `all_data_pools`.
# -----------------------------------------------------------------------------
print("[game_data.py] Loaded.") # Confirmation message