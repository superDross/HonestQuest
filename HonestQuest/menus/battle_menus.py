from HonestQuest.menus.menu import Menu, SubMenu
from HonestQuest.utils.print_text import print_centre
import HonestQuest.utils.common as common
import re


class MagicMenu(SubMenu):
    ''' Menu allowing player to select and use Hero magic.

    Attributes:
        hero (Hero): the players avatar object.
        enemy (Enemy): the players enemy.
        all_magic (list: Magic): list of all hero.magic methods available.
    '''
    def __init__(self, hero, parent_menu):
        self.hero = hero
        self.all_magic = self._get_all_magic()
        options = self._magic_spell_options()
        choices = self._magic_spell_string()
        SubMenu.__init__(self, options, choices, parent_menu)

    def _get_all_magic(self):
        ''' Returns all heros magic spells and stores in a list.
            e.g. [self.hero.magic.fireball, self.hero.magic.heal]
        '''
        all_magic = [x for x in dir(self.hero.magic)
                     if not re.search(r'_|hero|character', x)]
        return all_magic

    def _magic_spell_options(self):
        ''' Returns dict that has numbers (k) assigned to
            heros magic spell methods (v).
            e.g. {'1': self.hero.magic.fireball,
                  '2': self.hero.magic.heal}
        '''
        options = {str(k + 1): getattr(self.hero.magic, v)
                   for k, v in enumerate(self.all_magic)}
        return options

    def _magic_spell_string(self):
        ''' Return all magic spells as a string with numbers.
            e.g. '1. Fireball\n2. Heal'
        '''
        all_magic_num = ['{}. {}'.format(x + 1, y.title())
                         for x, y in enumerate(self.all_magic)]
        return '\n'.join(all_magic_num)


class ItemMenu(SubMenu):
    def __init__(self, hero, parent_menu):
        self.hero = hero
        choices, options = self._get_choices_options()
        SubMenu.__init__(self, options, choices, parent_menu)
        # Below classmethod init doesn't work due to multiple inheritence?
        # SubMenu.from_list(hero.inventory, parent_menu)

    def _get_choices_options(self):
        # Menu.from_list() temp replacement
        if self.hero.inventory:
            choices = '\n'.join(['{}. {}'.format(x + 1, y.name)
                                 for x, y in enumerate(self.hero.inventory)])
            options = {str(k + 1): v
                       for k, v in enumerate(self.hero.inventory)}
            return (choices, options)
        else:
            return ({}, {})


class TopMenu(Menu):
    ''' Top level battle menu.

    Holds all battle SubMenus in its _options
    attribute.

    Attributes:
        hero (Hero): the players avatar object.
        enemy (Enemy): the players enemy.
        magic_menu (MagicMenu): submenu for Hero magic.
        item_menu (ItemMenu): submenu for Hero items.
    '''

    def __init__(self, hero, enemy):
        self.hero = hero
        self.enemy = enemy
        self.magic_menu = MagicMenu(hero, self)
        self.item_menu = ItemMenu(hero, self)
        options = {'1': self.attack,
                   '2': self.magic_menu,
                   '3': self.item_menu,
                   '4': self.flee}
        choices = '1. Attack\n2. Magic\n3. Items\n4. Flee'
        Menu.__init__(self, options, choices)

    def attack(self):
        ''' Attack enemy.'''
        self.hero.attack(self.enemy)
        common.sleep()

    def flee(self):
        ''' Attempt to run from battle.'''
        print_centre('{} attempts to flee!'.format(self.hero.name))
        common.sleep()
        # 20% chance of fleeing
        weighted_success = {True: 2, False: 8}
        flee_success = common.weighted_choice(weighted_success)
        if flee_success:
            print_centre('{} successfully ran away!\n'.format(self.hero.name))
            common.sleep()
            return True
        else:
            print_centre("{} couldn't get away!\n".format(self.hero.name))
            common.sleep()
            return False
