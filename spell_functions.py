import libtcodpy as libtcod

from game_messages import Message


def cast_magic_missile(caster, spell_entity, **kwargs):
    caster = caster
    mana_cost = spell_entity.mana_cost
    power = spell_entity.power
    damage_type = spell_entity.damage_type

    target_entity = kwargs.get('target_entity')
    game_map = kwargs.get('game_map')

    # power = kwargs.get('power')
    # damage_type = kwargs.get('damage_type')
    #mana_cost = kwargs.get('mana_cost')

    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    damage = power * caster.fighter.int

    results.append({'mana_cost': mana_cost, 'message': Message('Sort de magic missile!', libtcod.light_blue)})
    results.extend(target_entity.fighter.take_damage(damage, caster, game_map, damage_type))

    return results
