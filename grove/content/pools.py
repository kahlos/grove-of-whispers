# grove/content/pools.py
# Defines pools of words/phrases for dynamic content generation.

import random # Good practice, though may not be strictly needed if not combining here

# --- Define individual pool lists ---
pool_adjectives_calm = ["peaceful", "serene", "sun-dappled", "quiet", "still", "tranquil", "hushed"]
# ... (include ALL your pool lists definitions here) ...
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

# --- Define the main dictionary accessing the pools ---
# (Using locals() can be dynamic but less explicit; defining directly is safer)
all_data_pools = {
    "adj_calm": pool_adjectives_calm, "adj_mysterious": pool_adjectives_mysterious,
    "adj_nature": pool_adjectives_nature, "adj_light": pool_adjectives_light,
    "adj_moody": pool_adjectives_moody,
    "scent_forest": pool_scents_forest, "scent_water": pool_scents_water,
    "scent_general": pool_scents_general,
    "sound_forest": pool_sounds_forest, "sound_water": pool_sounds_water,
    "sound_general": pool_sounds_general,
    "sight_forest": pool_minor_sights_forest, "sight_water": pool_minor_sights_water,
    "sight_general": pool_minor_sights_general,
    "events": pool_flavor_events,
    "breathe_insight": pool_breathe_insights, "listen_insight": pool_listen_insights,
    "feel_insight": pool_feel_insights, "sit_insight": pool_sit_insights,
    # Combine pools for convenience
    "sight_any": pool_minor_sights_forest + pool_minor_sights_water + pool_minor_sights_general,
    "scent_any": pool_scents_forest + pool_scents_water + pool_scents_general,
    "sound_any": pool_sounds_forest + pool_sounds_water + pool_sounds_general,
}

# Basic validation
if not isinstance(all_data_pools, dict):
    raise TypeError("all_data_pools did not load correctly as a dictionary.")
if not all_data_pools.get("adj_calm"):
     print("Warning: 'adj_calm' pool might be missing or empty in all_data_pools.")


print("[pools.py] Loaded.")