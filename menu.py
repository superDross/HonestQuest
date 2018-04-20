from termios import tcflush, TCIFLUSH
from restructure_test import Hero, EnemyFactory
from print_text import print_centre
from common import weighted_choice
import time
import sys
import os
import re


# menu/menu.py
class Menu(object):
    ''' Base class for all menus.

    Attributes:
        _options (dict): {option (str): method (func)}
        choices (str): string representation of _options
    '''

    def __init__(self, options, choices):
        self._options = options
        self.choices = choices

    def handle_options(self):
        ''' Extract and execute a method from self._options.'''
        try:
            print_centre(self.choices)
            choice = input('>> ')
            item = self._options[choice]
            return item
        except KeyError:
            msg = '{} is not a valid choice. Try again.\n'
            print_centre(msg.format(choice))
            self.sleep()
            return self.handle_options()

    def sleep(self):
        time.sleep(1.5)

    @classmethod
    def from_list(cls, l):
        ''' Constructs self._options and self.choices from a list.

        Args:
            l (list: str): list of strings to transform into a Menu.
        '''
        options = {str(k + 1): i for k, i in enumerate(l)}
        choices = '\n'.join('{}. {}'.format(k, i)
                            for k, i in sorted(options.items()))
        return cls(options, choices)


class SubMenu(Menu):
    ''' Base class for a Menu underneath a parent Menu.

    Attributes:
        parent (Menu): menu object above this sub menu
        _options (dict): {option (str): method (func)}
        choices (str): string representation of _options
    '''

    def __init__(self, options, choices, parent):
        self.parent = parent
        self.options = self.add_parent_to_options(options)
        self.choices = self.add_back_to_choices(choices)
        Menu.__init__(self, self.options, self.choices)

    def add_parent_to_options(self, options):
        ''' Modify options to include parent menu.'''
        if not isinstance(self.parent, Menu):
            raise ValueError('{} is not Menu type'.format(self.parent))
        number_options = len(options)
        new_option_key = str(number_options + 1)
        options[new_option_key] = self.parent
        return options

    def add_back_to_choices(self, choices):
        ''' Modify choices to ince back option.'''
        num = len(self.options)
        return choices + '\n{}. Back'.format(num)


# menu/battle_menu.py
class MagicMenu(SubMenu):
    ''' Menu allowing player to select and use Hero magic.

    Attributes:
        hero (Hero): the players avatar object.
        enemy (Enemy): the players enemy.
        parent (BaseMenu): menu above this menu.
        all_magic (list: Magic): list of all hero.magic methods available.
    '''

    def __init__(self, parent, hero, enemy):
        self.hero = hero
        self.enemy = enemy
        self.all_magic = self._get_all_magic()
        options = self._magic_spell_options()
        choices = self._magic_spell_string()
        SubMenu.__init__(self, options, choices, parent)

    def _get_all_magic(self):
        ''' Returns all heros magic spells and stores in a list.
            E.g.
                [self.hero.magic.fireball, self.hero.magic.heal]
        '''
        all_magic = [x for x in dir(self.hero.magic)
                     if not re.search(r'_|hero|character', x)]
        return all_magic

    def _magic_spell_options(self):
        ''' Returns dict that has numbers (k) assigned to
            heros magic spell methods (v).
            E.g.
                {'1': self.hero.magic.fireball,
                 '2': self.hero.magic.heal}
        '''
        options = {str(k + 1): getattr(self.hero.magic, v)
                   for k, v in enumerate(self.all_magic)}
        return options

    def _magic_spell_string(self):
        ''' Return all magic spells as a string with numbers.
            E.g.
                '1. Fireball\n2. Heal'
        '''
        all_magic_num = ['{}. {}'.format(x + 1, y.title())
                         for x, y in enumerate(self.all_magic)]
        return '\n'.join(all_magic_num)


class TopMenu(Menu):
    ''' Top level battle menu.

    Holds all battle sub-menus in its _options
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
        self.magic_menu = MagicMenu(self, hero, enemy)
        self.item_menu = None
        options = {'1': self.attack,
                   '2': self.magic_menu,
                   '3': self.item_menu,
                   '4': self.flee}
        choices = '1. Attack\n2. Magic\n3. Items\n4. Flee'
        Menu.__init__(self, options, choices)

    def attack(self):
        ''' Attack enemy.'''
        self.hero.attack(self.enemy)
        self.sleep()

    def flee(self):
        ''' Attempt to run from battle.'''
        print_centre('{} attempts to flee!\n'.format(self.hero.name))
        self.sleep()
        # 20% chance of fleeing
        weighted_success = {True: 2, False: 8}
        flee_success = weighted_choice(weighted_success)
        if flee_success:
            print_centre('{} successfully ran away!\n'.format(self.hero.name))
            sys.exit()
        else:
            print_centre("{} couldn't get away!\n".format(self.hero.name))
            return


# battle/battle_sequence.py
class BattleSequence(object):
    ''' Ititiates battle.

    Attributes:
        hero (Hero): the players avatar object.
        enemy (Enemy): the players enemy.
        main_menu (TopMenu): top level battle menu.
        magic_menu (MagicMenu): hero magic selection menu.
        item_menu (ItemMenu): hero item selection menu.

    Usage:
        battle = BattleSequence(hero_obj, enemy_obj)
        battle.execute_main_menu()
    '''

    def __init__(self, hero, enemy):
        self.hero = hero
        self.enemy = enemy
        self.main_menu = TopMenu(hero, enemy)
        self.magic_menu = self.main_menu.magic_menu
        self.item_menu = self.main_menu.item_menu

    def construct_battle_screen(self):
        ''' Clears screen and input, prints characters stats and animations.'''
        os.system('clear')
        print_centre(self.enemy.animation)
        print_centre('\n{}\n{}\n'.format(self.hero, self.enemy))
        tcflush(sys.stdin, TCIFLUSH)  # clears input

    def execute_main_menu(self):
        ''' Executes battle sequence.'''
        while not self.hero.dead and not self.enemy.dead:
            self.construct_battle_screen()
            option = self.main_menu.handle_options()
            choice = None
            if option == self.magic_menu:
                choice = self.execute_magic_menu()
            else:
                choice = option()
            if choice != self.main_menu:
                self.enemy.ai(self.hero)
            self.transfer_gold_exp()

    def execute_magic_menu(self):
        ''' Executes player magic spell choice and target selection.'''
        self.construct_battle_screen()
        magic = self.magic_menu.handle_options()
        if magic != self.magic_menu.parent:
            target = self.select_target()
            magic(target)
            self.magic_menu.sleep()
        else:
            return self.magic_menu.parent

    def select_target(self):
        ''' Generates a Menu that asks user to select hero
            or enemy attribute and returns choice.
        '''
        print_centre('Select target:\n')
        target_menu = Menu.from_list([self.hero, self.enemy])
        target = target_menu.handle_options()
        return target

    def transfer_gold_exp(self):
        ''' Transfer gold and exp from enemy to hero if enemy is dead.'''
        if self.enemy.dead:
            msg = '{} recieved {} exp and {} gold!\n'
            msg = msg.format(self.hero.name, self.enemy.exp, self.enemy.gold)
            print_centre(msg)
            self.hero.exp += self.enemy.exp
            self.hero.gold += self.enemy.gold


# Create Objects
factory = EnemyFactory(2, 'Goblin')
enemy = factory.generate()
guy = Hero('Guy', 1)

# Set HP & MP for Test
guy.mp = 200
guy.hp = 200
guy.st = 5
enemy.mp = 200
enemy.exp = 200


m = BattleSequence(guy, enemy)
m.execute_main_menu()
