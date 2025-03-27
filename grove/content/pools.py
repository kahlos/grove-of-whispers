# grove/content/pools.py
# v3: Added 'trees' key to all_data_pools dictionary.

import random

# --- Adjectives ---
pool_adjectives_calm = ["peaceful", "serene", "sun-dappled", "quiet", "still", "tranquil", "hushed", "gentle", "restful"]
pool_adjectives_mysterious = ["mysterious", "enigmatic", "shadowy", "misty", "ancient-feeling", "whispering", "half-hidden", "secretive"]
pool_adjectives_nature = ["verdant", "lush", "overgrown", "wild", "moss-covered", "flower-dotted", "damp", "earthy", "gnarled"]
pool_adjectives_light = ['dim', 'shadow-filled', 'darker', 'gloomy', 'dusky', 'filtered', 'bright', 'dazzling', 'soft']
pool_adjectives_moody = ['confusing', 'disorienting', 'overgrown', 'suffocatingly quiet', 'lonely', 'forgotten', 'melancholy', 'brooding']
pool_adjectives_cave = ["damp", "cool", "echoing", "dark", "still", "mineral-streaked", "close", "confined", "hollow"]
pool_adjectives_height = ["wind-swept", "exposed", "high", "airy", "vast", "distant", "precipitous", "invigorating"]
pool_adjectives_water_feature = ["roaring", "cascading", "misty", "bubbling", "clear", "murmuring", "rushing", "deep"]

# --- Nouns (Features) ---
pool_rocks = ['mossy rocks', 'smooth grey stones', 'a fissure in the earth', 'lichen-covered boulders', 'sharp granite', 'weathered limestone']
pool_trees = ['ancient oak', 'slender birch', 'towering pine', 'twisted hawthorn', 'weeping willow'] # Defined List
pool_ground = ['soft earth', 'packed dirt', 'fallen leaves', 'pine needles', 'uneven stone', 'slippery moss', 'muddy patch']
pool_water_details = ['smooth pebbles', 'colourful stones', 'dark sand', 'swirling eddies', 'patches of foam', 'reflections']
pool_cave_features = ['stalactites', 'stalagmites', 'flowstone', 'mineral deposits', 'dark crevices', 'puddles', 'loose scree']
pool_peak_features = ['sharp crags', 'a windswept cairn', 'distant mountains', 'clouds below', 'a circling bird of prey']

# --- Sensory Details ---
pool_scents_forest = ["pine needles", "damp earth", "moss", "cool air", "flowering blossoms", "wet stone", "fallen leaves", "wild herbs"]
pool_scents_water = ["clean water", "river mud", "wet rocks", "ozone", "water lilies", "damp moss", "faint fish smell"]
pool_scents_cave = ["damp stone", "mineral tang", "mustiness", "cool, still air", "earth", "absence of scent"]
pool_scents_height = ["clean thin air", "ozone", "distant pines", "dry rock", "faint scent of altitude"]
pool_scents_general = ["fresh air", "distant rain", 'petrichor', "sun-baked earth", "wildflowers", "crushed grass"]

pool_sounds_forest = ["rustling leaves", "distant bird calls", "buzzing insects", "a snapping twig", "deep silence", "wind sighing", "squirrel chattering", "woodpecker tapping"]
pool_sounds_water = ["gurgling water", "gentle lapping", "distant cascade", "croaking frogs", "splashing", "water dripping", "steady roar", "rushing torrent"]
pool_sounds_cave = ["dripping water", "deep silence", "faint echoes", "your own footsteps", "scraping stone", "whispering draft"]
pool_sounds_height = ["howling wind", "distant bird cries", "silence", "your own heartbeat", "faint rustling from below"]
pool_sounds_general = ["faint wind", "utter silence", "your own breathing", "heart beating", "a buzzing insect nearby"]

# --- Minor Features / Observations ---
pool_minor_sights_forest = [ "a vibrant patch of fungus", "an intricate spiderweb", "an unusually shaped leaf", "a shy creature watching briefly", "shifting sunlight patterns", "a twisted branch", "animal tracks", "a woodpecker hole", "tiny wildflowers", "a fallen log covered in moss", "a bird's nest high above", "smooth river stones near a path", ]
pool_minor_sights_water = [ "sky reflection on water", "colourful pebbles beneath", "a small fish darting away", "water striders", "sparkling ripples", "a dragonfly hovering", "foam near the bank", "a kingfisher perched momentarily", "waterlogged branch", ]
pool_minor_sights_cave = [ "a glistening patch on the wall", "strangely shaped rock formations", "tiny roots emerging from a crack", "an old, dried fungus", "patterns left by water flow", "a deeper shadow suggesting a side passage", "shimmering mineral veins", ]
pool_minor_sights_height = [ "a hawk soaring on updrafts", "patterns of fields far below", "shadows of clouds racing across land", "tiny, hardy alpine flowers", "a weathered trigonometric point", "the curve of the horizon", "distant signs of settlement (smoke?)", ]
pool_minor_sights_general = ["a strangely shaped cloud", "texture of ground beneath you", "a single feather", "an unusual insect", "the way light catches dust motes"]

# --- Flavor Events ---
pool_flavor_events = [ "A sudden gust of wind rustles everything, then fades.", "You hear a distinct bird call, then silence.", "A strangely coloured butterfly flits past.", "A fleeting, unidentifiable sweet fragrance.", "The quality of light changes subtly.", "A brief, tingling static sensation.", "A faint echo whispers just out of hearing.", "A single leaf spirals down before you.", "A small stone skitters down nearby.", "You briefly feel a sense of being watched, then it passes.", "A cloud perfectly mimics an animal shape for a moment.", ]

# --- Insightful Messages for Actions ---
pool_breathe_insights = [ "With the breath, a layer of mental fog lifts.", "You feel more grounded, present in your body.", "The breath anchors you to this moment.", "A sense of simple okay-ness arises.", "Each breath is a fresh start.", "Noticing the subtle movement of breath.", "The world seems slightly sharper after the pause.", "A quiet space opens within.", ]
pool_listen_insights = [ "The world seems richer, layered with sound.", "You distinguish a sound unnoticed before.", "The silence between sounds becomes profound.", "Focusing on sound quiets internal chatter.", "Listening connects you to the environment.", "Sounds become pure sensation, without labels.", "You notice the direction and distance of different sounds.", ]
pool_feel_insights = [ "Physical sensation brings you sharply into the present.", "Grounding through touch reduces drift.", "Appreciating the simple reality of the physical.", "Touch is an anchor in the now.", "Noticing temperature, texture, weight without judgment.", "The world feels more solid.", ]
pool_sit_insights = [ "Simply sitting and observing, stillness arises.", "The urge to *do* fades slightly.", "Noticing constant small movements in the 'still' world.", "There is peace in non-doing.", "Thoughts come and go like clouds.", "Resting in simple awareness.", ]
pool_observe_insights = [ "Watching thoughts without judgment creates distance.", "Thoughts are just mental events, not reality.", "Recognizing patterns in thought without entanglement.", "Letting thoughts pass without reaction.", ]
pool_gaze_insights = [ "Gazing softens focus, allowing the whole scene in.", "A sense of spaciousness arises.", "Appreciating color, light, and form without fixation.", "Lost in simple observation.", ]


# --- Dictionary of All Pools (for easy reference) ---
all_data_pools = {
    # Adjectives
    "adj_calm": pool_adjectives_calm, "adj_mysterious": pool_adjectives_mysterious,
    "adj_nature": pool_adjectives_nature, "adj_light": pool_adjectives_light,
    "adj_moody": pool_adjectives_moody, "adj_cave": pool_adjectives_cave,
    "adj_height": pool_adjectives_height, "adj_water_feature": pool_adjectives_water_feature,
    # Nouns / Features
    "rocks": pool_rocks,
    "trees": pool_trees, # *** ADDED KEY FOR pool_trees list ***
    "ground": pool_ground,
    "water_details": pool_water_details, "cave_features": pool_cave_features,
    "peak_features": pool_peak_features,
    # Sensory
    "scent_forest": pool_scents_forest, "scent_water": pool_scents_water,
    "scent_cave": pool_scents_cave, "scent_height": pool_scents_height,
    "scent_general": pool_scents_general,
    "sound_forest": pool_sounds_forest, "sound_water": pool_sounds_water,
    "sound_cave": pool_sounds_cave, "sound_height": pool_sounds_height,
    "sound_general": pool_sounds_general,
    # Sights
    "sight_forest": pool_minor_sights_forest, "sight_water": pool_minor_sights_water,
    "sight_cave": pool_minor_sights_cave, "sight_height": pool_minor_sights_height,
    "sight_general": pool_minor_sights_general,
    # Events
    "events": pool_flavor_events,
    # Insights
    "breathe_insight": pool_breathe_insights, "listen_insight": pool_listen_insights,
    "feel_insight": pool_feel_insights, "sit_insight": pool_sit_insights,
    "observe_insight": pool_observe_insights, "gaze_insight": pool_gaze_insights,
    # Combined convenience pools
    "sight_any": pool_minor_sights_forest + pool_minor_sights_water + pool_minor_sights_cave + pool_minor_sights_height + pool_minor_sights_general,
    "sound_any": pool_sounds_forest + pool_sounds_water + pool_sounds_cave + pool_sounds_height + pool_sounds_general,
    "scent_any": pool_scents_forest + pool_scents_water + pool_scents_cave + pool_scents_height + pool_scents_general,
}

print(f"[pools.py] v3 Loaded ({len(all_data_pools)} pool categories).")