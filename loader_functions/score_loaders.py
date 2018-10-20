#file created in v14

import datetime
import os

def create_score_bill(player, dungeon_level, killer, version):

    if not os.path.isfile('scores'):
        print('DEBUG : no score file. Creating one.')
        with open('scores', 'w') as score_file:
            score_file.write('Player name, Level, Killed by, Floor, Date, Game version \n')

    player_name = str(player.name)
    player_level = str(player.level.current_level)
    dungeon_level = str(dungeon_level)
    date = str(datetime.date.today())
    game_version = str(version)
    killed_by = str(killer.name)

    with open('scores', 'a') as score_file:
        score_file.write(player_name + ',' + player_level + ',' + killed_by + ',' + dungeon_level + ',' + date
                         + ',' + game_version + '\n')


def read_score_bill():
    with open('scores', 'r') as score_file:
        print(score_file.readlines())
