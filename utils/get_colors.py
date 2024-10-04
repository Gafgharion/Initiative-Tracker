def get_condition_color(status_type):
    # Define the color mappings for damage types and conditions
    damage_colors = {
        "acid": "green",
        "bludgeoning": "gray",
        "cold": "light blue",
        "fire": "red",
        "force": "purple",
        "lightning": "yellow",
        "necrotic": "black",
        "piercing": "gray",
        "poison": "dark green",
        "psychic": "pink",
        "radiant": "white",
        "slashing": "silver",
        "thunder": "yellow",
    }

    condition_colors = {
        "blinded": "dark gray",
        "charmed": "magenta",
        "deafened": "dark blue",
        "frightened": "orange",
        "grappled": "brown",
        "incapacitated": "gray",
        "invisible": "light gray",
        "paralyzed": "cyan",
        "petrified": "dark brown",
        "poisoned": "dark green",
        "prone": "olive",
        "restrained": "dark red",
        "stunned": "silver",
        "unconscious": "black",
    }

    # Convert input to lowercase for case-insensitive comparison
    if isinstance(status_type, str):
        status_type = status_type.lower()

        # Check if the status is a damage type
        if status_type in damage_colors:
            return damage_colors[status_type]

        # Check if the status is a condition
        elif status_type in condition_colors:
            return condition_colors[status_type]

    # If the status doesn't match anything, return None or a default color
    return None
