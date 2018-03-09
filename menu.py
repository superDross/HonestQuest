''' Class for battle menu.'''
import os
import re
import time
from protagonist import Human
from enemies import Rodent


class Menu(object):
    def __init__(self, hero, target):
        hero.target = target
        target.target = hero
        self.hero = hero
        self.target = target
        self.all_magic = self._get_all_magic()
        self._choice = None

    def _print_stats(func):
        ''' Decorator that prints stuff and clears
            screen after every action.'''
        def inner(self):
            if self.hero.target.dead:
                time.sleep(4)
                return None
            os.system('clear')
            print('\n{}\n{}\n'.format(self.hero, self.hero.target))
            func(self)
            self.choice = None
            self.battle_menu()
        return inner

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, value):
        ''' Ensures choice is a digit before setting.'''
        if value:
            if value.isdigit():
                self._choice = value
            else:
                print('Enter a digit')
                self.choice = input('>> ')

    def _get_all_magic(self):
        ''' Returns all heros magic spells and stores in a list.'''
        all_magic = [x for x in dir(self.hero.magic)
                     if not re.search(r'_|hero', x)]
        return all_magic

    def _magic_spell_string(self):
        ''' Return all magic spells as a string with numbers.'''
        numbers = range(1, len(self.all_magic) + 2)
        options = self.all_magic + ['Back']
        all_magic_num = ['{}. {}'.format(x, y)
                         for x, y in zip(numbers, options)]
        return '\n'.join(all_magic_num)

    def _magic_spell_dict(self):
        ''' Dict that has numbers (k) assigned to
            heros magic spell methods (v).'''
        numbers = range(1, len(self.all_magic) + 1)
        d = {str(k): getattr(self.hero.magic, v)
             for k, v in zip(numbers, self.all_magic)}
        # add an extra option for going back to the battle_menu
        d[str(max(numbers) + 1)] = self.battle_menu
        return d

    @_print_stats
    def battle_menu(self):
        ''' Main battle menu.'''
        print('1. Attack\n2. Magic\n3. Item')
        self.choice = input('>> ')
        self.exec_menu()

    @_print_stats
    def magic_menu(self):
        ''' Submenu for magic spells.'''
        magic_dict = self._magic_spell_dict()
        print(self._magic_spell_string())
        self.choice = input('>> ')
        spell = magic_dict[self.choice]
        spell()
        self.enemy_turn()

    def attack(self):
        self.hero.attack(self.hero.target)
        self.enemy_turn()

    def exec_menu(self):
        # need to add items
        exec_dict = {'1': self.attack,
                     '2': self.magic_menu}
        action = exec_dict[self.choice]
        action()

    def enemy_turn(self):
        if not self.target.dead:
            self.target.attack(self.target.target)


if __name__ == '__main__':
    guy = Human('Guy', 2)
    rat = Rodent('Rat', 10)
    menu = Menu(guy, rat)
    menu.battle_menu()
