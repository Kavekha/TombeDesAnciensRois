from random import randint


def from_dungeon_level(table, dungeon_level):
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value
    return 0


def random_choice_index(chances):
    print('DEBUG : random choice index : chances ', chances)
    if sum(chances) == 0:
        print('None return')
        return None

    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    print('DEBUG: random choice frm dict, choice : {}, chance : {}'.format(choices, chances))

    random_chance = random_choice_index(chances)
    if random_chance == None:
       to_return = None
    else:
        to_return = choices[random_chance]

    print('DEBUG : random choice from dict, to return : ', to_return)
    return to_return
