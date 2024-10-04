import random
import re


def calculate_health(average_health):
    if average_health.isdigit():
        number = 0
        average_health = int(average_health)
        while number == 0:
            number = random.randint(-1, 1)
            if number < 0:
                health = int(average_health) - int(
                    (average_health / 100) * random.randint(1, 40)
                )
            elif number > 0:
                health = int(average_health) + int(
                    (average_health / 100) * random.randint(1, 40)
                )
    else:
        # Match the pattern for dice rolls and any additional values
        match = re.match(r"(\d+)d(\d+)([+-]\d+)?", average_health)
        if match:
            num_dice = int(match.group(1))
            sides = int(match.group(2))
            additional = int(match.group(3) or 0)  # Default to 0 if not present

            # Roll the dice
            total = sum(random.randint(1, sides) for _ in range(num_dice))
            health = total + additional

        else:
            raise ValueError("Invalid health format.")

    return health
