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

    def __call__(self):
        self.handle_options()

    def handle_options(self):
        ''' Extract and execute a method from self._options.'''
        try:
            print_centre(self.choices)
            choice = input('>> ')
            item = self._options[choice]
            return item
        except KeyError:
            msg = '{} is not a valid choice. Try again.'
            print_centre(msg.format(choice))
            self.sleep()
            self.handle_options()

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


# menu/battle_menu.py
class BaseMenu(Menu):
    ''' Base class for all menus used during the battle sequence.

    Attributes:
        hero (Hero): the players avatar object.
        target (Enemy): the players in battle enemy.
    '''
    def __init__(self, hero, enemy, options, choices):
        '''Parameters:
              _options (dict): {option (str): method (func)}
              choices (str): string representation of _options
        '''
        Menu.__init__(self, options, choices)
        self.hero = hero
        self.enemy = enemy

    def construct_battle_screen(self):
        ''' Clears screen and input, prints characters stats and animations.'''
        os.system('clear')
        print_centre(self.enemy.animation)
        print_centre('\n{}\n{}\n'.format(self.hero, self.enemy))
        tcflush(sys.stdin, TCIFLUSH)  # clears input

    def handle_options(self):
        ''' Extract and execute a method from self._options.'''
        self.construct_battle_screen()
        return Menu.handle_options(self)

    def select_target(self):
        ''' Generates a Menu that asks user to select hero
            or enemy attribute and returns choice.
        '''
        print_centre('Select target:\n')
        target_menu = Menu.from_list([self.hero, self.enemy])
        target = target_menu.handle_options()
        return target


class MainMenu(BaseMenu):
    ''' Top battle menu which executes the battle sequence.

    Attributes:
        magic_menu (MagicMenu): submenu for Hero magic.
        item_menu (ItemMenu): submenu for Hero items.

    Usage:
        battle = MainMenu(hero_obj, enemy_obj)
        battle()
    '''
    def __init__(self, hero, enemy):
        ''' Parameters:
                hero (Hero): the players avatar object.
                enemy (Enemy): the players enemy.
        '''
        self.magic_menu = MagicMenu(self, hero, enemy)
        self.item_menu = None
        # self.main_menu = MainMenu(hero, enemy)
        options = {'1': self.attack,
                   '2': self.magic_menu,
                   '3': self.item_menu,
                   '4': self.flee}
        choices = '1. Attack\n2. Magic\n3. Items\n4. Flee'
        BaseMenu.__init__(self, hero, enemy, options, choices)

    def __call__(self):
        ''' Executes battle sequence.'''
        while not self.hero.dead and not self.enemy.dead:
            self.construct_battle_screen()
            option = self.handle_options()
            choice = option()
            self.transfer_gold_exp()
            if choice != self:
                self.enemy.ai(self.hero)

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

    def transfer_gold_exp(self):
        ''' Transfer gold and exp from enemy to hero if enemy is dead.'''
        if self.enemy.dead:
            msg = '{} recieved {} exp and {} gold!\n'
            msg = msg.format(self.hero.name, self.enemy.exp, self.enemy.gold)
            print_centre(msg)
            self.hero.exp += self.enemy.exp
            self.hero.gold += self.enemy.gold


class MagicMenu(BaseMenu):
    ''' Menu allowing player to select and use Hero magic.

    Attributes:
        parent (BaseMenu): menu above this menu.
        all_magic (list: Magic): list of all hero.magic methods available.
    '''
    def __init__(self, parent, hero, enemy):
        ''' Parameters:
                hero (Hero): the players avatar object.
                enemy (Enemy): the players enemy.
        '''
        self.parent = parent
        self.all_magic = self._get_all_magic(hero)
        options = self._magic_spell_dict(hero)
        choices = self._magic_spell_string()
        BaseMenu.__init__(self, hero, enemy, options, choices)

    def __call__(self):
        ''' Executes player magic spell choice and target selection.'''
        self.construct_battle_screen()
        magic = self.handle_options()
        if magic != self.parent:
            target = self.select_target()
            magic(target)
            self.sleep()
        else:
            return self.parent

    def _get_all_magic(self, hero):
        ''' Returns all heros magic spells and stores in a list.
            E.g.
                [self.hero.magic.fireball, self.hero.magic.heal]
        '''
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
guy = Hero('Guy', 1)

# Set HP & MP for Test
guy.mp = 200
guy.hp = 200
guy.st = 10
enemy.mp = 200
enemy.exp = 200


m = MainMenu(guy, enemy)
m()
