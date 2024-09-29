import random


def roll_stealth(participant, initial_values, refresh_callback):
    # Determine the stealth modifier
    attributes = initial_values.get(participant)
    if attributes["skills"]:
        if attributes["skills"]["Stealth"]:
            stealth_modifier = attributes.get("skills", {}).get("Stealth")
    else:
        stealth_modifier = attributes.get("dex_modifier", 0)


    # Roll a d20 and calculate the stealth value
    stealth_value = random.randint(1, 20) + int(stealth_modifier)

    # Update the initial_values dictionary with the new stealth value
    initial_values[participant]["current_stealth"] = stealth_value  # Add or update the stealth value

    refresh_callback()
    return stealth_value