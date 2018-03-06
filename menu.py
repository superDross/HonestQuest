''' Class for battle menu.'''
import os
import re
from protagonist import Human
from enemies import Rodent


class Menu(object):
    def __init__(self, character, target):
        self.character = character
        self.target = target
        self.all_magic = self._get_all_magic()
        self.choice = None

    def _print_stats(func):
        ''' Decorator that prints stuff and clears
            screen after every action.'''

        def inner(self):
            os.system('clear')
            print('\n{}\n{}\n'.format(self.character, self.target))
            func(self)
            self.choice = None
            self.battle_menu()
        return inner

    def _get_all_magic(self):
        ''' Returns all characters magic as a list.'''
        all_magic = [x for x in dir(self.character.magic)
                     if not re.search(r'_|character', x)]
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
            characters magic spell methods (v).'''
        numbers = range(1, len(self.all_magic) + 1)
        d = {str(k): getattr(self.character.magic, v)
             for k, v in zip(numbers, self.all_magic)}
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

    def attack(self):
        self.character.attack(self.target)

    def exec_menu(self):
        exec_dict = {'1': self.attack,
                     '2': self.magic_menu}
        action = exec_dict[self.choice]
        action()


if __name__ == '__main__':
    guy = Human('Guy', 2)
    rat = Rodent('Rat', 10)
    menu = Menu(guy, rat)
    menu.battle_menu()
