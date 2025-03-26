# grove/presentation/intro.py
# Contains the game's introduction sequence.

import time # Only needed if using direct time.sleep, prefer slow_print
from ..utils.text_utils import slow_print

def introduction():
    """Displays the introductory text and integrated tutorial."""
    print("\n" * 2)
    slow_print("...")
    slow_print("Your mind feels... scattered. Like leaves caught in a whirlwind.")
    slow_print("Thoughts race, plans tangle, memories flicker without focus.")
    slow_print("You don't know how you got here, but...")
    slow_print("...here you are.")
    # time.sleep(1.0) # Let slow_print handle pauses
    slow_print("Welcome to The Grove of Whispers.", delay_min=1.0, delay_max=1.5)

    print("\n" + "-" * 30 + "\n")

    slow_print("This place is... different. It seems to respond not just to your steps, but to your attention.", delay_max=2.8)
    slow_print("Moving around is simple. Type commands like 'N', 'S', 'E', 'W' when you see exits listed like [N] North.", delay_max=2.8)
    slow_print("But rushing forward might not always reveal the clearest path.", delay_max=3.0)

    print("\n" + "-" * 30 + "\n")

    slow_print("Sometimes, the Grove invites you to pause. You might see options like:")
    # time.sleep(0.5) # Let slow_print handle pauses
    slow_print("`[B] Breathe` - A reminder to take a conscious breath. Try it now, even just one. In... and out. Notice how the Grove responds when you choose this in the game.", delay_max=3.5)
    # time.sleep(0.8)
    slow_print("`[L] Listen` - Focus only on the sounds described. What details emerge when you truly pay attention?", delay_max=3.0)
    # time.sleep(0.8)
    slow_print("`[F] Feel` - Ground yourself in the sensations of touch described. The texture of moss, the coolness of water, the earth beneath your feet.", delay_max=3.5)
    # time.sleep(0.8)
    slow_print("`[S] Sit` or `[Stillness]` - Sometimes, simply being still and observing reveals more than movement.", delay_max=3.0)
    # time.sleep(0.8)
    slow_print("Other actions might appear too, like `[Examine Flowers]` or `[Touch Tree]`. Use the text in the brackets as your command. Type it exactly.", delay_max=3.5)

    print("\n" + "-" * 30 + "\n")

    slow_print("There is no 'winning' here in the usual sense. The journey *is* the purpose.", delay_max=3.0)
    slow_print("Pay attention. Be present. See what unfolds.", delay_max=2.5)
    # time.sleep(0.5)
    slow_print("If you ever wish to leave the Grove, simply type 'Quit'.")

    print("\n" + "-" * 30 + "\n")
    # Consider using a simple input loop if Enter isn't pressed
    input_text = input("Press Enter when you are ready to begin...")
    # Could add loop: while input_text: input_text = input(...)

print("[intro.py] Loaded.")