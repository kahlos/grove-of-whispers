# grove/utils/text_utils.py
import time
import random
import textwrap

def wrap_text(text: str, width: int = 80) -> str:
    """Wraps text for cleaner display."""
    if not isinstance(text, str): # Basic type check for safety
        text = str(text)
    return "\n".join(textwrap.wrap(text, width))

def slow_print(text: str, delay_min: float = 1.5, delay_max: float = 2.5, width: int = 80):
    """Prints text wrapped and with a noticeable pause."""
    print(wrap_text(text, width))
    time.sleep(random.uniform(delay_min, delay_max))

print("[text_utils.py] Loaded.")