import libtcodpy as libtcod


# v15 Having different confs for dungeons.

def get_dungeon_specs(dungeon_name):
    dungeon_specs = {
        'the_pit': {
            'dungeon_name': 'La Fausse',
            'nb_floors': 8,
            'room_min_size': 6,
            'room_max_size': 10,
            'max_room': 30,
            'dark_wall': libtcod.Color(0, 0, 100),
            'dark_ground': libtcod.Color(50, 50, 150),
            'light_wall': libtcod.Color(130, 110, 50),
            'light_ground': libtcod.Color(200, 180, 50),
            'monster_boss': 'ancient_king_horde',
            'max_monsters_per_room_by_level': [[2, 1], [3, 2], [4, 3], [5, 4], [6, 6], [7, 8]],
            'min_monsters_per_room_by_level': [[0, 1]],
            'max_items_per_room_by_level': [[1, 1], [2, 3], [3, 5], [4, 7]],
            'min_items_per_room_by_level': [[0, 1]],
            'monster_chances': {
                'orloog': [[80, 1], [70, 3], [60, 4], [50, 6], [40, 8]],
                'rat': [[10, 1], [20, 2], [30, 4], [40, 6], [50, 8]],
                'goblin': [[5, 1], [10, 3], [20, 5], [30, 6], [40, 8]],
                'troll': [[2, 1], [10, 2], [20, 3], [30, 4], [40, 6], [50, 8]],
                'ogre': [[0, 2], [1, 3], [2, 4], [5, 5], [10, 6], [15, 8]]
            },
            'item_chances': {
                'healing_potion': [[35, 1]],
                'confusion_scroll': [[10, 1], [25, 3]],
                'fireball_scroll': [[5, 1], [10, 3], [25, 6]],
                'lightning_scroll': [[10, 2], [15, 5]],
                'sword': [[1, 4]],
                'shield': [[15, 6]]
            }
        }
    }

    return dungeon_specs[dungeon_name]


def generate_dungeon_building_specs(dungeon_name):
    dungeon = get_dungeon_specs(dungeon_name)

    dungeon_name = dungeon['dungeon_name']
    nb_floors = dungeon['nb_floors']
    room_max_size = dungeon['room_max_size']
    room_min_size = dungeon['room_min_size']
    max_room = dungeon['max_room']
    dark_wall = dungeon['dark_wall']
    dark_ground = dungeon['dark_ground']
    light_wall = dungeon['light_wall']
    light_ground = dungeon['light_ground']

    return dungeon_name, nb_floors, room_min_size, room_max_size, max_room, dark_wall, dark_ground, light_wall, \
           light_ground


def generate_dungeon_monsters_specs(dungeon_name):
    dungeon = get_dungeon_specs(dungeon_name)

    monster_boss = dungeon['monster_boss']
    max_monsters_per_room_by_level = dungeon['max_monsters_per_room_by_level']
    min_monsters_per_room_by_level = dungeon['min_monsters_per_room_by_level']
    monster_chances = dungeon['monster_chances']

    return monster_boss, max_monsters_per_room_by_level, min_monsters_per_room_by_level, monster_chances


def generate_dungeon_items_specs(dungeon_name):
    dungeon = get_dungeon_specs(dungeon_name)

    max_items_per_room_by_level = dungeon['max_items_per_room_by_level']
    min_items_per_room_by_level = dungeon['min_items_per_room_by_level']
    item_chances = dungeon['item_chances']

    return max_items_per_room_by_level, min_items_per_room_by_level, item_chances
