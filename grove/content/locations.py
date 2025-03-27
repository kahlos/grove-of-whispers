# -*- coding: utf-8 -*-
# grove/content/locations.py
# v4: REMOVED 'visual' key. Visuals moved to visuals.py. Added UTF-8 decl.

# NOTE: pools.py needs to exist and be importable for pool references.
# Assume pools like 'adj_calm', 'scent_forest', etc. are defined in pools.py

locations = {
    'clearing': {
        # 'visual': r"""...""" Removed
        'description_template': "You stand in a {adj} clearing. Ancient stones covered in moss form a rough circle in the center. The air is {adj_nature} and carries the scent of {scent}. You notice {sight}. A familiar restlessness urges you to keep moving.",
        'description_pools': { 'adj': 'adj_calm', 'adj_nature': ['still', 'warm', 'gentle'], 'scent': ['wildflowers', 'sun-warmed grass', 'scent_forest'], 'sight': 'sight_forest' },
        'dynamic_intro': ["A gentle breeze rustles the leaves above.", "Sunlight warms your face.", "The quiet feels vast and deep."],
        'audio_mood': 'clearing_calm',
        'event_chance': 0.25,
        'exits': {'n': 'dark_woods_entrance', 'e': 'gentle_slope_base'},
        'actions': {
            's': { 'text': "You settle onto a large, mossy stone. It's {texture} beneath your hand. Focusing on the feeling, the urge to rush quiets. You notice tiny details - {sight_detail}.", 'description_pools': { 'texture': ['cool and damp', 'surprisingly soft', 'rougher than expected'], 'sight_detail': ['dew drops sparkling', 'a ladybug exploring', 'the intricate structure of the moss'] }, 'possible_messages': 'sit_insight', },
            'b': { 'text': "Standing still, you take a slow breath in... and out... Another... And one more... The inner chatter softens slightly.", 'possible_messages': 'breathe_insight', 'possible_reveals': [ {'reveal': {'w': 'hidden_track_start'}, 'message': "Clarity sharpens. You spot a hidden path westward!"}, {'reveal': None, 'message': "You feel calmer, centered."}, {'reveal': None, 'message': "A simple breath."}, ], 'reveal_chance': 0.6 },
            'l': { 'text': "Pausing, you close your eyes to simply listen. The {sound}... and beneath it, a deeper quiet.", 'description_pools': {'sound': 'sound_forest'}, 'possible_messages': 'listen_insight', }
        }
    },
    'dark_woods_entrance': {
        # 'visual': r"""...""" Removed
        'description_template': "The trees grow close here, casting {adj_mood} shadows. The air is cooler, smelling of {scent}. The path ahead [N] looks {adj_light}. Moss hangs heavy. You see {sight} nearby. The clearing [S] is behind you.",
        'description_pools': { 'adj_mood': 'adj_mysterious', 'scent': 'scent_forest', 'adj_light': ['uncertain', 'dark', 'overgrown'], 'sight': 'sight_forest', },
        'dynamic_intro': ["A twig snaps nearby.", "An owl hoots softly, unseen.", "A chill settles briefly."],
        'audio_mood': 'forest_neutral',
        'event_chance': 0.2,
        'exits': {'s': 'clearing', 'n': 'deep_woods'},
        'actions': {
             'f': { 'text': "You reach out to the moss on a branch. It's {texture}, {temperature}. Focusing on the sensation anchors you.", 'description_pools': { 'texture': ['damp', 'surprisingly rough', 'cool and yielding', 'dry and brittle'], 'temperature': ['cold', 'cool', 'clammy'] }, 'possible_messages': 'feel_insight', },
             'b': { 'text': "Breathing consciously, you notice the cool air. Despite the shadows, a measure of calm returns.", 'possible_messages': 'breathe_insight', }
        }
    },
    'deep_woods': {
         # 'visual': r"""...""" Removed
        'description_template': "Deeper in the woods. It's much {adj_light}. It feels {adj_mood} and easy to get lost. Tangled paths twist. You notice {sight}. The way back [S] is faintly visible.",
        'description_pools': { 'adj_light': 'adj_light', 'adj_mood': 'adj_moody', 'sight': 'sight_forest', },
        'audio_mood': 'woods_deep',
        'event_chance': 0.4,
        'exits': {'s': 'dark_woods_entrance'},
        'actions': {
             'b': { 'text': "Focusing on your breath... in... out... The rising {feeling} softens. You feel your feet firmly on the ground.", 'description_pools': { 'feeling': ['panic', 'confusion', 'anxiety', 'sense of being lost'] }, 'possible_messages': 'breathe_insight', 'possible_reveals': [ {'reveal': {'n': 'quiet_stream'}, 'message': "As calm settles, one path northward [N] seems clearer."}, {'reveal': None, 'message': "You feel centered, but paths remain confusing."}, ], 'reveal_chance': 0.7 },
             'o': { 'text': "Acknowledging thoughts ('lost!', 'Which way?') without judgment, like watching {metaphor}. They are just thoughts.", 'description_pools': { 'metaphor': ['clouds pass', 'leaves float by on a stream', 'bubbles rising'] }, 'message': "Observing thoughts creates distance." },
             'l': { 'text': "You stop and listen intently. Only {sound} breaks the deep silence.", 'description_pools': {'sound': ['faint rustling', 'your own heartbeat', 'a distant, unidentifiable noise']}, 'possible_messages': 'listen_insight', }
        }
     },
    'gentle_slope_base': {
        # 'visual': r"""...""" Removed
        'description_template': "A wide, {adj} slope rises gently to the [E]ast. Small, {adj_nature} flowers dot the hillside under the {weather} sky. You can hear faint {sound} from further up. The clearing is back to the [W]est.",
        'description_pools': { 'adj': ['grassy', 'sunlit', 'gentle'], 'adj_nature': 'adj_nature', 'weather': ['warm sun', 'blue sky', 'partly cloudy sky'], 'sound': 'sound_water', },
        'audio_mood': 'clearing_calm',
        'dynamic_intro': ["The warmth here feels inviting.", "A scent of grass and flowers is in the air."],
        'event_chance': 0.15,
        'exits': {'w': 'clearing', 'e': 'slope_top'},
        'actions': {
             'l': { 'text': "You focus on the sound of water from crest [E]. It's {adj_sound}.", 'description_pools': {'adj_sound': ['gentle', 'soothing', 'faint but clear']}, 'possible_messages': 'listen_insight', },
             'examine flowers': { 'text': "Kneeling, you look at tiny wildflowers. Colors {color_detail}, intricate shapes. Simple beauty.", 'description_pools': {'color_detail': ['vibrant blues/yellows', 'delicate whites/pinks', 'deep purples']}, 'message': "Appreciating the small details.", }
        }
    },
    'slope_top': {
        # 'visual': r"""...""" Removed
        'description_template': "You reach the top of the slope. Before you lies a {adj_view} vista overlooking a valley [E]. A small, {adj_spring} spring bubbles from {rocks} here, feeding a stream flowing down. Path back down [W]. You see {sight}.",
        'description_pools': { 'adj_view': ['beautiful', 'expansive', 'peaceful', 'hazy but vast'], 'adj_spring': ['clear', 'bubbling', 'quiet'], 'rocks': ['mossy rocks', 'smooth grey stones', 'a fissure in the earth'], 'sight': ['sight_general', 'sight_water'], },
        'audio_mood': 'stream',
        'dynamic_intro': ["A refreshing breeze blows here.", "The sound of the spring is calming."],
        'event_chance': 0.1,
        'exits': {'w':'gentle_slope_base', 'e': 'valley_view'},
        'actions': {
             'examine spring': { 'text': "Kneeling by the spring, the water is {adj_water}, bubbling over {pebbles}. Mesmerizing.", 'description_pools': { 'adj_water': ['crystal clear', 'cool', 'sparkling'], 'pebbles': ['smooth pebbles', 'colourful stones', 'dark sand'] }, 'possible_messages': ['Simple beauty.', 'Lost in the gentle motion.'], },
             'drink': { 'text': "Cupping your hands, you sip the cool, clear water. It tastes {taste}.", 'description_pools': {'taste': ['fresh and clean', 'earthy', 'like pure stone']}, 'message': "Refreshing." },
             'b': { 'text': "Breathing here, feeling the open space, brings a sense of {feeling}.", 'description_pools': {'feeling': ['calm', 'perspective', 'openness']}, 'possible_messages': 'breathe_insight', }
         }
    },
    'hidden_track_start': {
         # 'visual': r"""...""" Removed
        'description_template': "Pushing aside a {bush_type} bush reveals a faint, narrow track heading [W]est into a {adj_density} part of the woods. It smells of {scent}. The clearing is back [E].",
        'description_pools': { 'bush_type': ['flowering', 'thorny', 'dense leafy'], 'adj_density': ['denser', 'quieter', 'more shadowed'], 'scent': ['scent_forest', 'crushed leaves'], },
        'audio_mood': 'forest_mysterious',
        'dynamic_intro': ["The air feels still and expectant.", "It's noticeably quieter here."],
        'event_chance': 0.3,
        'exits': {'e': 'clearing', 'w': 'ancient_tree'},
        'actions': {
             'f': { 'text': "Kneeling, you feel the path: {texture}, packed {firmness}. You notice {detail}.", 'description_pools': { 'texture': ['soft earth', 'covered leaves', 'slightly muddy'], 'firmness': ['slightly', 'firmly in places', 'very lightly'], 'detail': ['a deer hoof imprint', 'bright green moss', 'nothing of note'] }, 'possible_messages': 'feel_insight', },
             'l': { 'text': "Listening... very quiet. Just the {sound}.", 'description_pools': {'sound': ['faintest wind whisper', 'distant woods sounds', 'your quiet breathing']}, 'possible_messages': 'listen_insight', }
        }
    },
    'ancient_tree': {
        # 'visual': r"""...""" Removed
        'description_template': "The narrow track ends at the base of an enormous, ancient tree. Its bark is {bark_adj}, branches high above. It feels {feeling} here. Back [E]. {sight}",
        'description_pools': { 'bark_adj': ['deeply furrowed', 'rough gnarled', 'mossy lichen-covered'], 'feeling': ['wise peaceful', 'solemn quiet', 'powerfully still', 'timeless'], 'sight': 'sight_forest', },
        'audio_mood': 'forest_mysterious',
        'dynamic_intro': ["Sunlight filters magically through canopy.", "Air cool and still."],
        'event_chance': 0.1,
        'exits': {'e':'hidden_track_start'},
        'actions': {
             'touch tree': { 'text': "Placing hand on {texture} bark. Feels {sensation}, quiet strength. Connects to its long existence.", 'description_pools': { 'texture': ['rough, sturdy', 'cool, mossy', 'smooth patches'], 'sensation': ['solid ancient', 'alive still', 'calm reassuring'], }, 'possible_messages': ['Deep time, resilience.', 'Grounded by stillness.'], },
             's': { 'text': "Sitting at base, against trunk. Peace profound. Observe {observation}.", 'description_pools': { 'observation': ['light through leaves', 'tiny insects on bark', 'gentle branch sway'] }, 'possible_messages': 'sit_insight', },
             'b': { 'text': "Breathing slowly in presence of this ancient being feels restorative.", 'possible_messages': 'breathe_insight', }
         }
    },
     'quiet_stream': {
         # 'visual': r"""...""" Removed
        'description_template': "You've found a small, {adj} stream flowing [E]. Water {sound} over {stones}. Sunlight filters, less gloomy. {sight}. Path back [S].",
        'description_pools': { 'adj': ['quiet', 'clear', 'peaceful', 'chuckling', 'meandering'], 'sound': 'sound_water', 'stones': ['smooth pebbles', 'mossy rocks', 'flat stones', 'sparkling sand'], 'sight': 'sight_water', },
        'audio_mood': 'stream',
        'dynamic_intro': ["Sound of water is soothing.", "Cooler near stream."],
        'event_chance': 0.15,
        'exits': {'s':'deep_woods', 'e':'stream_bend'},
        'actions': {
            'l': { 'text': "Listen only to stream. {sound_detail} wash away distraction.", 'description_pools': {'sound_detail': ['soft gurgling', 'occasional splash', 'steady flow']}, 'possible_messages': 'listen_insight', },
            'feel water': { 'text': "Dip fingers in, water is {temperature}. Feels {sensation}.", 'description_pools': { 'temperature': ['cool', 'cold', 'surprisingly mild'], 'sensation': ['refreshing', 'very real', 'soothing', 'alive'] }, 'possible_messages': 'feel_insight', },
            'skip stone': { 'text': "Find smooth stone. Flick wrist... {skips}!", 'description_pools': { 'skips': ['once, twice.. ploop', '3 satisfying skips!', 'a clumsy splash', '4, maybe 5 skips! Wow'] }, 'message': "Playful focus." }
         }
     },
     # --- Endings ---
     'valley_view': {
          # 'visual': r"""...""" Removed
        'description': "The view from the cliff edge is breathtaking... [[ You have found a moment of clarity. Thank you for playing! Type 'quit' to exit. ]]",
        'audio_mood': 'clearing_calm',
        'exits': {}, 'actions': {}
     },
     'stream_bend': {
         # 'visual': r"""...""" Removed
        'description': "The stream bends around large rock formation... [[ You have found a moment of flow. Thank you for playing! Type 'quit' to exit. ]]",
        'audio_mood': 'stream',
        'exits': {}, 'actions': {}
     },
}

print("[locations.py] v4 Loaded (visuals removed).")