# -*- coding: utf-8 -*-
# grove/content/locations.py
# v6: Fixed NameErrors by using string keys for pool references.

# NOTE: Assumes all string keys used here (e.g., 'adj_calm', 'trees') exist in pools.all_data_pools

locations = {
    # --- Forest Area ---
    'clearing': {
        'description_template': "Sunlight dapples a {adj} clearing. A circle of ancient, mossy stones rests centrally. Air feels {adj_nature}, scented with {scent}. Nearby, you see {sight}. Restlessness urges movement.",
        # FIX: Use string keys from pools.py
        'description_pools': {'adj':'adj_calm', 'adj_nature':['still','warm','gentle'], 'scent':['wildflowers','sun-warmed grass','scent_forest'], 'sight':'sight_forest'},
        'dynamic_intro': ["Breeze rustles leaves.", "Sunlight warms face.", "Quiet feels vast."], 'audio_mood': 'clearing_calm', 'event_chance': 0.25,
        'exits': {'n': 'dark_woods_entrance', 'e': 'gentle_slope_base'},
        'actions': {
            's': {'text': "Sit on mossy stone, cool and {texture}. Focus on sensation, urge to rush quiets. Notice tiny {detail}.", 'description_pools': {'texture':['damp','soft','rougher'], 'detail':['dew drops','ladybug','moss structure']}, 'possible_messages':'sit_insight'},
            'b': {'text': "Stand still. Slow breath in... out... Again... And again... Inner chatter softens.", 'possible_messages':'breathe_insight', 'possible_reveals':[{'reveal': {'w': 'hidden_track_start'}, 'message':"Clarity sharpens. Spot hidden path [W]!"}, {'reveal':None,'message':"Feel calmer, centered."}],'reveal_chance': 0.6 },
            'l': {'text': "Pause, close eyes. Listen... {sound}... beneath it, deep quiet.", 'description_pools':{'sound':'sound_forest'}, 'possible_messages':'listen_insight'},
            'gaze': {'text':"Soften focus, look broadly at clearing. Take in light, shapes, feeling of space.", 'possible_messages':'gaze_insight'},
        }
    },
    'dark_woods_entrance': {
        'description_template': "Trees grow close, casting {adj_mood} shadows. Air is cooler, smells of {scent}. Path ahead [N] looks {adj_light}. {trees} have heavy moss. {sight} nearby. Clearing back [S].",
        # FIX: Use string keys from pools.py
        'description_pools': {'adj_mood':'adj_mysterious', 'scent':'scent_forest', 'adj_light':['uncertain','dark','overgrown'], 'trees':'trees', 'sight':'sight_forest'},
        'dynamic_intro': ["Twig snaps nearby.", "Owl hoots softly.", "Chill settles briefly."], 'audio_mood': 'forest_neutral', 'event_chance': 0.2,
        'exits': {'s': 'clearing', 'n': 'deep_woods'},
        'actions': {
             'f': {'text':"Reach out, touch hanging moss. It's {texture}, {temperature}. Focusing anchors you.", 'description_pools':{'texture':['damp','rough','cool','yielding','dry brittle'], 'temperature':['cold','cool','clammy']}, 'possible_messages':'feel_insight'},
             'b': {'text':"Conscious breath, notice cool air. Despite shadows, sense of steady calm holds.", 'possible_messages':'breathe_insight'},
             'notice shadows': {'text': "Observe the shifting patterns of light and shadow on the {ground}. Notice how darkness defines light.", 'description_pools': {'ground':'ground'}, 'possible_messages': ["Appreciating contrast.", "Finding stillness in shadow."]},
        }
    },
    'deep_woods': {
        'description_template': "Deeper now. Much {adj_light}. Feels {adj_mood}. Tangled paths twist confusingly among {trees}. Ground is covered in {ground_cover}. {sight}. Path back [S] visible.",
         # FIX: Use string keys from pools.py
         'description_pools': {'adj_light':'adj_light', 'adj_mood':'adj_moody', 'trees':'trees', 'ground_cover':['old leaves','thick moss','pine needles', 'ground'], 'sight':'sight_forest'},
         'audio_mood': 'woods_deep', 'event_chance': 0.4,
         'exits': {'s':'dark_woods_entrance'}, # Exit N revealed by 'b' action
         'actions': {
             'b': {'text':"Focus breath... in... out... Rising {feeling} softens. Feel feet on ground.", 'description_pools':{'feeling':['panic','confusion','anxiety']}, 'possible_messages':'breathe_insight', 'possible_reveals':[{'reveal':{'n':'quiet_stream'}, 'message':"Calm settles. Path [N] seems slightly clearer."}, {'reveal': None, 'message':"Centered, but paths still confusing."}],'reveal_chance': 0.7},
             'o': {'text':"Acknowledge thoughts ('lost!', 'which way?') without judgment, like watching {metaphor}.", 'description_pools':{'metaphor':['clouds','leaves on stream','bubbles']}, 'message': "Observing thoughts creates distance." },
             'l': {'text':"Listen intently. Only {sound} breaks the deep silence.", 'description_pools':{'sound':['faint rustling','own heartbeat','distant noise']}, 'possible_messages':'listen_insight'},
             'feel bark': {'text': "Place hand against rough bark of a {tree_type}. Feels {texture}. Connection to grounded energy.", 'description_pools':{'tree_type':'trees', 'texture':['solid','cool','damp','slightly yielding']}, 'possible_messages':'feel_insight'}
        }
     },
    'quiet_stream': {
        'description_template': "Followed path to a small, {adj} stream flowing [E] over {stones}. {water_sound}. Sunlight filters here. {sight}. Woods back [S].",
        # FIX: Use string keys from pools.py
        'description_pools': {'adj':['quiet','clear','peaceful','chuckling','meandering'], 'stones':'rocks', 'water_sound':'sound_water', 'sight':['sight_water', 'sight_forest']},
        'audio_mood': 'stream', 'dynamic_intro': ["Sound of water soothing.", "Cooler near stream."], 'event_chance': 0.15,
        'exits': {'s':'deep_woods', 'e':'stream_bend'},
        'actions': {
            'l': {'text': "Listen only to stream. {sound_detail} wash away distraction.", 'description_pools': {'sound_detail': ['soft gurgling', 'occasional splash', 'steady flow']}, 'possible_messages':'listen_insight'},
            'feel water': {'text': "Dip fingers in. Water is {temperature}, feels {sensation}.", 'description_pools': {'temperature': ['cool', 'cold', 'mild'], 'sensation': ['refreshing', 'very real', 'soothing', 'alive']}, 'possible_messages':'feel_insight'},
            'skip stone': {'text': "Find smooth, flat stone. Flick wrist... {skips}!", 'description_pools':{'skips':['once, twice.. ploop', '3 satisfying skips!', 'clumsy splash', '4, maybe 5! Wow']}, 'message':"Playful focus."},
            'watch reflections': {'text': "Gaze at water's surface. Sky, trees, light dance. Shifting world, steady flow.", 'possible_messages':'gaze_insight'}
        }
     },
    'stream_bend': {
         'description_template': "Stream bends around {adj} {rock_type}. Sound is {sound_adj}. Leads further [E] or back [W]. Way up rocks [U]?",
         # FIX: Use string keys from pools.py
         'description_pools': {'adj':'adj_nature', 'rock_type':'rocks', 'sound_adj': ['louder here','focused','hypnotic'], },
         'audio_mood': 'stream', 'event_chance': 0.1,
         'exits': {'w':'quiet_stream', 'e':'waterfall_approach', 'u': 'rocky_ascent'},
         'actions': {
             'sit on rock': {'text':"Find dry spot on large rock. Feel solidness beneath. Watch water flow.", 'possible_messages':'sit_insight'},
             'trace patterns': {'text':"Notice patterns moss/lichen make on rock face. Intricate tiny maps. Lose self in details.", 'possible_messages':["Focus narrows.", "Appreciating complexity."]},
             'feel spray': {'text':"Tiny cool spray droplets land on skin. Refreshing focus.", 'possible_messages':'feel_insight'},
         }
    },
     'waterfall_approach': {
        'description_template': "Path nears sound source. A {adj} waterfall cascades down rocks [E]. Air thick with {scent} and mist. Roaring {sound_level}. Back [W].",
        # FIX: Use string keys from pools.py
        'description_pools': {'adj':'adj_water_feature', 'scent':['ozone','damp earth','clean water'], 'sound_level': ['fills the air','is quite loud','resonates deep']},
        'audio_mood': 'stream', 'event_chance': 0.3,
        'exits': {'w':'stream_bend', 'e':'waterfall_base'},
        'actions': {
            'feel mist': {'text': "Fine cool mist dampens face/clothes. Notice sensation, smell ozone. Invigorating.", 'possible_messages':['Awakening sensation.','Cool clarity.']},
            'l': {'text': "Focus on roar. Hear individual tones? Highs and lows within.", 'possible_messages':'listen_insight'},
        }
     },
    'waterfall_base': {
         'description_template': "Base of {adj} waterfall! Water crashes, mist swirls. Deafening {sound_adj}. Ground is {ground_type}. Path behind falls [N]? Retreat [W].",
         # FIX: Use string keys from pools.py
         'description_pools': {'adj': ['thundering', 'powerful', 'magnificent'], 'sound_adj':['sound','roar','energy'], 'ground_type':['slippery rock','muddy','strewn pebbles', 'ground']},
         'audio_mood': 'stream', # Needs specific waterfall mood?
         'event_chance': 0.5,
         'exits': {'w':'waterfall_approach'},
         'actions': {
             'meditate': {'text': "Sit near pool edge, despite roar. Let sound wash through, focus beyond thought.", 'possible_messages': ["Meditating on intensity.", "Finding stillness in chaos."]},
             'feel spray': {'text': "Closer. Mist soaks, wind pushes. Feel nature's power. Raw sensation.", 'possible_messages':'feel_insight'},
             'look behind falls': {'text': "Peer through shimmering veil. See dim opening [N] - passage?", 'reveal': {'n': 'waterfall_cave'}, 'message':"A hidden entrance!"}
         }
    },
    'waterfall_cave': {
         'description_template': "Behind the roar! A {adj} cave, {temp}. Water drips down walls ({cave_detail}). Sound muffled. Damp {scent}. Exit back [S].",
         # FIX: Use string keys from pools.py
         'description_pools': {'adj': 'adj_cave', 'temp':['cool','cold','damp'], 'cave_detail': 'cave_features', 'scent':'scent_cave' },
         'audio_mood': 'woods_deep', # Cave mood?
         'event_chance': 0.2,
         'exits': {'s':'waterfall_base'},
         'actions': {
             'l': {'text':"Listen. Falls are dull roar. Hear {sound} clearly.", 'description_pools':{'sound':['water drips','own breath','faint echoes', 'sound_cave']}, 'possible_messages':'listen_insight'},
             'feel walls': {'text':"Touch cave walls. {texture}, cold. Feel earth enclosing you.", 'description_pools':{'texture':['smooth wet stone','rough minerals','slimy patch']}, 'possible_messages':'feel_insight'},
             'b': {'text':"Breathe cool, damp air deeply. Feels {sensation}.", 'description_pools':{'sensation':['strangely fresh','heavy','mineral-rich']}, 'possible_messages':'breathe_insight'},
         }
    },

    # --- Hidden Track / Ancient Tree Area ---
    'hidden_track_start': {
        'description_template': "Push aside {bush} reveals faint, narrow track [W] into {adj} woods. Smells of {scent}. Clearing back [E].",
        'description_pools': { 'bush':['flowering bush','thorny tangle','dense leaves'], 'adj':['denser','quieter','shadowed'], 'scent':['scent_forest','crushed leaves']},
        'audio_mood': 'forest_mysterious', 'dynamic_intro': ["Air still and expectant.", "Noticeably quieter."], 'event_chance': 0.3,
        'exits': {'e': 'clearing', 'w': 'ancient_tree'},
        'actions': {
             'f': {'text':"Kneel, feel path: {texture}, packed {firmness}. Notice {detail}.", 'description_pools':{'texture':['soft earth','old leaves','muddy patch'], 'firmness':['slightly','firmly','very lightly'], 'detail':['deer hoof imprint','bright green moss','nothing much']}, 'possible_messages':'feel_insight'},
             'l': {'text':"Listen... very quiet. Just {sound}.", 'description_pools':{'sound':['faintest wind','distant forest sounds','own breath', 'sound_forest']}, 'possible_messages':'listen_insight'}
        }
    },
    'ancient_tree': {
        'description_template': "Track ends at enormous, ancient tree. Bark {bark_adj}, branches high. Feels {feeling}. Path back [E]. See {sight}.",
        # FIX: Use string keys from pools.py
        'description_pools': {'bark_adj':['deeply furrowed','rough gnarled','mossy lichen-covered'], 'feeling':['wise peaceful','solemn quiet','powerfully still','timeless'], 'sight':'sight_forest'},
        'audio_mood': 'forest_mysterious', 'dynamic_intro': ["Sunlight filters magically.", "Air cool and still."], 'event_chance': 0.1,
        'exits': {'e':'hidden_track_start'},
        'actions': {
             'touch tree': {'text':"Place hand on {texture} bark. Feels {sensation}, quiet strength. Connects to its long existence.", 'description_pools':{'texture':['rough sturdy','cool mossy','smooth patches'], 'sensation':['solid ancient','alive yet still','calm reassuring']}, 'possible_messages':['Deep time.','Grounded by stillness.']},
             's': {'text':"Sit at base, against trunk. Peace profound. Observe {observation}.", 'description_pools':{'observation':['light through leaves','tiny insects on bark','gentle branch sway']}, 'possible_messages':'sit_insight'},
             'b': {'text':"Breathe slowly here. Feels restorative.", 'possible_messages':'breathe_insight'},
             'look up': {'text': "Crane neck, gaze up at immense canopy spreading against sky. Awe.", 'possible_messages': 'gaze_insight'}
         }
    },

    # --- Slope / Height Area ---
    'gentle_slope_base': {
        'description_template': "Wide, {adj} slope rises [E]. {adj_nature} flowers dot hillside under {weather} sky. Hear faint {sound} from above. Clearing back [W].",
        # FIX: Use string keys from pools.py
        'description_pools': { 'adj': ['grassy', 'sunlit', 'gentle'], 'adj_nature': 'adj_nature', 'weather': ['warm sun', 'blue sky', 'partly cloudy sky'], 'sound': 'sound_water' },
        'audio_mood': 'clearing_calm', 'dynamic_intro': ["Warmth inviting.", "Scent of grass, flowers."], 'event_chance': 0.15,
        'exits': {'w': 'clearing', 'e': 'slope_top'},
        'actions': { 'l': { 'text': "Focus on water sound from crest [E]. It's {adj_sound}.", 'description_pools': {'adj_sound': ['gentle', 'soothing', 'faint']}, 'possible_messages':'listen_insight'}, 'examine flowers': { 'text': "Kneel, look closely. Colors {color}, shapes intricate. Simple beauty.", 'description_pools': {'color':['vibrant blues/yellows','delicate whites/pinks','deep purples']}, 'message':"Appreciating details."}, }
    },
    'slope_top': {
        'description_template': "Top of slope. {adj_view} vista over valley [E]. Small, {adj_spring} spring bubbles from {rocks}, feeds stream. Path down [W]. Steep rocks up [U]. See {sight}.",
        # FIX: Use string keys from pools.py
        'description_pools': { 'adj_view': ['beautiful', 'expansive', 'peaceful', 'hazy'], 'adj_spring': ['clear', 'bubbling', 'quiet'], 'rocks': 'rocks', 'sight': ['sight_general', 'sight_water'] },
        'audio_mood': 'stream', 'dynamic_intro': ["Refreshing breeze.", "Sound of spring calming."], 'event_chance': 0.1,
        'exits': {'w':'gentle_slope_base', 'e': 'valley_view', 'u': 'rocky_ascent'},
        'actions': { 'examine spring': { 'text': "Kneel by spring. Water {adj_water}, bubbles over {pebbles}. Mesmerizing.", 'description_pools': { 'adj_water': ['crystal clear', 'cool', 'sparkling'], 'pebbles': ['smooth pebbles', 'colourful stones', 'dark sand'] }, 'possible_messages': ['Simple beauty.', 'Lost in gentle motion.'], }, 'drink': { 'text': "Cup hands, sip cool clear water. Tastes {taste}.", 'description_pools': {'taste': ['fresh clean', 'earthy', 'like pure stone']}, 'message': "Refreshing." }, 'b': { 'text': "Breathe, feeling open space. Sense of {feeling}.", 'description_pools': {'feeling': ['calm', 'perspective', 'openness']}, 'possible_messages':'breathe_insight', }, 'gaze valley': {'text':"Look out over valley. Soften eyes, taking in whole vista without focus.", 'possible_messages':'gaze_insight'}, }
    },
     'rocky_ascent': {
         'description_template': "Steep climb on {adj_rocks}. Path {path_adj}. Careful steps needed. Down [D]. Further up [U]? Feels {adj_height}.",
         # FIX: Use string keys from pools.py
         'description_pools': {'adj_rocks': 'rocks', 'path_adj':['narrow','treacherous','faintly marked'], 'adj_height':'adj_height'},
         'audio_mood': 'forest_neutral', # Maybe 'height' mood?
         'event_chance': 0.3, 'dynamic_intro': ["Wind whistles past.", "Loose stone shifts.", "View getting wider."],
         'exits': {'d':'slope_top', 'u': 'high_peak'},
         'actions': {
             'feel footing': {'text': "Pause. Focus on feet connecting with rock. Find solid hold. Assess balance.", 'possible_messages':['Grounding awareness.', 'Mindful movement needed.']},
             'check breath': {'text': "Notice breath, likely quicker from exertion. Deepen slightly. Observe body.", 'possible_messages':'breathe_insight'},
             'look down': {'text':"Carefully glance down. Steep drop. Brief jolt, then focus on path.", 'possible_messages':["Presence required.", "Acknowledge fear, focus action."]}
         }
     },
    'high_peak': {
        'description_template': "Wind whips this exposed summit! {view_adj} panorama unfolds. Clouds {cloud_pos}. {peak_detail}. Only way down [D].",
        # FIX: Use string keys from pools.py
        'description_pools': {'view_adj':['Incredible','Breathtaking','Endless','Cloud-level'], 'cloud_pos':['below','nearby','like islands in sky'], 'peak_detail':'peak_features'},
        'audio_mood': 'clearing_calm', # 'height' mood needed
        'event_chance': 0.6, 'dynamic_intro': ["Wind howls.", "Feel very small.", "Sense of vast space."],
        'exits': {'d': 'rocky_ascent'},
        'actions': {
             's': {'text': "Find sheltered spot behind rocks. Sit, absorb vastness. Feel wind, sun. Just be.", 'possible_messages':'sit_insight'},
             'b': {'text':"Breathe thin, clean air. Fill lungs. Exhale fully. Feel alive, awake.", 'possible_messages':'breathe_insight'},
             'feel wind': {'text': "Face wind. Feel force, coolness, sound. Unwavering presence against power.", 'possible_messages':'feel_insight'},
             'shout': {'text':"Deep breath, shout into wind! Sound whipped away instantly. Release.", 'message': "Ephemeral expression."}
         }
     },

     # --- Endings ---
     'valley_view': {
        'description': "The view from cliff edge is breathtaking... [[ Found clarity. Thank you! Type 'quit' ]]",
        'audio_mood': 'clearing_calm', 'exits': {}, 'actions': {}
     },
     # No visual keys in end locations
}

print("[locations.py] v6 Loaded (Expanded, pool keys fixed).")