import libtcodpy as libtcod

from item_functions import heal, cast_fireball, cast_lightning, cast_confuse, gain_mana
from render_functions import RenderOrder

from damage_types import DamageType
from components.item import Item

from game_messages import Message
from systems.targeting import TargetType

from entity import Entity

# v15 Refacto objets.


def get_items_list(item_name):
    items_list = {
        'healing_potion': {
            'name': 'Healing potion',
            'use_function': heal,
            'power': 18,
            'aspect': '!',
            'color': libtcod.violet,
            'targeting': TargetType.SELF,
            'targeting_message': None,
            'radius': None,
            'maximum_range': None,
            'damage_type': DamageType.LIFE,
            'stackable': True
        },
        'mana_potion': {
            'name': 'Mana potion',
            'use_function': gain_mana,
            'power': 18,
            'aspect': '!',
            'color': libtcod.light_blue,
            'targeting': TargetType.SELF,
            'targeting_message': None,
            'radius': None,
            'maximum_range': None,
            'damage_type': DamageType.LIFE,
            'stackable': True
        },
        'fireball_scroll': {
            'name': 'Fireball scroll',
            'use_function': cast_fireball,
            'targeting_message': 'Left-click a target tile for the 3x3 fireball, or right-click to cancel.',
            'power': 24,
            'radius': 3,
            'aspect': '#',
            'color': libtcod.red,
            'targeting': TargetType.RADIUS,
            'maximum_range': None,
            'damage_type': DamageType.FIRE,
            'stackable': True
        },
        'lightning_scroll': {
            'name': 'Lightning scroll',
            'use_function': cast_lightning,
            'targeting_message': None,
            'power': 40,
            'radius': None,
            'maximum_range': 5,
            'aspect': '#',
            'color': libtcod.yellow,
            'targeting': TargetType.CLOSEST_ENTITIES,
            'damage_type': DamageType.LIGHTNING,
            'stackable': True
        },
        'confusion_scroll': {
            'name': 'Confusion scroll',
            'use_function': cast_confuse,
            'targeting_message': 'Left-click an enemy to confuse it, or right-click to cancel.',
            'power': 12,
            'radius': 0,
            'aspect': '#',
            'color': libtcod.light_pink,
            'targeting': TargetType.ENEMY,
            'maximum_range': None,
            'damage_type': DamageType.UNKNOWN,
            'stackable': True
        }
    }

    return items_list[item_name]


def generate_item(item_name, x, y, game_map=None):
    item = get_items_list(item_name)

    use_function = item.get('use_function')
    power = item.get('power')
    aspect = item.get('aspect')
    color = item.get('color')
    name = item.get('name')
    targeting_message = item.get('targeting_message')
    if targeting_message:
        targeting_message = Message(targeting_message, libtcod.light_cyan)
    radius = item.get('radius')
    targeting = item.get('targeting')
    maximum_range = item.get('maximum_range')
    damage_type = item.get('damage_type')
    stackable = item.get('stackable')

    item_component = Item(use_function=use_function, power=power, game_map=game_map,
                          targeting_message=targeting_message, radius=radius, targeting=targeting,
                          maximum_range=maximum_range, damage_type=damage_type, stackable=stackable)
    item_to_return = Entity(x, y, aspect, color, name, render_order=RenderOrder.ITEM, item=item_component)

    return item_to_return
