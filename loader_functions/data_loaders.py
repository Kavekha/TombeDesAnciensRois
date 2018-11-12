import shelve
import os


def save_game(player, entities, game_map, message_log, game_state):
    # v15 Named save
    file_name = './saves/' + player.name + '_savegame'

    with shelve.open(file_name, 'n') as data_file:
        print('DEBUG : shelve open save')
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state


def load_game(save_to_load):
    print('DEBUG : load function started')
    print('INFO : save_to_load received : ', save_to_load)
    save_file = './saves/' + save_to_load
    print('INFO : save file renamed : ', save_file)

    if not os.path.isfile(save_file):
        print('DEBUG : file not found')
        raise FileNotFoundError

    nb_of_char_in_save_name = len(save_file)
    save_file = save_file[:(nb_of_char_in_save_name - 4)]

    print('INFO : save file without date : ', save_file)
    print('INFO: there is a file, keep reading')

    with shelve.open(save_file, 'r') as data_file:
        print('DEBUG : shelve open')
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state


# v15
def get_saved_games():
    count = 0
    names_in_file = []
    for file in os.listdir('./saves/'):
        if file.endswith('_savegame.dat'):
            names_in_file.append(file)
            count += 1

    return names_in_file
