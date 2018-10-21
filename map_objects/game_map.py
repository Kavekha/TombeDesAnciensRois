import libtcodpy as libtcod

from random import randint
from render_functions import RenderOrder

from components.stairs import Stairs

from entity import Entity

from game_messages import Message

from random_utils import random_choice_from_dict, from_dungeon_level

from map_objects.tile import Tile
from map_objects.rectangle import Rect

from data.data_monsters import generate_monster
from data.data_items import generate_item
from data.data_weapons import generate_weapon
from data.data_dungeons import generate_dungeon_building_specs, generate_dungeon_monsters_specs, \
    generate_dungeon_items_specs, get_random_dungeon


# v15 Refacto.
class GameMap:
    def __init__(self, width, height, version, name, dungeon_level=1, dungeon_config=get_random_dungeon()):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.version = version
        self.name = name
        self.dungeon_level = dungeon_level
        self.dungeon_config = dungeon_config

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):

        # v15 : config dungeon.
        # dungeon_to_build = 'the_pit'
        dungeon_to_build = 'the_necropole'

        dungeon_name, nb_floors, room_min_size, room_max_size, \
        max_room = generate_dungeon_building_specs(dungeon_to_build)

        self.name = dungeon_name

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

                self.place_entities(new_room, entities, dungeon_to_build)
                # append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        # condition add in v14.
        if self.dungeon_level < 8:
            stairs_component = Stairs(self.dungeon_level + 1)
            down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Stairs',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            entities.append(down_stairs)

        else:
            # v15. Refacto monster. Test Data Monster.
            monster = generate_monster('ancient_king_horde', center_of_last_room_x, center_of_last_room_y)
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

    def place_entities(self, room, entities, dungeon_to_build):
        # v15 configurable dungeons.
        monster_boss, max_monsters_per_room_by_level, min_monsters_per_room_by_level, \
        monster_list_from_config = generate_dungeon_monsters_specs(dungeon_to_build)

        max_items_per_room_by_level, min_items_per_room_by_level, max_number_of_weapons_by_level, \
        item_list_from_config, weapon_list_from_config = generate_dungeon_items_specs(dungeon_to_build)


        # random nb of monsters
        max_monsters_per_room = from_dungeon_level(max_monsters_per_room_by_level, self.dungeon_level)
        max_items_per_room = from_dungeon_level(max_items_per_room_by_level, self.dungeon_level)

        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        # v15 config dungeon. Chances to create monster, item & weapon this level.
        monster_chances = {}
        for i in monster_list_from_config:
            monster_chances[i] = from_dungeon_level(monster_list_from_config[i], self.dungeon_level)

        item_chances = {}
        for i in item_list_from_config:
            item_chances[i] = from_dungeon_level(item_list_from_config[i], self.dungeon_level)

        weapon_chances = {}
        for i in weapon_list_from_config:
            weapon_chances[i] = from_dungeon_level(weapon_list_from_config[i], self.dungeon_level)
            print('INFO : weapon chance : ', weapon_chances[i])

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                # v15 generate dungeon from config
                monster = generate_monster(monster_choice, x, y)
                print('INFO : chosen monster was {}, created was {}'.format(monster_choice, monster.name))

                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                # v16 : chance to have a weapon against chance to have an item.
                rand_for_weapon = randint(1, 10)
                if rand_for_weapon == 1 and max_number_of_weapons_by_level > 0:
                    print('INFO : weapon_chances = ', weapon_chances)
                    weapon_choice = random_choice_from_dict(weapon_chances)
                    if weapon_choice is not None:
                        max_number_of_weapons_by_level -= 1
                        item = generate_weapon(weapon_choice, x, y)
                        print('INFO : weapon requested {}, weapon given {}'.format(weapon_choice, item.name))

                if rand_for_weapon > 1 or weapon_choice == None:
                    item_choice = random_choice_from_dict(item_chances)

                    # v15 generate item from config dungeon
                    item = generate_item(item_choice, x, y, self)
                    print('INFO : item demandé {}, item obtenu {}'.format(item_choice, item.name))

                entities.append(item)

        '''
        for i in range(number_of_weapons):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                weapon_choice = random_choice_from_dict(weapon_chances)

                # v15 generate item from config dungeon
                weapon = generate_weapon(weapon_choice, x, y)

                entities.append(weapon)
        '''

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
