import libtcodpy as libtcod

from death_functions import kill_monster, kill_player
from components.death import Death

from entity import get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message
from game_states import GameStates
from imput_handlers import handle_keys, handle_mouse, handle_main_menu, handle_score_bill_menu, \
    handle_character_creation_menu, handle_load_menu

from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import save_game, load_game, get_saved_games

from loader_functions.scores_loader import create_score_bill

from render_functions import clear_all, render_all
from menus import main_menu, message_box, score_bill_menu, character_creation_menu, menu


def main():
    constants = get_constants()

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

    main_screen(constants)


def main_screen(constants):
    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

    print('DEBUG : MAIN SCREEN')
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

                    '''
                    try:
                        player, entities, game_map, message_log, game_state = load_game()
                        show_main_menu = False
                    except FileNotFoundError:
                        show_load_error_message = True
                    '''

            # v14
            elif score_bill:
                show_main_menu = False
                show_score_bill = True

            elif exit_game:
                break

        # v15
        elif show_load_menu:
            number_of_games = get_saved_games()
            print('INFO : number of games : ', number_of_games)
            header = 'Choose your save :'
            menu(con, header, number_of_games, int(constants['screen_width'] / 2), constants['screen_width'],
                 constants['screen_height'])

            libtcod.console_flush()

            action = handle_load_menu(key)

            load_chosen = None
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

            if letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '-']:
                if len(character_name) < 10:
                    character_name += str(letter)

            if validate_creation:
                if len(character_name) == 0:
                    character_name = 'Player'

                show_creation_menu = False
                player, entities, game_map, message_log, game_state = get_game_variables(constants)
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


def play_game(player, entities, game_map, message_log, game_state, con, panel, constants):
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    if game_state != GameStates.VICTORY and game_state != GameStates.PLAYER_DEAD:    # v14 Fix immortal at reload dead
        # before v14, those two were inverted.
        previous_game_state = game_state
        game_state = GameStates.PLAYERS_TURN

    targeting_item = None

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['bar_width'],
                   constants['panel_height'], constants['panel_y'], mouse, constants['colors'], game_state)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        wait = action.get('wait')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target, game_map)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        elif wait:
            game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < \
                len(player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
            else:
                message_log.add_message(Message('There are no stairs here.', libtcod.yellow))

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            if level_up == 'str':
                player.fighter.base_str += 1
            if level_up == 'dex':
                player.fighter.base_dex += 1

            game_state = previous_game_state

        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state)
                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting cancelled'))

            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(Message('You gain {} experience points.'.format(xp)))

                if leveled_up:
                    message_log.add_message(Message('Your battle skills grow stronger! You reached level {}'.format(
                        player.level.current_level) + '!', libtcod.yellow))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

            if dead_entity:

                # v14.
                if dead_entity.death.death_function:
                    message, game_state = dead_entity.death.death_function(dead_entity, game_state)

                '''
                # death methode before v14.
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)
                '''

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

            if equip:
                equip_results = player.equipment.toggle_equip(equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        message_log.add_message(Message('You equipped the {}.'.format(equipped.name)))

                    if dequipped:
                        message_log.add_message(Message('You dequipped the {}.'.format(dequipped.name)))

                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state
                message_log.add_message(Message('Targeting cancelled'))

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity, game_state)
                            else:
                                message = kill_monster(dead_entity, game_state)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN

        # v14 victory condition.
        if game_state == GameStates.VICTORY:
            score_created = False
            if not score_created:
                create_score_bill(player, game_map.dungeon_level, 'VICTORY', game_map.version)  # v14
                game_state = GameStates.PLAYER_DEAD


if __name__ == '__main__':
    main()
