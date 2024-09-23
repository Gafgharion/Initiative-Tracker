import os


# Function to get the file name based on monster type
def get_file_name(monster_type):
    return f"{monster_type.lower()}_status.txt"


# Function to get the file directory based on monster type
def get_file_directory(monster_type):
    file_name = get_file_name(monster_type)
    file_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "monster_status_strings", file_name)
    return file_directory


# Function to fill the status list for a given monster type
def fill_status_lists(status_lists, zahl, line, monster_type):
    if monster_type.lower() not in status_lists:
        # If not, create a new key-value pair with an empty list
        status_lists[monster_type.lower()] = []
    status_lists[monster_type.lower()].append((zahl, f"{line}"))


# Function to read the data from the file and fill the status list
def read_data_file(monster_type, status_lists):
    """Method to read data from the corresponding txt file. The txt file should have
    lines such as 0-20, 20-40, 40-60, 80-100 describing the monster's condition
    based on hitpoints. The strings are stored in the corresponding list.

    Args:
        monster_type (str): Type of the monster (for file lookup)
        status_lists (dict): Dictionary where status strings are stored

    Returns:
        None
    """
    file_directory = get_file_directory(monster_type)

    with open(file_directory, encoding="utf8") as file:
        line = file.readline()
        while line:
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
            if line not in ["0-20", "20-40", "40-60", "60-80", "80-100"]:
                fill_status_lists(status_lists, zahl, line, monster_type)
            line = file.readline()

    file.close()
