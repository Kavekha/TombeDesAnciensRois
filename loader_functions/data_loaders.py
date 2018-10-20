import shelve
import os


def save_game(player, entities, game_map, message_log, game_state):
    print('DEBUG : save_game')
    with shelve.open('savegame', 'n') as data_file:
        print('DEBUG : shelve open save')
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state

    print('DEBUG : Saved end')


def load_game():
    print('DEBUG : load function started')
    if not os.path.isfile('savegame.dat'):
        print('DEBUG : file not found')
        raise FileNotFoundError

    print('DEBUG: there is a file, keep reading')
    with shelve.open('savegame', 'r') as data_file:
        print('DEBUG : shelve open')
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']

    player = entities[player_index]

    return player, entities, game_map, message_log, game_state
