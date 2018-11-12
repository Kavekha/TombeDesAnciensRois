import libtcodpy as libtcod

from game_messages import Message
from components.ai import ModifiedMindMonster, BrainStates


def gain_mana(caster, item_entity, **kwargs):
    entity = caster
    amount = item_entity.item.power

    results = []

    if entity.fighter.mana == entity.fighter.max_mana:
        results.append({'targeting_cancelled': True, 'message': Message('You are already at full mana.',
                                                                        libtcod.yellow)})
    else:
        entity.fighter.gain_mana(amount)
        results.append({'consumed': item_entity, 'message': Message('You feel more connected to the energies of the world '
                                                             'than ever!', libtcod.green)})

    return results


def heal(caster, item_entity, **kwargs):
    entity = caster
    amount = item_entity.item.power


    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'targeting_cancelled': True, 'message': Message('You are already at full health.',
                                                                        libtcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': item_entity, 'message': Message('Your wounds start to feel better!', libtcod.green)})

    return results


def cast_lightning(caster, item_entity, **kwargs):
    caster = caster
    damage = item_entity.item.power
    game_map = kwargs.get('game_map')
    damage_type = item_entity.item.damage_type
    target_list = kwargs.get('target_entity')

    results = []

    for target in target_list:
        results.append({'consumed': item_entity, 'target': target, 'message': Message(
                        'A lightning bolt strikes the {} with a loud thunder!'.format(target.name), libtcod.orange)})
        results.extend(target.fighter.take_damage(damage, caster, game_map, damage_type))
        break

    return results


def cast_fireball(caster, item_entity, **kwargs):
    caster = caster
    damage = item_entity.item.power
    radius = item_entity.item.radius
    game_map = kwargs.get('game_map')
    damage_type = kwargs.get('damage_type')

    target_list = kwargs.get('target_entity')

    results = []

    results.append({'consumed': item_entity, 'message': Message('The fireball explodes, burning everything within {} tiles!'.
                                                         format(radius), libtcod.orange)})

    if target_list:
        for entity in target_list:
            results.append({'message': Message('The {} gets burned for {} hit points.'.format(entity.name, damage),
                                               libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage, caster, game_map, damage_type))


    return results


def cast_confuse(caster, item_entity, **kwargs):
    caster = caster
    power = item_entity.item.power

    target_entity = kwargs.get('target_entity')


    results = []

    print('DEBUG : item cast confuse caster is : ', caster.name)
    duration = power + caster.fighter.int

    if target_entity.ai:
        if target_entity.ai.state == BrainStates.CONFUSED:

            target_entity.ai.number_of_turns += int(duration / 2)

            results.append({'consumed': item_entity, 'message': Message(
                'The eyes of the {} change briefly, then he keep stumbling around!'.format(target_entity.name),
                libtcod.light_green)})
            # before v15, no if / else.
        else:
            confused_ai = ModifiedMindMonster(target_entity.ai, duration)

            confused_ai.owner = target_entity
            target_entity.ai = confused_ai

            results.append({'consumed': item_entity, 'message': Message(
                'The eyes of the {} look vacant, as he stats to stumble around!'.format(target_entity.name),
                libtcod.light_green)})

    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.',
                                                              libtcod.yellow)})

    return results
