# grove/content/dynamics.py
# Functions for dynamically generating text content using templates and pools.

import random
from typing import Dict, Any, Optional, List

# Import data pools (read-only access)
try:
    from .pools import all_data_pools
except ImportError:
    print("Error loading pools in dynamics.py")
    all_data_pools = {}


def _get_random_from_pool(pool_ref: Any, placeholder_name: str = "value") -> str:
    """Internal helper to safely get a random string from a pool reference."""
    chosen_value = f"<{placeholder_name}?#>" # Updated error placeholder

    try:
        if isinstance(pool_ref, str) and pool_ref in all_data_pools:
            pool = all_data_pools[pool_ref]
            if pool and isinstance(pool, list):
                chosen_value = random.choice(pool)
            else:
                # If a pool name is given but it's empty or invalid in all_data_pools
                print(f"[DEBUG] Pool '{pool_ref}' referenced by '{placeholder_name}' is empty/invalid.")
        elif isinstance(pool_ref, list):
            # If an inline list is provided directly in the locations data
            if pool_ref:
                 # Combine logic: Check if elements are pool names or direct strings
                 processed_pool = []
                 for item in pool_ref:
                     if isinstance(item, str) and item in all_data_pools:
                         pool_content = all_data_pools[item]
                         if pool_content and isinstance(pool_content, list):
                              processed_pool.extend(pool_content) # Add all items from referenced pool
                         else:
                             print(f"[DEBUG] Invalid pool '{item}' referenced within list for '{placeholder_name}'.")
                     elif isinstance(item, str):
                          processed_pool.append(item) # Add direct string
                 if processed_pool:
                    chosen_value = random.choice(processed_pool)
            # If pool_ref is an empty list `[]`
            else: chosen_value = ""
        elif isinstance(pool_ref, str):
            # Static string provided directly (not a pool name), use it as is
            chosen_value = pool_ref
        elif pool_ref is None:
            chosen_value = "" # Allow None to mean empty string replacement

    except Exception as e:
        print(f"[DEBUG] Error resolving pool for '{placeholder_name}' (ref: {pool_ref}): {e}")
        # Keep the default error placeholder chosen_value

    # Ensure return is always a string
    return str(chosen_value) if chosen_value is not None else ""


def generate_dynamic_text(template: str, pool_references: Dict[str, Any]) -> str:
    """Generates text by filling a template using specified pools."""
    if not template or not isinstance(template, str):
        return "[Error: Invalid template provided]"

    format_dict = {}
    for placeholder, pool_ref in pool_references.items():
        # Use the internal helper to get the value for the placeholder
        format_dict[placeholder] = _get_random_from_pool(pool_ref, placeholder)

    # Format the template using the resolved values
    try:
        # Using f-string style formatting requires all keys in format_dict
        final_text = template.format(**format_dict)
    except KeyError as e:
        print(f"[DEBUG] Template formatting KeyError: Missing key {e} for template '{template[:50]}...'")
        # Try to format gracefully, replacing only found keys? No standard way.
        # Fallback: Show template with placeholders that caused errors
        final_text = template # Or attempt a more robust substitution later if needed
    except Exception as e:
        print(f"[DEBUG] Unexpected template formatting error: {e}")
        final_text = template

    return final_text

def select_random_outcome(possible_outcomes: Optional[List[Dict[str, Any]]]) -> Optional[Dict[str, Any]]:
    """Selects one outcome dictionary randomly from a list."""
    if possible_outcomes and isinstance(possible_outcomes, list):
        return random.choice(possible_outcomes)
    return None

def generate_event_text(location_data: Dict[str, Any]) -> Optional[str]:
    """Determines if a flavor event occurs and returns its text."""
    event_chance = location_data.get('event_chance', 0)
    if random.random() < event_chance:
        event_pool_ref = location_data.get('possible_events', 'events') # Default to global 'events' pool
        event_text = _get_random_from_pool(event_pool_ref, "event")
        if event_text and event_text != "<event?#>":
            return event_text
    return None


print("[dynamics.py] Loaded.")