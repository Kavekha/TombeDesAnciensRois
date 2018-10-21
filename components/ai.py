import libtcodpy as libtcod
from random import randint
from enum import Enum

from game_messages import Message


# v 15
class BrainStates(Enum):
    NORMAL = 0
    CONFUSED = 1
    PARALYZED = 2


class MovingItem:
    def __init__(self, caster, power, damage_type, target_x, target_y, entities):
        self.caster = caster
        self.power = power
        self.damage_type = damage_type
        self.target_x = target_x
        self.target_y = target_y
        self.duration = power
        self.entities = entities

    def explode_on_contact(self, entities, game_map):
        monster = self.owner

        results = []
        # Am I on someone toe?
        print('DEBUG : Im at : ', monster.x, monster.y)
        for entity in entities:
            if entity.x == monster.x and entity.y == monster.y and entity != self.caster and entity != monster and entity.fighter:
                print('DEBUG : entity in same place')
                damage = self.power * self.caster.fighter.int
                self.power = int(self.power / 2)
                print('DEBUG : entity has life : {} and is {} '.format(entity.fighter.hp, entity.name))
                results.extend(entity.fighter.take_damage(damage, self.caster, game_map, self.damage_type))
                results.append({'message': Message('{} size is reduce by half after its explosion.'.format(
                    self.owner.name), libtcod.blue)})
                break
        else:
            print('DEBUG : no entity ever on the same spot')

        return results

    def take_turn(self, player, fov_map, game_map, entities):

        results = []

        monster = self.owner
        print('MY TURN, I m at ', monster.x, monster.y)

        results.extend(self.explode_on_contact(entities, game_map))

        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance(self.target_x, self.target_y) > 0:
                monster.move_towards(self.target_x, self.target_y, game_map, entities)
                self.duration -= 1
            else:
                results.extend(self.dispeled())

        else:
            self.duration -= 2

        if self.duration <= 0:
            results.extend(self.dispeled())
            pass


        return results

    def dispeled(self):
        results = []

        results.append({'message': Message('{} exploded!'.format(self.owner.name), libtcod.blue)})
        self.entities.remove(self.owner)

        return results


class Obstacle:
    def __init__(self, tile, entities, number_of_turn=1):
        self.number_of_turns = number_of_turn
        self.tile = tile
        self.entities = entities

        self.tile.blocked = True
        self.tile.block_sight = True

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            self.number_of_turns -= 1
            print('DEBUG : turn')
        else:
            print('DDEBUG : dispel')
            self.dispeled()

        print('DEBUG : Arcanic wall take turn. Nb of turn : ', self.number_of_turns)

        return results

    def dispeled(self):
        print('Dispel asked.')
        print('Before dispel : {}'.format(self.tile.blocked))
        self.tile.blocked = False
        self.tile.block_sight = False
        print('After dispel : {}'.format(self.tile.blocked))
        self.entities.remove(self.owner)


class BasicMonster:
    def __init__(self):
        self.state = BrainStates.NORMAL

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner

        # v16 ultra crade gestion de paralyzed, ici et dans Fighter
        if not monster.fighter.paralyzed:
            if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

                if monster.distance_to(target) >= 2:
                    monster.move_astar(target, entities, game_map)

                elif target.fighter.hp > 0:
                    attack_results = monster.fighter.attack(target, game_map)
                    results.extend(attack_results)
        else:
            if monster.fighter.paralyzed > 0:
                results.append({'message': Message('{} is still paralyzed.'.format(monster.name), libtcod.light_blue)})
                monster.fighter.paralyzed -= 1
            else:
                self.out_of_paralyze()


        return results

    def out_of_paralyze(self):

        results = []

        results.append({'message': Message('{} starts moving!'.format(self.owner.name), libtcod.red)})
        self.owner.fighter.paralyzed = None

        return results


class ModifiedMindMonster:
    def __init__(self, previous_ai, number_of_turns=1):
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

        if rand > chance_to_stay_confuse:
            self.number_of_turns -= 2
            if self.number_of_turns <= 0:
                results.extend(self.out_of_confusion())

        return results

    def out_of_confusion(self):
        results = []

        self.owner.ai = self.previous_ai
        results.extend({'message': Message('The {} is no longer confused!'.format(self.owner.name), libtcod.red)})

        return results

