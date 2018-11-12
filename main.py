import libtcodpy as libtcod

from imput_handlers import handle_main_menu, handle_score_bill_menu, \
    handle_character_creation_menu, handle_load_menu

from loader_functions.initialize_new_game import get_game_variables
from loader_functions.data_loaders import load_game, get_saved_games
from loader_functions.initialize_new_game import get_constants, create_player

from menus import main_menu, message_box, score_bill_menu, character_creation_menu, menu

from game_states import GameStates

from engine import play_game


def main():
    constants = get_constants()

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

    main_screen(constants)


def main_screen(constants):
    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False
    show_score_bill = False
    show_creation_menu = False
    show_load_menu = False

    character_name = str("")
    main_menu_background_image = libtcod.image_load('menu_background.png')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(con, main_menu_background_image, constants['screen_width'], constants['screen_height'],
                      constants['version'])

            if show_load_error_message:
                message_box(con, 'No save game to load', 50, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            score_bill = action.get('score_bill')
            exit_game = action.get('exit')
            fullscreen = action.get('fullscreen')

            if fullscreen:
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False

            elif new_game:
                # v14.
                show_main_menu = False
                show_creation_menu = True

            elif load_saved_game:
                # v15
                if show_load_menu == False:
                    number_of_games = get_saved_games()
                    if number_of_games == []:
                        show_load_error_message = True
                    else:
                        show_main_menu = False
                        show_load_menu = True

            # v14
            elif score_bill:
                show_main_menu = False
                show_score_bill = True

            elif exit_game:
                break

        # v15
        elif show_load_menu:
            number_of_games = get_saved_games()
            header = 'Choose your save :'
            '''
            menu(con, header, number_of_games, int(constants['screen_width'] / 2), constants['screen_width'],
                 constants['screen_height'])
            '''
            menu(con, header, number_of_games, int(constants['screen_width'] / 2), constants['screen_width'],
                 constants['screen_height'])

            libtcod.console_flush()

            action = handle_load_menu(key)

            load_chosen = action.get('load_chosen')
            load_exit = action.get('load_exit')

            if load_exit:
                show_main_menu = True
                show_load_menu = False

            if load_chosen != None:
                try:
                    save_to_load = number_of_games[load_chosen]
                    player, entities, game_map, message_log, game_state = load_game(save_to_load)
                    show_main_menu = False
                    show_creation_menu = False
                    show_score_bill = False
                    show_load_menu = False

                except FileNotFoundError:
                    show_load_error_message = True

        # v14
        elif show_creation_menu:
            character_creation_menu(main_menu_background_image, constants['screen_width'],
                                      constants['screen_height'], character_name)

            libtcod.console_flush()

            action = handle_character_creation_menu(key)

            exit_creation = action.get('exit_creation')
            validate_creation = action.get('validate_creation')
            letter = action.get('letter')

            if letter == 'backspace':
                if len(character_name) > 0:
                    character_name = character_name[:-1]

            if letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-']:
                if len(character_name) < 10:
                    character_name += str(letter)

            if validate_creation:
                if len(character_name) == 0:
                    character_name = 'Player'

                show_creation_menu = False
                player = create_player("warrior")
                entities, game_map, message_log, game_state = get_game_variables(constants, player)
                player.name = character_name
                game_state = GameStates.PLAYERS_TURN

            if exit_creation:
                show_creation_menu = False
                show_main_menu = True

        # v14
        elif show_score_bill:
            # show score bill.
            score_bill_menu(main_menu_background_image, constants['screen_width'],
                            constants['screen_height'])

            libtcod.console_flush()

            action = handle_score_bill_menu(key)
            exit_score_bill = action.get('score_exit')

            if exit_score_bill:
                show_score_bill = False
                show_main_menu = True

        else:
            libtcod.console_clear(con)
            play_game(player, entities, game_map, message_log, game_state, con, panel, constants)

            show_main_menu = True


if __name__ == '__main__':
    main()
