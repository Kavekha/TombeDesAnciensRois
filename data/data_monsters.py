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
            'hp': 140,
            'str': 30,
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
        },
        'rat': {
            'name': 'Rat',
            'aspect': 'r',
            'color': libtcod.darkest_green,
            'death_function': kill_monster,
            'ai': BasicMonster(),
            'hp': 10,
            'str': 3,
            'dex': 12,
            'defense': 0,
            'resistance': 0,
            'xp': 30
        },
        'goblin': {
            'name': 'Goblin',
            'aspect': 'G',
            'color': libtcod.green,
            'death_function': kill_monster,
            'ai': BasicMonster(),
            'hp': 20,
            'str': 7,
            'dex': 6,
            'defense': 1,
            'resistance': 0,
            'xp': 56
        },
        'skeleton': {
            'name': 'Squelette',
            'aspect': 's',
            'color': libtcod.dark_gray,
            'death_function': kill_monster,
            'ai': BasicMonster(),
            'hp': 20,
            'str': 3,
            'dex': 2,
            'defense': 2,
            'resistance': 0,
            'xp': 28
        },
        'zombie': {
            'name': 'Zombie',
            'aspect': 'z',
            'color': libtcod.dark_amber,
            'death_function': kill_monster,
            'ai': BasicMonster(),
            'hp': 40,
            'str': 9,
            'dex': 1,
            'defense': 2,
            'resistance': 0,
            'xp': 96
        },
        'chauvesouris': {
            'name': 'Chauve-souris',
            'aspect': 'w',
            'color': libtcod.dark_blue,
            'death_function': kill_monster,
            'ai': BasicMonster(),
            'hp': 10,
            'str': 2,
            'dex': 12,
            'defense': 0,
            'resistance': 0,
            'xp': 28
        },
        'fantome': {
            'name': 'Fantome',
            'aspect': 'F',
            'color': libtcod.dark_azure,
            'death_function': kill_monster,
            'ai': BasicMonster(),
            'hp': 60,
            'str': 9,
            'dex': 6,
            'defense': 3,
            'resistance': 0,
            'xp': 216
        },
        'mumy': {
            'name': 'Momie',
            'aspect': 'M',
            'color': libtcod.darkest_orange,
            'death_function': kill_monster,
            'ai': BasicMonster(),
            'hp': 120,
            'str': 18,
            'dex': 3,
            'defense': 5,
            'resistance': 0,
            'xp': 624
        },
        'vampire': {
            'name': 'Vampire',
            'aspect': 'V',
            'color': libtcod.dark_azure,
            'death_function': kill_monster,
            'ai': BasicMonster(),
            'hp': 90,
            'str': 12,
            'dex': 12,
            'defense': 4,
            'resistance': 0,
            'xp': 504
        },
        'ancient_king_necropole': {
            'name': 'Ancient King of the Necropole',
            'aspect': 'K',
            'color': libtcod.green,
            'death_function': kill_final_boss,
            'ai': BasicMonster(),
            'hp': 180,
            'str': 24,
            'dex': 24,
            'defense': 6,
            'resistance': 0,
            'xp': 0
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
