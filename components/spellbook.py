import libtcodpy as libtcod
from enum import Enum

from game_messages import Message


class TargetType(Enum):
    SELF = 0
    ENEMY = 1
    ALLIED = 2
    RADIUS = 3
    TILE = 4


class Spellbook:
    def __init__(self, capacity):
        self.capacity = capacity
        self.spells = []

    def add_spell(self, spell):
        results = []

        if spell in self.spells:
            results.append({'message': Message('{} is already in your spellbook.'.format(spell.name), libtcod.yellow)})
        else:
            self.spells.append(spell)

        return results

    def cast_spell(self, spell_entity, **kwargs):
        results = []

        spell_component = spell_entity.spell

        if not spell_component.targeting:
            results.append({'message': Message('{} doesn t have a targeting system. Canceled.'.format(spell_entity.name), libtcod.yellow)})
            print('DEBUG : spell component targeting : {}'.format(spell_component.targeting))

        elif kwargs.get('to_cast'):

            kwargs = {**spell_component.function_kwargs, **kwargs}
            spell_cast_results = spell_component.spell_function(self.owner, spell_entity.spell, **kwargs)

            results.extend(spell_cast_results)

        # targeting on the player
        elif spell_component.targeting == TargetType.SELF:
            results.append({'message': Message('{} target self.'.format(spell_entity.name), libtcod.yellow)})

        elif spell_component.targeting == TargetType.ALLIED:
            results.append({'message': Message('{} target allied.'.format(spell_entity.name), libtcod.yellow)})

        elif spell_component.targeting == TargetType.ENEMY:
            # results.append({'message': Message('{} target a fighter.'.format(spell_entity.name), libtcod.yellow)})
            results.append({'spell_targeting': {'spell': spell_entity, 'target_mode': spell_component.targeting}})

        elif spell_component.targeting == TargetType.RADIUS:
            results.append({'message': Message('{} target a Tile and all tiles around.'.format(spell_entity.name), libtcod.yellow)})

        elif spell_component.targeting == TargetType.TILE:
            results.append({'message': Message('{} target a tile.'.format(spell_entity.name), libtcod.yellow)})

        else:
            results.append({'message': Message('Error : {} has no target mode.'.format(spell_entity.name), libtcod.yellow)})

        '''
        if spell_component.spell_targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
            results.append({'spell_targeting': spell_entity})
        else:
            kwargs = {**spell_component.function_kwargs, **kwargs}
            spell_cast_results = spell_component.spell_function(self.owner, **kwargs)

            results.extend(spell_cast_results)
        '''

        return results
