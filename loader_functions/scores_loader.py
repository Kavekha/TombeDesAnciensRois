# file created in v14

import datetime
import os


def create_score_bill(player, dungeon_level, killer, version):

    if not os.path.isfile('scores'):
        print('DEBUG : no score file. Creating one.')
        with open('scores.txt', 'w') as score_file:
            score_file.write('Player name, Level, Status, Floor, Date, Game version \n')

    player_name = str(player.name)
    player_level = str(player.level.current_level)
    dungeon_level = str(dungeon_level)
    date = str(datetime.date.today())
    game_version = str(version)

    # Deal with VICTORY instead of Killed by.
    if type(killer) == str:
        status = killer # Victory
    else:
        status = str('Killed by ' + killer.owner.name)

    remove_older_scores('scores')

    with open('scores', 'a') as score_file:
        score_file.write(player_name + ',' + player_level + ',' + status + ',' + dungeon_level + ',' + date
                         + ',' + game_version + '\n')


def remove_older_scores(file):
    print('DEBUG : remove older scores')
    with open(file, 'r') as score_file:
        lines = score_file.readlines()

    print('DEBUG : lines in remove older scores : ', lines)

    nb_lines = 0

    for line in lines:
        nb_lines += 1

    print('DEBUG : nb_lines : ', nb_lines)
    nb_to_delete = 0

    if nb_lines >= 30:
        nb_to_delete = nb_lines - 29
    print('DEBUG : nb to delete ', nb_to_delete)

    header_to_copy = True

    with open(file, 'w') as score_file:
        for line_to_copy in lines:
            if header_to_copy:
                score_file.write(line_to_copy)
                header_to_copy = False
                print('DEBUG : first line kept')
            elif nb_to_delete > 0:
                nb_to_delete -= 1
                print('This line wont be kept : ', line_to_copy)
            else:
                score_file.write(line_to_copy)


def read_score_bill():
    if not os.path.isfile('scores'):
        print('DEBUG : no score file. Creating one.')
        with open('scores', 'w') as score_file:
            score_file.write('Player name, Level, Status, Floor, Date, Game version \n')

    with open('scores', 'r') as score_file:
        scores = score_file.readlines()

    return scores
