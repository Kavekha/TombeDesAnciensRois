import libtcodpy as libtcod

from death_functions import kill_monster, kill_player

from systems.targeting import spell_targeting_resolution

from entity import get_blocking_entities_at_location

from fov_functions import initialize_fov, recompute_fov

from game_messages import Message
from game_states import GameStates
from imput_handlers import handle_keys, handle_mouse


from loader_functions.data_loaders import save_game

from loader_functions.scores_loader import create_score_bill

from render_functions import clear_all, render_all


def play_game(player, entities, game_map, message_log, game_state, con, panel, constants):
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    previous_game_state = None
    item_or_spell_targeting = None
    target_mode = None
    victory = False

    if game_state != GameStates.VICTORY and game_state != GameStates.PLAYER_DEAD:    # v14 Fix immortal at reload dead
        # before v14, those two were inverted.
        previous_game_state = game_state
        game_state = GameStates.PLAYERS_TURN

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

        show_spellbook = action.get('spellbook')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        spellbook_index = action.get('spellbook_index')

        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        # PLAYER TURN
        player_turn_results = []

        # Exit, full screen
        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN,
                              GameStates.SHOW_SPELLBOOK):
                game_state = previous_game_state
            elif game_state in (GameStates.TARGETING, GameStates.SPELL_TARGETING):
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state)
                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # PLAYER MOVE
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

        # PlAYER TAKE STAIRS.
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

        # PLAYER DOESNT ACT.
        elif wait:
            game_state = GameStates.ENEMY_TURN

        # PLAYER PICKUP ITEM.
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        # SPELLBOOK & SPELL & TARGETING
        if show_spellbook:
            previous_game_state = game_state
            game_state = GameStates.SHOW_SPELLBOOK

        # INVENTORY AND ITEM USE
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        # DROP ITEM
        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        # IF PLAYER HAS CHOSEN SOME ITEM TO DROP/ USE FROM INVENTORY OR A SPELL FROM SPELLBOOK
        if spellbook_index is not None or inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD:

            if spellbook_index is not None and spellbook_index < len(player.spellbook.spells):
                spell_or_item_to_use = player.spellbook.spells[spellbook_index]

            elif inventory_index is not None and inventory_index < len(player.inventory.items):
                spell_or_item_to_use = player.inventory.items[inventory_index]
                print('DEBUG : item at inventory index is : ', spell_or_item_to_use)
            else:
                print('Inventory index : ', inventory_index)
                print('spellbook index : ', spellbook_index)
                print('inventory index len : ', len(player.inventory.items))
                print('spellbook len ; ', len(player.spellbook.spells))
                print('WARNING : action required from Spellbook or inventory, case not supported!!')
                break

            # object : spell or item we want to use

            # CAN THE SPELL BE CASTED?
            if game_state == GameStates.SHOW_SPELLBOOK:
                # since its spellbook, we know object is spell
                if spell_or_item_to_use.spell.mana_cost > player.fighter.mana:
                    message_log.add_message(
                        Message('Not enough mana to cast {}'.format(spell_or_item_to_use.name), libtcod.yellow))
                else:
                    # on recoit à la fin "spell_entity" qui est spell_or_item_to_use + .spell et le targeting_mode.
                    print('INFO : In SHOW SPELLBOOK, spelloritem is ', spell_or_item_to_use)
                    player_turn_results.extend(
                        player.spellbook.cast_spell(spell_or_item_to_use, entities=entities, fov_map=fov_map,
                                                    to_cast=spell_or_item_to_use.spell.to_cast,
                                                    game_map=game_map))
                    print('INFO : We cast some spell ')

            # ARE WE USING AN ITEM?
            if game_state == GameStates.SHOW_INVENTORY:
                print('DEBUG : spell or item to use is : ', spell_or_item_to_use)
                player_turn_results.extend(player.inventory.use(spell_or_item_to_use, entities=entities, fov_map=fov_map))

            # ARE WE DROPING AN ITEM?
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(spell_or_item_to_use))

        # WE HAVE NOW AN item_or_spell_targeting, through the player_turn results of spell.use / item.use
        if game_state == GameStates.SPELL_TARGETING:

            target_entities = spell_targeting_resolution(item_or_spell_targeting, target_mode, player, game_map, fov_map,
                                                           entities, left_click, right_click)

            # objectif a lancer.

            # spell_use_results = spell_targeting_resolution(item_or_spell_targeting, target_mode, player, game_map, fov_map,
            #                                               entities, action, left_click, right_click)

            if target_entities:
                if left_click:
                    target_x, target_y = left_click
                else:
                    target_x, target_y = None, None

                print('BEFORE cast true : target entities is ', target_entities)
                print('INFO : item_or_spell targeting ', item_or_spell_targeting)
                if item_or_spell_targeting.spell:
                    spell_use_results = player.spellbook.cast_spell(item_or_spell_targeting,
                                                                    mana_cost=item_or_spell_targeting.spell.mana_cost,
                                                                    entities=entities, target_x=target_x,
                                                                    target_y=target_y,
                                                                    target_entity=target_entities,
                                                                    to_cast=True, game_map=game_map)
                    player_turn_results.extend(spell_use_results)

                elif item_or_spell_targeting.item:
                    spell_use_results = player.inventory.use(item_or_spell_targeting, entities=entities,
                                                             target_x=target_x, target_y=target_y,
                                                             target_entity=target_entities, to_cast=True,
                                                             game_map=game_map)

                    player_turn_results.extend(spell_use_results)

            elif target_entities is None:
                pass

            elif not target_entities:
                player_turn_results.append({'targeting_cancelled': True})

            else:
                print('Else in target entities, spell targeting. Should not happen.')

        # CHARAC SCREEN
        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            if level_up == 'str':
                player.fighter.base_str += 1
            if level_up == 'dex':
                player.fighter.base_dex += 1

            game_state = previous_game_state

        # PlAYER ACTION RESULTS AND RESOLUTION.
        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            # v16 spellbook.
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            # v16 type of targeting. Receive spell entity and target type.
            spell_targeting = player_turn_result.get('spell_targeting')
            mana_cost = player_turn_result.get('mana_cost')
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting cancelled'))

            # XP GAIN BY PLAYER, LEVEL UP.
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

                message_log.add_message(message)

            # SPELL RESOLUTION.
            if mana_cost:
                print('DEBUG : mana cost about to be paid')
                player.fighter.mana -= mana_cost

                game_state = GameStates.ENEMY_TURN
                print('DEBUG mana cost paid, enemy turn')


            # v16
            if spell_targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.SPELL_TARGETING

                item_or_spell_targeting = spell_targeting['spell']
                target_mode = spell_targeting['target_mode']

                print('DEBUG : Item or spell targeting is : ', item_or_spell_targeting)
                print('DEBUG : Item or spell targeting owner is : ', item_or_spell_targeting.name)
                if item_or_spell_targeting.spell:
                    if item_or_spell_targeting.spell.targeting_message:
                        message_log.add_message(item_or_spell_targeting.spell.targeting_message)
                elif item_or_spell_targeting.item:
                    if item_or_spell_targeting.item.targeting_message:
                        message_log.add_message(item_or_spell_targeting.item.targeting_message)

                '''
                # v16 : msg if no targeting obj message.
                if item_or_spell_targeting.spell.targeting_message:
                    message_log.add_message(item_or_spell_targeting.spell.targeting_message)
                '''

            # ITEM RESOLUTION.
            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                player.inventory.remove_item(item_consumed, 1)
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

        # ENEMY TURN.
        if game_state == GameStates.ENEMY_TURN:
            # FOR EACH ENTITY WITH AI.
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

                            # v15 'or' to fix victory message not displayed, and player action possible.
                            if game_state == GameStates.PLAYER_DEAD or game_state == GameStates.VICTORY:
                                break

                    # v15 fix victory displayed
                    if game_state == GameStates.PLAYER_DEAD or game_state == GameStates.VICTORY:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN
                # NOT WORKING, TO REDO.
                # v16 ally
                for entity in entities:
                    if entity.ai and entity.ally:
                        player_turn_results.extend(entity.ai.take_turn(player, fov_map, game_map, entities))

        # v14 victory condition.
        if game_state == GameStates.VICTORY and not victory:
            victory = True
            create_score_bill(player, game_map.dungeon_level, 'VICTORY', game_map.name)  # v14


