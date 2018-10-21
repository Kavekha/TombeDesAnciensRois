import libtcodpy as libtcod

from game_messages import Message

from entity import Entity

from components.ai import Obstacle
from render_functions import RenderOrder


def cast_magic_missile(caster, spell_entity, **kwargs):
    caster = caster
    mana_cost = spell_entity.mana_cost
    power = spell_entity.power
    damage_type = spell_entity.damage_type

    target_entity = kwargs.get('target_entity')
    game_map = kwargs.get('game_map')

    damage = caster.fighter.int

    print('DEBUG : Spell is casting')
    results = []

    # list can't be empty there.
    results.append({'mana_cost': mana_cost, 'message': Message('Bolts of energy come out of {} hands!'.
                                                                   format(caster.name), libtcod.blue)})

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

    damage = caster.fighter.int * power

    print('DEBUG : game map is : ', game_map)
    tile = game_map.tiles[target_x][target_y]

    ai_component = Obstacle(tile, entities, damage)
    arcanic_wall = Entity(target_x, target_y, '+', libtcod.darkest_blue, name='Arcanic Wall', blocks=True,
                   render_order=RenderOrder.ACTOR, ai=ai_component)

    entities.append(arcanic_wall)

    results = []

    results.append({'mana_cost': mana_cost, 'message': Message('{} create an arcanic wall to block the way!'.
                                                                   format(caster.name), libtcod.blue)})
    return results


def get_closest_entities(maximum_range, caster, entities, fov_map):

    target_list = []
    for entity in entities:
        if entity.fighter and libtcod.map_is_in_fov(fov_map, entity.x, entity.y) and entity != caster:
            distance = caster.distance_to(entity)
            if distance < maximum_range + 1:
                target_list.append(entity)

    return target_list


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
