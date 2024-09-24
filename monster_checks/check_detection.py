def check_for_detection(initial_values):
    detected_characters = []
    spotting_characters = []
    stealth_values = []
    passive_perceptions = []

    # Check for relevant info
    for character, values in initial_values.items():
        if 'current_stealth' in values:
            stealth_values.append((character, values["current_stealth"]))
        if 'passive_perception' in values:
            passive_perceptions.append((character, values["passive_perception"]))

    for name, stealth_number in stealth_values:
        max_perception = max(int(value) for _, value in passive_perceptions) if passive_perceptions else float('inf')
        if int(stealth_number) <= max_perception and len(passive_perceptions) >= 1:
            detected_characters.append(name)

    for name, passive_perception in passive_perceptions:
        min_stealth = min(int(value) for _, value in stealth_values) if stealth_values else float('-inf')
        if int(passive_perception) >= min_stealth and len(stealth_values) >= 1:
            spotting_characters.append(name)

    return detected_characters, spotting_characters

