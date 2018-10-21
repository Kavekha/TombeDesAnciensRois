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

        print('INFO : Nous sommes dans CastSpell')

        if not spell_entity.spell.targeting and not spell_entity.spell.to_cast:
            results.append({'message': Message('{} doesn t have a targeting system. Canceled.'.format(spell_entity.name)
                                               , libtcod.yellow)})
            print('DEBUG : spell component targeting : {}'.format(spell_entity.spell.targeting))

        elif kwargs.get('to_cast'):
            kwargs = {**spell_entity.spell.function_kwargs, **kwargs}
            spell_cast_results = spell_entity.spell.spell_function(self.owner, spell_entity.spell, **kwargs)

            results.extend(spell_cast_results)

        # refacto v16c
        elif spell_entity.spell.targeting:
            results.append({'spell_targeting': {'spell': spell_entity, 'target_mode': spell_entity.spell.targeting}})

        else:
            results.append({'message': Message('Error : {} has no target mode.'.format(spell_entity.name), libtcod.yellow)})

        return results
