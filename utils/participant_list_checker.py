import re


def get_starting_monster_count(monster_name, initial_values):
    """
    Finds the highest monster count for a given monster name from the current participants.
    Returns the starting count for new monsters of the same name.
    """
    current_participants = initial_values.keys()
    list_of_monsters_with_same_name = [
        monster
        for monster in current_participants
        if re.match(rf"{re.escape(monster_name)}\d*$", monster)
        # Matches 'monster_name' followed by optional digits
    ]

    if list_of_monsters_with_same_name:
        return find_highest_monster_count(list_of_monsters_with_same_name)
    return 0


def find_highest_monster_count(list_of_input_strings):
    numbers = []

    # Extract numbers from each string and convert them to integers
    for string in list_of_input_strings:
        found_numbers = re.findall(r"\d+", string)
        if found_numbers:
            numbers.extend(map(int, found_numbers))  # Convert extracted numbers to int

    # Return the maximum number found (or 0 if no numbers found)
    return max(numbers) if numbers else 1
