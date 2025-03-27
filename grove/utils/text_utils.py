# grove/utils/text_utils.py
# v2: slow_print now skips delay in debug mode.

import time
import random
import textwrap
from typing import Optional

# Import config for debug flag
try:
    from .. import config
except ImportError:
    # Dummy config for standalone testing or import issues
    class config: DEBUG = False

def wrap_text(text: str, width: int = 80) -> str:
    """Wraps text for cleaner display."""
    if not isinstance(text, str): # Basic type check
        text = str(text)
    return "\n".join(textwrap.wrap(text, width))

def slow_print(text: str, delay_min: float = 1.5, delay_max: float = 2.5, width: int = 80):
    """Prints text wrapped. Pauses unless config.DEBUG is True."""
    print(wrap_text(text, width))
    # *** Skip delay if in debug mode ***
    if not config.DEBUG:
        time.sleep(random.uniform(delay_min, delay_max))

# Added a simple conditional sleep utility
def conditional_sleep(duration_min: float, duration_max: Optional[float] = None):
    """Sleeps for a random duration within range, unless config.DEBUG is True."""
    if not config.DEBUG:
        sleep_time = random.uniform(duration_min, duration_max if duration_max else duration_min)
        time.sleep(sleep_time)

print(f"[text_utils.py] Loaded (DEBUG={config.DEBUG})")