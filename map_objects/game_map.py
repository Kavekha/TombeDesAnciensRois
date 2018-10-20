import libtcodpy as libtcod

from random import randint
from render_functions import RenderOrder

from components.ai import BasicMonster
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs
from components.death import Death

from death_functions import kill_monster, kill_final_boss

from entity import Entity

from game_messages import Message
from item_functions import heal, cast_lightning, cast_fireball, cast_confuse

from random_utils import random_choice_from_dict, from_dungeon_level

from map_objects.tile import Tile
from map_objects.rectangle import Rect


class GameMap:
    def __init__(self, width, height, version, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.version = version

        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break

            else:
                # no intersection
                self.create_room(new_room)
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # first room, player starts there
                    player.x = new_x
                    player.y = new_y
                else:
                    # connect it to previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip if v or h for the tunnel
                    if randint(0, 1) == 1:
                        # move h, then v
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)
                # append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        # condition add in v14.
        if self.dungeon_level < 10:
            stairs_component = Stairs(self.dungeon_level + 1)
            down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            entities.append(down_stairs)
        else:
            fighter_component = Fighter(hp=120, defense=8, power=32, xp=0)
            ai_component = BasicMonster()
            death_component = Death(kill_final_boss)  # v14

            monster = Entity(center_of_last_room_x, center_of_last_room_y, 'K', libtcod.darker_amber, 'Ancient King', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                             death=death_component)
            entities.append(monster)


    def create_room(self, room):
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) +1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) +1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities):
        # random nb of monsters
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 2], [4, 3], [5, 4], [6, 6], [7, 10]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 3], [3, 6],[4, 10]], self.dungeon_level)
        print('DEBUG : max monsters : {}'.format(max_monsters_per_room))
        print('DEBUG : max items : {}'.format(max_items_per_room))

        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances = {
            'orc': from_dungeon_level([[80, 1], [70, 3], [60, 5], [50, 7], [30, 10]], self.dungeon_level),
            'troll': from_dungeon_level([[15, 1], [30, 3],[60, 5]], self.dungeon_level),
            'ogre': from_dungeon_level([[0, 1], [1, 3], [2, 5], [5, 6], [10, 7], [15, 8], [20, 9], [25, 10]],
                                       self.dungeon_level)
        }

        item_chances = {
            'healing_potion': 35,
            'confusion_scroll': from_dungeon_level([[10, 1], [25,3]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[5, 1], [10, 3], [25, 6]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[10, 2], [15, 5]], self.dungeon_level),
            'sword': from_dungeon_level([[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level)
        }

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)
                print('DEBUG : monster_choice from game map = {}'.format(monster_choice))
                print('monster_choice == orc? reponse : {}, alors que monster choice = {}'.format(monster_choice == 'orc', monster_choice))

                print('Type of monster_choice = {} et contient {}'.format(type(monster_choice), monster_choice))

                if monster_choice == 'orc':
                    print('Ogre was chosen')
                    fighter_component = Fighter(hp=20, defense=0, power=4, xp=25)
                    ai_component = BasicMonster()
                    death_component = Death(kill_monster)   #v14

                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                     death=death_component)

                if monster_choice == 'troll':
                    print('Troll was chosen')
                    fighter_component = Fighter(hp=30, defense=2, power=8, xp=100)
                    ai_component = BasicMonster()
                    death_component = Death(kill_monster)   #v14

                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                     death=death_component)

                if monster_choice == 'ogre':
                    print('Ogre was chosen')
                    fighter_component = Fighter(hp=60, defense=4, power=16, xp=400)
                    ai_component = BasicMonster()
                    death_component = Death(kill_monster)   #v14

                    monster = Entity(x, y, 'O', libtcod.darker_crimson, 'Ogre', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                     death=death_component)
                else:
                    print('WARNING : "Else" was used, instead of {} in monster choice'.format(monster_choice))

                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=40)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                                          damage=25, radius=3, game_map=self)
                    item = Entity(x, y, '#', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'lightning_scroll':
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5, game_map=self)   # v14a gamemap
                    item = Entity(x, y, '#', libtcod.yellow, 'Lightning scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan))
                    item = Entity(x, y, '#', libtcod.light_pink, 'Confusion scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(x, y, '/', libtcod.sky, 'sword', equippable=equippable_component)
                elif item_choice == 'shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
                    item = Entity(x, y, '[', libtcod.darker_orange, 'Shield', equippable=equippable_component)
                else:
                    item = Entity(x, y, 'x', libtcod.light_gray, 'item choice out of range',
                                  render_order=RenderOrder.ITEM)

                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        return entities
