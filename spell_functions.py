import libtcodpy as libtcod

from game_messages import Message

from entity import Entity

from components.ai import Obstacle, MovingItem
from render_functions import RenderOrder


def cast_power_orb(caster, spell_entity, **kwargs):
    caster = caster
    mana_cost = spell_entity.mana_cost
    power = spell_entity.power
    damage_type = spell_entity.damage_type
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    entities = kwargs.get('entities')
    game_map = kwargs.get('game_map')

    results = []

    ai_component = MovingItem(caster, power, damage_type, target_x, target_y, entities)
    power_orb = Entity(caster.x, caster.y, '&', libtcod.darkest_blue, name='Orb of power', blocks=False,
                      render_order=RenderOrder.ACTOR, ai=ai_component, ally=True)

    entities.append(power_orb)

    results.append({'mana_cost': mana_cost, 'message': Message('{} launches an orb of power !'.
                                                                   format(caster.name), libtcod.light_blue)})
    return results


def cast_mass_paralyze(caster, spell_entity, **kwargs):
    caster = caster
    mana_cost = spell_entity.mana_cost
    power = spell_entity.power
    target_entity = kwargs.get('target_entity')

    results = []

    results.append({'mana_cost': mana_cost, 'message': Message('{} unleach a massive paralyzing energy!'.
                                                                   format(caster.name), libtcod.light_blue)})

    paralyze_duration = power + caster.fighter.int

    count = len(target_entity)

    if count > 0:
        paralyze_duration = int(paralyze_duration / count)
        for entity in target_entity:
            if entity != caster and entity.ai and entity.fighter:
                results.extend(entity.fighter.get_paralyzed(caster, paralyze_duration))



    return results


def cast_evocation(caster, spell_entity, **kwargs):
    caster = caster
    mana_cost = spell_entity.mana_cost
    power = spell_entity.power

    results = []

    if caster.fighter.hp == caster.fighter.max_hp:
        results.append({'message': Message('Already at full heal.', libtcod.yellow)})
        results.append({'targeting_cancelled': True})
    else:
        heal_effect = power + caster.fighter.int
        print('power is {} and int is {}'.format(power, caster.fighter.int))
        print('Heal effect is : {}, mana is {} '.format(heal_effect, caster.fighter.mana))
        caster.fighter.hp += heal_effect

        if caster.fighter.hp > caster.fighter.max_hp:
            caster.fighter.hp = caster.fighter.max_hp

        results.append({'mana_cost': mana_cost, 'message': Message('{} regenerates through mana!!'.
                                                                   format(caster.name), libtcod.light_blue)})

    return results


def cast_magic_missile(caster, spell_entity, **kwargs):
    caster = caster
    mana_cost = spell_entity.mana_cost
    power = spell_entity.power
    damage_type = spell_entity.damage_type

    target_entity = kwargs.get('target_entity')
    game_map = kwargs.get('game_map')

    damage = caster.fighter.int

    results = []

    # list can't be empty there.
    results.append({'mana_cost': mana_cost, 'message': Message('Bolts of energy come out of {} hands!'.
                                                                   format(caster.name), libtcod.light_blue)})

    count = power
    for target in target_entity:
        if count > 0:
            results.extend(target.fighter.take_damage(damage, caster, game_map, damage_type))
            count -= 1
        else:
            break

    return results


def cast_arcanic_wall(caster, spell_entity, **kwargs):
    caster = caster
    mana_cost = spell_entity.mana_cost
    power = spell_entity.power
    damage_type = spell_entity.damage_type

    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')
    game_map = kwargs.get('game_map')
    entities = kwargs.get('entities')
    target_entity = kwargs.get('target_entity')

    damage = caster.fighter.int * power

    print('DEBUG : game map is : ', game_map)
    tile = target_entity

    ai_component = Obstacle(tile, entities, damage)
    arcanic_wall = Entity(target_x, target_y, '+', libtcod.darkest_blue, name='Arcanic Wall', blocks=True,
                   render_order=RenderOrder.ACTOR, ai=ai_component)

    entities.append(arcanic_wall)

    results = []

    results.append({'mana_cost': mana_cost, 'message': Message('{} create an arcanic wall to block the way!'.
                                                                   format(caster.name), libtcod.light_blue)})
    return results


def cast_example_enemy_target(caster, spell_entity, **kwargs):
    caster = caster
    mana_cost = spell_entity.mana_cost
    power = spell_entity.power
    damage_type = spell_entity.damage_type

    target_entity = kwargs.get('target_entity')
    game_map = kwargs.get('game_map')

    #entities = kwargs.get('entities')
    #fov_map = kwargs.get('fov_map')
    #radius = kwargs.get('radius')
    #target_x = kwargs.get('target_x')
    #target_y = kwargs.get('target_y')

    results = []

    damage = power * caster.fighter.int

    results.append({'mana_cost': mana_cost, 'message': Message('Sort de magic missile!', libtcod.light_blue)})
    results.extend(target_entity.fighter.take_damage(damage, caster, game_map, damage_type))

    return results
