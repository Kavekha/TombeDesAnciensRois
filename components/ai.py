import libtcodpy as libtcod
from random import randint
from enum import Enum

from game_messages import Message


# v 15
class BrainStates(Enum):
    NORMAL = 0
    CONFUSED = 1


class BasicMonster:
    def __init__(self):
        self.state = BrainStates.NORMAL

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner

        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target, game_map)
                results.extend(attack_results)

        return results


class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns
        self.state = BrainStates.CONFUSED

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            results.extend(self.out_of_confusion())

        return results

    def take_damage(self, damage):

        results = []

        print('INFO : Damage taken while Confused')
        chance_to_stay_confuse = (self.owner.fighter.hp - damage) / self.owner.fighter.max_hp
        chance_to_stay_confuse *= 200
        rand = randint(1, 100)

        print('DEBUG : chance to stay confuse : {}, rand {}'.format(chance_to_stay_confuse, rand))

        if rand > chance_to_stay_confuse:
            self.number_of_turns -= 2
            print('INFO : confuse time reduces by damage.')
            if self.number_of_turns <= 0:
                results.extend(self.out_of_confusion())

        return results

    def out_of_confusion(self):
        results = []

        self.owner.ai = self.previous_ai
        results.append({'message': Message('The {} is no longer confused!'.format(self.owner.name), libtcod.red)})

        return results

