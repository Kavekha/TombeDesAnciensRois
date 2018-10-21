import libtcodpy as libtcod

from game_messages import Message
from systems.targeting import TargetType


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

        if not spell_component.targeting and not spell_component.to_cast:
            results.append({'message': Message('{} doesn t have a targeting system. Canceled.'.format(spell_entity.name), libtcod.yellow)})
            print('DEBUG : spell component targeting : {}'.format(spell_component.targeting))

        elif kwargs.get('to_cast'):
            print('DEBUG : Spell must be cast.')
            kwargs = {**spell_component.function_kwargs, **kwargs}
            spell_cast_results = spell_component.spell_function(self.owner, spell_entity.spell, **kwargs)

            results.extend(spell_cast_results)

        # tested
        elif spell_component.targeting == TargetType.SELF:
            print('DEBUG : Spell target self')
            results.append({'spell_targeting': {'spell': spell_entity, 'target_mode': spell_component.targeting}})

        # tested, allied not implemented
        elif spell_component.targeting == TargetType.ALLIED:
            results.append({'message': Message('{} target allied.'.format(spell_entity.name), libtcod.yellow)})

        # tested, enemy not implemented. Only entity fighter.
        elif spell_component.targeting == TargetType.ENEMY:
            results.append({'spell_targeting': {'spell': spell_entity, 'target_mode': spell_component.targeting}})

        # in progress
        elif spell_component.targeting == TargetType.RADIUS:
            results.append({'spell_targeting': {'spell': spell_entity, 'target_mode': spell_component.targeting}})

        # To refacto.
        elif spell_component.targeting == TargetType.TILE:
            results.append({'spell_targeting': {'spell': spell_entity, 'target_mode': spell_component.targeting}})

        # Done.
        elif spell_component.targeting == TargetType.CLOSEST_ENTITIES:
            results.append({'spell_targeting': {'spell': spell_entity, 'target_mode': spell_component.targeting}})
            print('DEBUG : targeting closest entities')

        elif spell_component.targeting == TargetType.TILE_OR_ENTITY:
            results.append({'spell_targeting': {'spell': spell_entity, 'target_mode': spell_component.targeting}})
        else:
            results.append({'message': Message('Error : {} has no target mode.'.format(spell_entity.name), libtcod.yellow)})

        return results
