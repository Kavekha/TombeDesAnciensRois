from random import randint


def from_dungeon_level(table, dungeon_level):
    print('DEBUG : from dungeon level {} : table : {}'.format(dungeon_level, table))
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value
    return 0


def random_choice_index(chances):
    print('DEBUG : chances from random choice index : {}'.format(chances))
    random_chance = randint(1, sum(chances))
    print('DEBUG : randomchoiceindex : random chance = {}'.format(random_chance))

    running_sum = 0
    choice = 0
    for w in chances:
        print('DEBUG : w in loop random choice index : {}'.format(w))
        running_sum += w
        print('DEBUG : running sum : {}'.format(running_sum))

        if random_chance <= running_sum:
            print('DEBUG : random chance {} <= running sum {}, return choice : {}'.format(random_chance, running_sum, choice))
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    print('DEBUG : random_choice_fromdict : choice dict : {}'.format(choice_dict))
    choices = list(choice_dict.keys())
    print('DEBUG : random choice dict : choices : {}'.format(choices))
    chances = list(choice_dict.values())
    print('DEBUG : random choice from dict : chances : {}'.format(chances))

    to_return = choices[random_choice_index(chances)]
    print('DEBUG : rand choice from dict : RETURN : choices rand choice index chances : {}'.format(to_return))
    return to_return
