import libtcodpy as libtcod
from game_messages import Message

from enum import Enum


class TargetType(Enum):
    SELF = 0
    ENEMY = 1
    ALLIED = 2
    RADIUS = 3
    TILE = 4
    CLOSEST_ENTITIES = 5
    TILE_OR_ENTITY = 6


def spell_targeting_resolution(targeting_obj, target_mode, player, game_map, fov_map, entities, left_click,
                               right_click):

    #targeting_obj : entity with spell or item component. The spell we want to cast or item we want to use.

    results = []

    print('INFO targeting result. Targeting obj is ', targeting_obj.name)

    target_entity = None
    target_x = None
    target_y = None

    if not target_mode:
        results.append({'message': Message('ERROR : No targeting system for {}'.format(targeting_obj.name),
                                           libtcod.yellow)})
        target_entity = False

    elif target_mode:

        if target_mode == TargetType.CLOSEST_ENTITIES:
            # nearest entitites.
            # maximum_range = (targeting_obj.power + int(player.fighter.int / 2))
            maximum_range = 12

            target_entity = get_closest_entities(maximum_range, player, entities, fov_map)

            if not target_entity:

                # results.append({'message': Message('No target around can be hit with  {}'.format(
                    # targeting_obj.name), libtcod.yellow)})
                target_entity = False

        elif target_mode == TargetType.SELF:
            # caster as target.
            target_entity = player

            if not target_entity:
                # results.append({'message': Message('ERROR : should be the caster, but doesnt work.'.format(
                    # targeting_obj.name), libtcod.yellow)})
                target_entity = False

        # elif asking for coords from mouse left click
        elif left_click:
            target_x, target_y = left_click

            if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
                # results.append({'message': Message('You cannot target something outside your field of view.',
                #                            libtcod.yellow)})
                target_entity = False

            else:

                # Tile or entity : since we just care for FoV, no check are necessary.
                if target_mode == TargetType.TILE_OR_ENTITY:
                    target_entity = game_map.tiles[target_x][target_y]

                # looking for a tile.
                if target_mode == TargetType.TILE:
                    for entity in entities:
                        if entity.x == target_x and entity.y == target_y:
                            # results.append({'message': Message('There is someone there, no action can be done '
                            #                                 'on this tile.', libtcod.yellow)})
                            target_entity = False
                            break
                    else:
                        target_entity = game_map.tiles[target_x][target_y]

                # Looking for an Entity fighter.
                if target_mode in (TargetType.ENEMY, TargetType.ALLIED):

                    for entity in entities:
                        if entity.x == target_x and entity.y == target_y and entity.fighter:
                            target_entity = entity
                            break

                    else:
                        # results.append({'message': Message('You have to target someone.', libtcod.yellow)})
                        target_entity = False

                if target_mode == TargetType.RADIUS:

                    radius = 3
                    if targeting_obj.spell:
                        radius = targeting_obj.spell.radius
                    elif targeting_obj.item:
                        radius = targeting_obj.item.radius

                    entity_list = []

                    for entity in entities:
                        if entity.distance(target_x, target_y) <= radius and entity.fighter:
                            entity_list.append(entity)

                    target_entity = entity_list

                    if target_entity == []:
                        # Else, radius targeting will never end if no target.
                        # Not great, since it will help check invisible creatures if there were.
                        target_entity = False


        elif right_click:
            target_entity = False

        else:
            # waiting for left or right click.
            pass

    else:
        # results.append({'message': Message('ERROR : Existing target mode, but no results for {}'.format(
            # targeting_obj.name), libtcod.yellow)})
        target_entity = False

    # for all target mode, we wait for a can be cast True to cast. If false: Cancel. Else, wait for action.
    if target_entity:

        print('INFO : targeting, if target entity, targeting obj is ', targeting_obj)

        return target_entity
        # results.extend(spell_use_results)

    # Not target_entity given, still waiting to receive one.
    elif target_entity == False:
        print('DEBUG : no target entity :', target_entity)
        # results.append({'targeting_cancelled': True})
        return False

    else:
        # still waiting to receive a target.
        pass


def get_closest_entities(maximum_range, caster, entities, fov_map):

    target_list = []
    for entity in entities:
        if entity.fighter and libtcod.map_is_in_fov(fov_map, entity.x, entity.y) and entity != caster:
            distance = caster.distance_to(entity)
            if distance < maximum_range + 1:
                target_list.append(entity)

    return target_list
