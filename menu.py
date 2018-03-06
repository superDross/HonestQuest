import os
from protagonist import Human
from enemies import Rodent


class Menu(object):
    def __init__(self, character, target):
        self.character = character
        self.target = target
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

    @_print_stats
    def battle_menu(self):
        ''' Main battle menu.'''
        print('1. Attack\n2. Magic\n3. Item')
        self.choice = input('>> ')
        self.exec_menu()

    @_print_stats
    def magic_menu(self):
        ''' Submenu for magic spells.'''
        magic_dict = {'1': self.character.heal,
                      '2': self.character.rage,
                      '3': self.battle_menu}
        print('1. Heal\n2. Rage\n3. Back')
        self.choice = input('>> ')
        spell = magic_dict[self.choice]
        spell()

    def attack(self):
        self.character.attack(self.target)

    def exec_menu(self):
        # dict values executes all at once
        exec_dict = {'1': self.attack,
                     '2': self.magic_menu}
        action = exec_dict[self.choice]
        action()


guy = Human('Guy', 2)
rat = Rodent('Rat', 10)
menu = Menu(guy, rat)
menu.battle_menu()
