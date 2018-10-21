import libtcodpy as libtcod

from item_functions import heal, cast_fireball, cast_lightning, cast_confuse
from render_functions import RenderOrder

from components.fighter import DamageType
from components.item import Item

from game_messages import Message

from entity import Entity

# v15 Refacto objets.


def get_items_list(item_name):
    items_list = {
        'healing_potion': {
            'name': 'Healing potion',
            'use_function': heal,
            'power': 40,
            'aspect': '!',
            'color': libtcod.violet,
            'targeting_message': None,
            'text_color': None,
            'radius': None,
            'targeting': False,
            'maximum_range': None,
            'damage_type': DamageType.LIFE
        },
        'fireball_scroll': {
            'name': 'Fireball scroll',
            'use_function': cast_fireball,
            'targeting_message': 'Left-click a target tile for the 3x3 fireball, or right-click to cancel.',
            'text_color': libtcod.light_cyan,
            'power': 25,
            'radius': 3,
            'aspect': '#',
            'color': libtcod.red,
            'targeting': True,
            'maximum_range': None,
            'damage_type': DamageType.FIRE
        },
        'lightning_scroll': {
            'name': 'Lightning scroll',
            'use_function': cast_lightning,
            'targeting_message': None,
            'text_color': libtcod.light_cyan,
            'power': 40,
            'radius': None,
            'maximum_range': 5,
            'aspect': '#',
            'color': libtcod.yellow,
            'targeting': False,
            'damage_type': DamageType.LIGHTNING
        },
        'confusion_scroll': {
            'name': 'Confusion scroll',
            'use_function': cast_confuse,
            'targeting_message': 'Left-click an enemy to confuse it, or right-click to cancel.',
            'text_color': libtcod.light_cyan,
            'power': 0,
            'radius': 0,
            'aspect': '#',
            'color': libtcod.light_pink,
            'targeting': True,
            'maximum_range': None,
            'damage_type': DamageType.UNKNOWN
        }
    }

    return items_list[item_name]


def generate_item(item_name, x, y, game_map):
    item = get_items_list(item_name)

    use_function = item.get('use_function')
    power = item.get('power')
    aspect = item.get('aspect')
    color = item.get('color')
    name = item.get('name')
    targeting_message = item.get('targeting_message')
    text_color = item.get('text_color')
    radius = item.get('radius')
    targeting = item.get('targeting')
    maximum_range = item.get('maximum_range')
    damage_type = item.get('damage_type')

    item_component = Item(use_function=use_function, power=power, game_map=game_map, targeting_message=Message(
        targeting_message, text_color), radius=radius, targeting=targeting, maximum_range=maximum_range,
                          damage_type=damage_type)
    item_to_return = Entity(x, y, aspect, color, name, render_order=RenderOrder.ITEM, item=item_component)

    return item_to_return
