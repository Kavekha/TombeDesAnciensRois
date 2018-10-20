import libtcodpy as libtcod

from game_messages import Message
from loader_functions.score_loaders import create_score_bill


class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, amount, attacker, game_map): # v14 attacker, game_map ajoutés.
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})
            # version 14. scorebill.
            if not self.owner.ai:
                print('DEBUG: Je suis un player')
                create_score_bill(self.owner, game_map.dungeon_level, attacker, game_map.version)

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target, game_map):
        results = []

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{} attacks {} for {} hit points.'.format(self.owner.name.capitalize(),
                                                                                         target.name, str(damage)),
                                               libtcod.white)})
            results.extend(target.fighter.take_damage(damage, self.owner, game_map))  # v14 self.owner, game_map ajoutés
        else:
            results.append({'message': Message('{} attacks {} but does no damage.'.format(self.owner.name.capitalize(),
                                                                                          target.name), libtcod.white)})

        return results
