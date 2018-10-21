import libtcodpy as libtcod

from render_functions import RenderOrder
from components.item import Item

import math


class Entity:
    # generic object to represent players, enemies, items, etc
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None,
                 item=None, inventory=None, stairs=None, level=None, equipment=None, equippable=None, death=None,
                 spellbook=None, spell=None):
        # v14 death added
        # v16 spellbook added
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable
        self.death = death
        self.spellbook = spellbook
        self.spell = spell

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

        if self.death:
            self.death.owner = self

        if self.spellbook:
            self.spellbook.owner = self

        if self.spell:
            self.spell.owner = self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move_astar(self, target, entities, game_map):
        # create a fov map at the dimensions of the map
        fov = libtcod.map_new(game_map.width, game_map.height)

        # scan current map each turn and set all walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight, not game_map.tiles[x1][y1].blocked)

        # scan all objets to see if there are objects that must be navigated around.
        # check also if object isn't self or the target
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                #set the tile as a wall so it muyst be navigated around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # allocate a A* path
        # 1.31 normal diag cost of moving, to put to 0 if diagonal forbiden
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # compute path between self coordinates and the target coordinate
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # check if path exists && shorter than 25 tiles
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # find next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # set self coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # old move function if no path
            self.move_towards(target.x, target.y, game_map, entities)

        # delete the path to free memeory
        libtcod.path_delete(my_path)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        # v16 entity.fighter to deal with obstacle like arcanic wall.
        if entity.blocks and entity.x == destination_x and entity.y == destination_y and entity.fighter:
            return entity
    return None
