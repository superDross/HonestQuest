from termios import tcflush, TCIFLUSH
from restructure_test import Hero, EnemyFactory
from print_text import print_centre
import time
import sys
import os
import re

MSG_TIME = 1.5


# menu/menu.py
class Menu(object):
    ''' Base class for all menus.

    Attributes:
        _options (dict): {option (str): method (func)}
    '''

    def __init__(self, options, choices):
        self._options = options
        self.choices = choices

    def __call__(self):
        self.handle_options()

    def handle_options(self):
        ''' Extract and execute a method from self._options.

        Args:
            option (str): should be a key within self._options.
        '''
        try:
            print_centre(self.choices)
            choice = input('>> ')
            item = self._options[choice]
            return item
        except KeyError:
            msg = '{} is not a valid choice. Try again.'
            print_centre(msg.format(choice))
            time.sleep(MSG_TIME)
            self.handle_options()

    @classmethod
    def from_list(cls, l):
        options = {str(k + 1): i for k, i in enumerate(l)}
        choices = '\n'.join('{}. {}'.format(k, i)
                            for k, i in sorted(options.items()))
        return cls(options, choices)


# menu/battle_menu.py
class BattleMenu(object):
    ''' Base class for all menus used during the battle sequence.

    Attributes:
        hero (Hero): the players avatar object.
        target (Enemy): the players in battle enemy.
    '''

    def __init__(self, hero, enemy, options, choices):
        self._options = options
        self.choices = choices
        self.hero = hero
        self.enemy = enemy

    def construct_battle_screen(self):
        # if self.enemy.dead removed, may casue a BUG
        os.system('clear')
        print_centre(self.enemy.animation)
        print_centre('\n{}\n{}\n'.format(self.hero, self.enemy))
        tcflush(sys.stdin, TCIFLUSH)  # clears input

    def handle_options(self):
        ''' Extract and execute a method from self._options.

        Args:
            option (str): should be a key within self._options.
        '''
        try:
            self.construct_battle_screen()
            print_centre(self.choices)
            choice = input('>> ')
            item = self._options[choice]
            return item
        except KeyError:
            msg = '{} is not a valid choice. Try again.'
            print_centre(msg.format(choice))
            time.sleep(MSG_TIME)
            self.handle_options()

    def select_target(self):
        print_centre('Select target:\n')
        target_menu = Menu.from_list([self.hero, self.enemy])
        target = target_menu.handle_options()
        return target

    # handle_options = construct_battle_screen(Menu.handle_options)


class MainMenu(BattleMenu):
    def __init__(self, hero, enemy):
        self.magic_menu = MagicMenu(self, hero, enemy)
        options = {'1': self.attack,
                   '2': self.magic_menu,
                   '3': None}  # item menu
        choices = '1. Attack\n2. Magic\n3. Items'
        BattleMenu.__init__(self, hero, enemy, options, choices)

    def __call__(self):
        while not self.hero.dead and not self.enemy.dead:
            self.construct_battle_screen()
            option = self.handle_options()
            choice = option()
            if choice != self:
                self.enemy.ai(self.hero)
            return self.__call__()

    def attack(self):
        self.hero.attack(self.enemy)
        time.sleep(MSG_TIME)


class MagicMenu(BattleMenu):
    def __init__(self, parent, hero, enemy):
        self.parent = parent
        self.all_magic = self._get_all_magic(hero)
        options = self._magic_spell_dict(hero)
        choices = self._magic_spell_string()
        BattleMenu.__init__(self, hero, enemy, options, choices)

    def __call__(self):
        self.construct_battle_screen()
        magic = self.handle_options()
        if magic != self.parent:
            target = self.select_target()
            magic(target)
            time.sleep(MSG_TIME)
        else:
            return self.parent

    def _get_all_magic(self, hero):
        ''' Returns all heros magic spells and stores in a list.'''
        all_magic = [x for x in dir(hero.magic)
                     if not re.search(r'_|hero|character', x)]
        return all_magic

    def _magic_spell_dict(self, hero):
        ''' Returns dict that has numbers (k) assigned to
            heros magic spell methods (v).
            E.g.
                {'1': self.hero.magic.fireball,
                 '2': self.hero.magic.heal}
        '''
        numbers = range(1, len(self.all_magic) + 1)
        d = {str(k): getattr(hero.magic, v)
             for k, v in zip(numbers, self.all_magic)}
        # adds an extra option for going back to the battle_menu
        d[str(max(numbers) + 1)] = self.parent
        return d

    def _magic_spell_string(self):
        ''' Return all magic spells as a string with numbers.
            E.g.
                '1. Fireball\n2. Heal'
        '''
        numbers = range(1, len(self.all_magic) + 2)
        options = self.all_magic + ['Back']
        all_magic_num = ['{}. {}'.format(x, y.title())
                         for x, y in zip(numbers, options)]
        return '\n'.join(all_magic_num)


# Create Objects
factory = EnemyFactory(2, 'Goblin')
enemy = factory.generate()
guy = Hero('Guy', 7)

# Set HP & MP for Test
guy.mp = 200
guy.hp = 5
guy._max_hp = 5
enemy.mp = 200


m = MainMenu(guy, enemy)
m()
