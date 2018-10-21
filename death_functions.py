import libtcodpy as libtcod

from menus import message_box
from game_messages import Message
from game_states import GameStates
from render_functions import RenderOrder


def kill_player(player, game_state):
    player.char = '%'
    player.color = libtcod.dark_red

    return Message('You died', libtcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster, game_state):
    death_message = Message('{} is dead!'.format(monster.name.capitalize()), libtcod.orange)

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message, game_state


def kill_final_boss(monster, game_state):
    death_message = Message('The {} has been vanquished! The threath is over! VICTORY!'.
                            format(monster.name.capitalize(), libtcod.lightest_yellow))

    monster.char = '%'
    monster.color = libtcod.dark_red

    return death_message, GameStates.VICTORY