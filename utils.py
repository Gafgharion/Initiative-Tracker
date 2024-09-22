import os


def get_file_name(monster_type):
    return f"{monster_type.lower()}_status.txt"


def get_file_directory(monster_type):
    file_name = get_file_name(monster_type)
    return os.path.join(os.path.dirname(__file__), "monster_status_strings", file_name)


def fill_status_lists(status_lists, zahl, line, monster_type):
    if monster_type.lower() not in status_lists:
        status_lists[monster_type.lower()] = []

    status_lists[monster_type.lower()].append((zahl, line))


def read_data_file(status_lists, monster_type):
    """Method to read in data from the corresponding txt file for the monster_type.
    The txt file should contain lines indicating hitpoint ranges.
    These lines are used to fill the status lists for the monster.

    Args:
        status_lists (dict): A dictionary to hold status lists for each monster type.
        monster_type (str): The type of monster being processed.

    Returns:
        None
    """
    file_path = get_file_directory(monster_type)

    with open(file_path, encoding="utf8") as file:
        for line in file:
            line = line.strip()
            if "0-20" in line:
                zahl = 0
            elif "20-40" in line:
                zahl = 20
            elif "40-60" in line:
                zahl = 40
            elif "60-80" in line:
                zahl = 60
            elif "80-100" in line:
                zahl = 80
            else:
                # Only add lines that are not ranges
                if line not in ["0-20", "20-40", "40-60", "60-80", "80-100"]:
                    fill_status_lists(status_lists, zahl, line, monster_type)
