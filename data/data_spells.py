import libtcodpy as libtcod

from entity import Entity
from spell_functions import cast_example_enemy_target, cast_magic_missile, cast_arcanic_wall

from game_messages import Message

from components.spell import Spell
from components.spellbook import TargetType

from render_functions import RenderOrder
from damage_types import DamageType

def get_spells_list(spell_name):
    spells_list = {
        'example_enemy_target': {
            'spell_name': 'Missile magique',
            'spell_function': cast_example_enemy_target,
            'targeting': TargetType.ENEMY,
            'targeting_message': 'Left click on the enemy you want to hit. Right-click or Esc to cancel.',
            'mana_cost': 4,
            'spell_level': 1,
            'power': 1,
            'damage_type': DamageType.ARCANE,
            'to_cast': False
        },
        # magic missile random target
        'magic_missile': {
            'spell_name': 'Missile magique',
            'spell_function': cast_magic_missile,
            'targeting': TargetType.CLOSEST_ENTITIES,
            'targeting_message': None,
            'mana_cost': 6,
            'spell_level': 2,
            'power': 3,
            'damage_type': DamageType.ARCANE,
            'to_cast': False
        },
        # target tile.
        'arcanic_wall': {
            'spell_name': 'Mur arcanique',
            'spell_function': cast_arcanic_wall,
            'targeting': TargetType.TILE,
            'targeting_message': 'Target a tile to create an arcanic wall.',
            'mana_cost': 4,
            'spell_level': 1,
            'power': 1,
            'damage_type': DamageType.ARCANE,
            'to_cast': False
        }
    }

    return spells_list[spell_name]


def generate_spell(spell_name: object, x: object, y: object) -> object:
    spec_from_spell = get_spells_list(spell_name)

    spell_name = spec_from_spell['spell_name']
    spell_function = spec_from_spell['spell_function']
    targeting = spec_from_spell['targeting']

    targeting_message = spec_from_spell['targeting_message']
    if targeting_message:
        targeting_message = Message(targeting_message, libtcod.light_blue)

    mana_cost = spec_from_spell['mana_cost']
    spell_level = spec_from_spell['spell_level']
    power = spec_from_spell['power']
    damage_type = spec_from_spell['damage_type']
    to_cast = spec_from_spell['to_cast']

    spell_component = Spell(spell_function=spell_function, targeting=targeting,
                            targeting_message=targeting_message, mana_cost=mana_cost,
                            spell_level=spell_level, power=power, damage_type=damage_type, to_cast=to_cast)
    spell_to_create = Entity(x, y, '.', libtcod.white, spell_name, render_order=RenderOrder.ITEM, spell=spell_component)

    return spell_to_create