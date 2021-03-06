import libtcodpy as libtcod

from loader_functions.scores_loader import read_score_bill


def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create a off screen console for menu s window
    window = libtcod.console_new(width, height)

    # print t header with auto wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ')' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(con, header, player, inventory, inventory_width, screen_width, screen_height):
    if len(inventory.items) == 0:
        options = ['inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{} (on main hand.)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{} (on off hand.)'.format(item.name))
            # v15 Stack system.
            elif item.item.stack > 1:
                options.append('{} ( {} )'.format(item.name, str(item.item.stack)))
            else:
                print('INFO : Pas de stack. ', item)
                options.append(item.name)

    menu(con, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, background_image, screen_width, screen_height, version):
    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'TOMBS OF THE ANCIENT KINGS')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE,
                             libtcod.CENTER, version)

    menu(con, ' ', ['Play a new game', 'Continue last game', 'Score', 'Quit'], 24, screen_width, screen_height)


# v14
def score_bill_menu(background_image, screen_width, screen_height):

    score_list = read_score_bill()

    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 4) - 4, libtcod.BKGND_NONE,
                             libtcod.CENTER, 'BEST SCORES')

    y = 0
    for line in score_list:
        row = line.split(',')
        x = 0
        for info in row:
            libtcod.console_print_ex(0, int(screen_width / 10) + x, int(screen_height / 4) + y, libtcod.BKGND_NONE, libtcod.CENTER, info)
            x += 13
        if y == 0:
            y += 2
        else:
            y += 1

    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE,
                             libtcod.CENTER, 'Press ESC for Main Menu')


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 hp, from {})'.format(player.fighter.base_max_hp),
               'Strength (+1 str, from {})'.format(player.fighter.base_str),
               'Dexterity (+1 dex, from {})'.format(player.fighter.base_dex)]

    menu(con, header, options, menu_width, screen_width, screen_height)


def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):

    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '----- ' + player.name + ' -----')
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Level : {}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience : {}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 5, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience to level : {}'.format(
            player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Strength: {} + {}'.format(player.fighter.base_str,
                                                                           player.equipment.str_bonus))
    libtcod.console_print_rect_ex(window, 0, 9, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Dexterity: {} + {}'.format(player.fighter.base_dex,
                                                                            player.equipment.dex_bonus))
    libtcod.console_print_rect_ex(window, 0, 11, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Resistance : {}'.format(player.fighter.resistance))
    libtcod.console_print_rect_ex(window, 0, 12, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defense : {}'.format(player.fighter.defense))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)


def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)


# v14.
def victory_screen(character_screen_width, character_screen_height, screen_width, screen_height):

    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'VICTORY !!')
    libtcod.console_print_rect_ex(window, 0, 5, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'The Ancient King of the Horde is dead!')

    libtcod.console_print_rect_ex(window, 0, 9, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Press ESC to quit this game.')

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2

    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)


# v14
def character_creation_menu(background_image, screen_width, screen_height, character_name):

    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 4) - 4, libtcod.BKGND_NONE,
                             libtcod.CENTER, 'NEW GAME : CREATION SCREEN')

    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 4), libtcod.BKGND_NONE,
                             libtcod.CENTER, character_name)

    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 5), libtcod.BKGND_NONE,
                             libtcod.CENTER, 'Press ENTER to validate')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 4), libtcod.BKGND_NONE,
                             libtcod.CENTER, 'Press ESC for Main Menu')

