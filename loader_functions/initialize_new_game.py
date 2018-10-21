import libtcodpy as libtcod

from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment
from components.death import Death
from components.spellbook import Spellbook

from death_functions import kill_player

from entity import Entity
from game_messages import MessageLog
from game_states import GameStates

from map_objects.game_map import GameMap

from render_functions import RenderOrder

from data.data_weapons import generate_weapon
from data.data_items import generate_item
from data.data_spells import generate_spell


def get_constants():
    window_title = 'Tomb of the Ancient Kings'
    version = '0.16a'
    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3
    max_items_per_room = 2

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    constants = {
        'window_title': window_title,
        'version': version,
        'screen_width': screen_width,
        'screen_height': screen_height,

        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,

        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,

        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,

        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,

        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,

        'colors': colors
    }

    return constants


def get_game_variables(constants):
    fighter_component = Fighter(hp=50, mana=10, str=2, dex=2, int=1, background='warrior')
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    death_component = Death(kill_player)
    spellbook_component = Spellbook(26)
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component,
                    equipment=equipment_component, death=death_component, spellbook=spellbook_component)

    entities = [player]

    dagger = generate_weapon('dagger', 0, 0)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    potion = generate_item('healing_potion', 0, 0)
    player.inventory.add_item(potion)

    for spell_to_create in ('magic_missile', 'arcanic_wall'):
        spell = generate_spell(spell_to_create, 0, 0)
        player.spellbook.add_spell(spell)

    game_map = GameMap(constants['map_width'], constants['map_height'], constants['version'], 'Dungeon')
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
