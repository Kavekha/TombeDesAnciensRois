import libtcodpy as libtcod

from game_messages import Message
from components.ai import ConfusedMonster, BrainStates


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('power')

    results = []

    print('DEBUG : Caster du Heal Parchemin est ', entity)

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health.', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', libtcod.green)})

    return results


def cast_lightning(*args, **kwargs):
    print('DEBUG : Lightning cast!')
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('power')
    maximum_range = kwargs.get('maximum_range')
    game_map = kwargs.get('game_map')
    damage_type = kwargs.get('damage_type')

    print('DEBUG : lightning : args {} , entities {} , fov map {} , damage {} , max range {} , game map {} , '
          'damagetype {} '.format(caster, entities, fov_map, damage, maximum_range, game_map, damage_type ))

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message(
            'A lightning bolt strikes the {} with a loud thunder! The damage is {}.'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage, caster, game_map, damage_type))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.',
                                                                              libtcod.red)})
    return results


def cast_fireball(*args, **kwargs):
    print('DEBUG : fireball cast!')
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('power')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    game_map = kwargs.get('game_map')
    damage_type = kwargs.get('damage_type')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of vision.', libtcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message('The fireball explodes, burning everything within {} tiles!'.format(radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('The {} getsburned for {} hit points.'.format(entity.name, damage), libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage, caster, game_map, damage_type))

    return results


def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.',
                                                              libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            # v15.
            if entity.ai.state == BrainStates.CONFUSED:

                entity.ai.number_of_turns += 5

                results.append({'consumed': True, 'message': Message(
                    'The eyes of the {} change briefly, then he keep stumbling around!'.format(entity.name),
                    libtcod.light_green)})
            # before v15, no if / else.
            else:
                confused_ai = ConfusedMonster(entity.ai, 10)

                confused_ai.owner = entity
                entity.ai = confused_ai

                results.append({'consumed': True, 'message': Message(
                    'The eyes of the {} look vacant, as he stats to stumble around!'.format(entity.name),
                    libtcod.light_green)})

            break

    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.',
                                                              libtcod.yellow)})

    return results
