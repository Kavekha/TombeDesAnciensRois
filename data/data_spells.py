import libtcodpy as libtcod

from entity import Entity
from spell_functions import cast_magic_missile

from game_messages import Message

from components.spell import Spell
from components.spellbook import TargetType

from render_functions import RenderOrder
from components.fighter import DamageType

def get_spells_list(spell_name):
    spells_list = {
        'magic_missile': {
            'spell_name': 'Missile magique',
            'spell_function': cast_magic_missile,
            'targeting': TargetType.ENEMY,
            'targeting_message': 'Left click on the enemy you want to hit. Right-click or Esc to cancel.',
            'mana_cost': 2,
            'spell_level': 1,
            'power': 1,
            'damage_type': DamageType.ARCANE
        }
    }

    return spells_list[spell_name]


def generate_spell(spell_name, x, y):
    spec_from_spell = get_spells_list(spell_name)

    spell_name = spec_from_spell['spell_name']
    spell_function = spec_from_spell['spell_function']
    targeting = spec_from_spell['targeting']
    targeting_message = spec_from_spell['targeting_message']
    mana_cost = spec_from_spell['mana_cost']
    spell_level = spec_from_spell['spell_level']
    power = spec_from_spell['power']
    damage_type = spec_from_spell['damage_type']

    spell_component = Spell(spell_function=spell_function, targeting=targeting,
                            targeting_message=Message(targeting_message, libtcod.light_blue), mana_cost=mana_cost,
                            spell_level=spell_level, power=power, damage_type=damage_type)
    spell_to_create = Entity(x, y, '.', libtcod.white, spell_name, render_order=RenderOrder.ITEM, spell=spell_component)

    return spell_to_create