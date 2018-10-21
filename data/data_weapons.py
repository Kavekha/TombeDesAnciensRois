import libtcodpy as libtcod

from components.equippable import Equippable
from equipement_slots import EquipmentSlots

from entity import Entity


def get_weapons_list(weapon_name):
    weapons_list = {
        'sword': {
            'name': 'Sword',
            'EquipmentSlots': EquipmentSlots.MAIN_HAND,
            'str_bonus': 3,
            'dex_bonus': 0,
            'max_hp_bonus': 0,
            'defense_bonus': 0,
            'resistance_bonus': 0,
            'aspect': '/',
            'color': libtcod.sky
        },
        'shield': {
            'name': 'Shield',
            'EquipmentSlots': EquipmentSlots.OFF_HAND,
            'str_bonus': 0,
            'dex_bonus': 0,
            'max_hp_bonus': 0,
            'defense_bonus': 2,
            'resistance_bonus': 0,
            'aspect': '[',
            'color': libtcod.darker_orange
        },
        'dagger': {
            'name': 'Dagger',
            'EquipmentSlots': EquipmentSlots.MAIN_HAND,
            'str_bonus': 1,
            'dex_bonus': 1,
            'max_hp_bonus': 0,
            'defense_bonus': 0,
            'resistance_bonus': 0,
            'aspect': '-',
            'color': libtcod.sky
        }
    }

    return weapons_list[weapon_name]


def generate_weapon(weapon_name, x, y):
    weapon = get_weapons_list(weapon_name)

    name = weapon.get('name')
    equipment_slot = weapon.get('EquipmentSlots')
    str_bonus = weapon.get('str_bonus')
    dex_bonus = weapon.get('dex_bonus')
    max_hp_bonus = weapon.get('max_hp_bonus')
    defense_bonus = weapon.get('defense_bonus')
    resistance_bonus = weapon.get('resistance_bonus')
    aspect = weapon.get('aspect')
    color = weapon.get('color')

    equippable_component = Equippable(equipment_slot, str_bonus=str_bonus, dex_bonus=dex_bonus,
                                      max_hp_bonus=max_hp_bonus, defense_bonus=defense_bonus,
                                      resistance_bonus=resistance_bonus)
    weapon_to_return = Entity(x, y, aspect, color, name, equippable=equippable_component)

    return weapon_to_return
