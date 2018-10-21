import libtcodpy as libtcod

from entity import Entity
from spell_functions import cast_example_enemy_target, cast_magic_missile, cast_arcanic_wall, cast_power_orb, cast_evocation, cast_mass_paralyze

from game_messages import Message

from components.spell import Spell

from systems.targeting import TargetType

from render_functions import RenderOrder
from damage_types import DamageType


def get_spells_list(spell_name):
    spells_list = {
        'example_enemy_target': {
            'spell_name': 'Missile magique',
            'spell_function': cast_example_enemy_target,
            'targeting': TargetType.ENEMY,
            'radius': False,
            'targeting_message': 'Left click on the enemy you want to hit. Right-click or Esc to cancel.',
            'mana_cost': 4,
            'spell_level': 1,
            'power': 2,
            'damage_type': DamageType.ARCANE
        },
        # magic missile random target
        'magic_missile': {
            'spell_name': 'Missile magique',
            'spell_function': cast_magic_missile,
            'targeting': TargetType.CLOSEST_ENTITIES,
            'radius': False,
            'targeting_message': None,
            'mana_cost': 6,
            'spell_level': 2,
            'power': 6,
            'damage_type': DamageType.ARCANE
        },
        # target tile.
        'arcanic_wall': {
            'spell_name': 'Mur arcanique',
            'spell_function': cast_arcanic_wall,
            'targeting': TargetType.TILE,
            'radius': False,
            'targeting_message': 'Target a tile to create an arcanic wall.',
            'mana_cost': 4,
            'spell_level': 1,
            'power': 2,
            'damage_type': DamageType.ARCANE
        },
        'power_orb': {
            'spell_name': 'Orbe de puissance',
            'spell_function': cast_power_orb,
            'targeting': TargetType.TILE_OR_ENTITY,
            'radius': False,
            'targeting_message': 'Target where you want the power orb to go.',
            'mana_cost': 9,
            'spell_level': 3,
            'power': 13,
            'damage_type': DamageType.ARCANE
        },
        'evocation': {
            'spell_name': 'Evocation',
            'spell_function': cast_evocation,
            'targeting': TargetType.SELF,
            'radius': False,
            'targeting_message': None,
            'mana_cost': 9,
            'spell_level': 3,
            'power': 13,
            'damage_type': DamageType.ARCANE
        },
        'mass_paralyze': {
            'spell_name': 'Paralysie de masse',
            'spell_function': cast_mass_paralyze,
            'targeting': TargetType.RADIUS,
            'radius': 3,
            'targeting_message': 'Target the center of your 3x3 tiles spell.',
            'mana_cost': 12,
            'spell_level': 4,
            'power': 24,
            'damage_type': DamageType.ARCANE
        }
    }

    return spells_list[spell_name]


def generate_spell(spell_name, x, y):
    spec_from_spell = get_spells_list(spell_name)

    spell_name = spec_from_spell['spell_name']
    spell_function = spec_from_spell['spell_function']

    targeting = spec_from_spell['targeting']
    radius = spec_from_spell['radius']

    targeting_message = spec_from_spell['targeting_message']
    if targeting_message:
        targeting_message = Message(targeting_message, libtcod.light_blue)

    mana_cost = spec_from_spell['mana_cost']
    spell_level = spec_from_spell['spell_level']
    power = spec_from_spell['power']
    damage_type = spec_from_spell['damage_type']

    spell_component = Spell(spell_function=spell_function, targeting=targeting,
                            targeting_message=targeting_message, mana_cost=mana_cost,
                            spell_level=spell_level, power=power, damage_type=damage_type, radius=radius)
    spell_to_create = Entity(x, y, '.', libtcod.white, spell_name, render_order=RenderOrder.ITEM, spell=spell_component)

    return spell_to_create
