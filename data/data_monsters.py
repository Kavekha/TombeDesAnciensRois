# v15. Refacto monster creation.

import libtcodpy as libtcod

from render_functions import RenderOrder
from components.fighter import Fighter
from components.ai import BasicMonster
from components.death import Death
from entity import Entity
from death_functions import kill_monster, kill_final_boss


'''
Data structure for monster.

    ancient_king_horde = {
        'name': 'Ancient King of the Horde',
        'aspect': 'K',
        'color': libtcod.darker_amber,
        'death_function': kill_final_boss,
        'hp': 120,
        'str': 32,
        'dex': 16,
        'defense': 4,
        'resistance': 3,
        'xp': 0
     }
'''


def get_monster_list(monster_name):
    monsters_list = {
        'ancient_king_horde': {
            'name': 'Ancient King of the Horde',
            'aspect': 'K',
            'color': libtcod.darker_amber,
            'death_function': kill_final_boss,
            'ai': BasicMonster(),
            'hp': 120,
            'str': 40,
            'dex': 16,
            'defense': 4,
            'resistance': 0,
            'xp': 0
         },
        'orloog': {
            'name': 'Orloog',
            'aspect': 'o',
            'color': libtcod.desaturated_green,
            'death_function': kill_monster,
            'ai': BasicMonster(),
            'hp': 15,
            'str': 5,
            'dex': 2,
            'defense': 0,
            'resistance': 0,
            'xp': 21
        },
        'troll': {
            'name': 'Troll',
            'aspect': 'T',
            'color': libtcod.darker_green,
            'death_function': kill_monster,
            'ai': BasicMonster(),
            'hp': 30,
            'str': 10,
            'dex': 4,
            'defense': 1,
            'resistance': 0,
            'xp': 90
        },
        'ogre': {
            'name': 'Ogre',
            'aspect': 'O',
            'color': libtcod.darker_crimson,
            'death_function': kill_monster,
            'ai': BasicMonster(),
            'hp': 60,
            'str': 20,
            'dex': 8,
            'defense': 2,
            'resistance': 0,
            'xp': 360
        }
    }

    return monsters_list[monster_name]


def generate_monster(monster_name, x, y):
    monster = get_monster_list(monster_name)

    ai = monster.get('ai')
    death_function = monster.get('death_function')
    name = monster.get('name')
    aspect = monster.get('aspect')
    color = monster.get('color')
    hp = monster.get('hp')
    str = monster.get('str')
    dex = monster.get('dex')
    defense = monster.get('defense')
    xp = monster.get('xp')
    resistance = monster.get('resistance')
    state = monster.get('state')

    fighter_component = Fighter(hp=hp, str=str, dex=dex, defense=defense, resistance=resistance, xp=xp)
    ai_component = ai
    death_component = Death(death_function)

    monster_to_return = Entity(x, y, aspect, color, name, blocks=True, render_order=RenderOrder.ACTOR,
                               fighter=fighter_component, ai=ai_component, death=death_component)

    return monster_to_return
