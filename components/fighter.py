import libtcodpy as libtcod

from enum import Enum
from random import randint

from game_messages import Message
from loader_functions.scores_loader import create_score_bill    #v14a

from components.ai import BrainStates


# v15
class DamageType(Enum):
    UNKNOWN = 1
    PHYSICAL = 2
    FIRE = 3
    LIGHTNING = 4
    LIFE = 5
    ARCANE = 6


class Fighter:
    def __init__(self, hp, str, dex, int=0, mana=0, defense=0, resistance=0, xp=0, background=None):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_resistance = resistance
        self.xp = xp
        self.base_str = str
        self.base_dex = dex
        self.background = background
        self.base_int = int
        self.base_max_mana = mana
        self.mana = mana

        if self.background == 'warrior':
            self.base_max_hp += 50
            self.base_str += 2
            self.base_dex += 1
            self.base_int += 1

        if self.background == 'mage':
            self.base_max_hp += 25
            self.base_str += 0
            self.base_dex += 1
            self.base_int += 3
            self.base_max_mana += 25

        self.hp = self.base_max_hp
        self.mana = self.base_max_mana

    @property
    def max_mana(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_mana_bonus
        else:
            bonus = 0

        return self.base_max_mana + bonus

    @property
    def int(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.int_bonus
        else:
            bonus = 0

        return self.base_int + bonus

    @property
    def str(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.str_bonus
        else:
            bonus = 0

        return self.base_str + bonus

    @property
    def dex(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.dex_bonus
        else:
            bonus = 0

        return self.base_dex + bonus

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0
        if self.owner.level:
            bonus += (self.owner.level.current_level - 1) * 10

        return self.base_max_hp + bonus

    @property
    def resistance(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.resistance_bonus
        else:
            bonus = 0

        return self.base_resistance + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, damage, attacker, game_map, damage_type=DamageType.UNKNOWN):
        results = []

        if damage_type == DamageType.PHYSICAL:
            damage -= self.defense

            if damage <= 0:
                damage = 0

            results.append({'message': Message('{} attacks {} for {} hit points.'.format(
                attacker.owner.name.capitalize(), self.owner.name, str(damage)), libtcod.white)})

        if damage_type in (DamageType.FIRE, DamageType.LIGHTNING, DamageType.ARCANE):
            damage -= self.resistance

            results.append({'message': Message('{} blast {} with magical energy for {} hit points.'.format(
                attacker.name.capitalize(), self.owner.name, str(damage)), libtcod.white)})

        self.hp -= damage

        if self.owner.ai:
            if self.owner.ai.state == BrainStates.CONFUSED:
                self.owner.ai.take_damage(damage)
                print('INFO : Confused AI ')
            else:
                print('INFO : Not confused ai, ai = ', self.owner.ai)

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})
            if not self.owner.ai:
                create_score_bill(self.owner, game_map.dungeon_level, attacker, game_map.version)

        return results

    def attack(self, target, game_map):
        results = []

        hit_chance = int((self.dex + 10) / ((target.fighter.dex + 10) * 2) * 100)
        rand = randint(1, 100)

        if target.ai:
            if target.ai.state == BrainStates.CONFUSED:
                rand = 0

        if rand <= hit_chance:
            damage = self.str
            results.extend(target.fighter.take_damage(damage, self, game_map, damage_type=DamageType.PHYSICAL))
        else:
            results.append({'message': Message('{} misses against {}!'.format(
                self.owner.name.capitalize(), target.name.capitalize()), libtcod.white)})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp
