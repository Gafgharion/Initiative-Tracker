import random
def get_random_status_string(health_percentage, type):
    type = type.lower()
    # print( "SO sieht gerade das dictionary aus:", self.status_lists)
    # print("This is the type:", type)
    liste = self.status_lists[type]
    # print(f"Dies ist in der Liste: {self.status_lists[type]}")
    # print ("Dis ist in der Liste:", liste)
    if health_percentage >= 80:
        number = random.randint(
            sum(1 for tuple in liste if tuple[0] == 0 or tuple[0] == 20 or tuple[0] == 40 or tuple[0] == 60), sum(
                1 for tuple in liste if
                tuple[0] == 0 or tuple[0] == 20 or tuple[0] == 40 or tuple[0] == 60 or tuple[0] == 80) - 1)
        health_status = liste[number][1]
        color = "chartreuse4"


    elif health_percentage >= 60 and health_percentage < 80:
        number = random.randint(sum(1 for tuple in liste if tuple[0] == 0 or tuple[0] == 20 or tuple[0] == 40), sum(
            1 for tuple in liste if tuple[0] == 0 or tuple[0] == 20 or tuple[0] == 40 or tuple[0] == 60) - 1)
        health_status = liste[number][1]
        color = "chartreuse1"


    elif health_percentage >= 40 and health_percentage < 60:
        number = random.randint(sum(1 for tuple in liste if tuple[0] == 20 or tuple[0] == 0),
                                sum(1 for tuple in liste if tuple[0] == 0 or tuple[0] == 20 or tuple[0] == 40) - 1)
        health_status = liste[number][1]
        color = "orange"


    elif health_percentage >= 20 and health_percentage < 40:
        number = random.randint(sum(1 for tuple in liste if tuple[0] == 0),
                                sum(1 for tuple in liste if tuple[0] == 20 or tuple[0] == 0) - 1)
        health_status = liste[number][1]
        color = "firebrick1"


    elif health_percentage >= 0 and health_percentage < 20:
        number = random.randint(0, sum(1 for tuple in liste if tuple[0] == 0) - 1)
        health_status = liste[number][1]
        color = "firebrick4"

    # self.display_passive_perception()

    return health_status, color
    # TODO: FUnktion schreiben