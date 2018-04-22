from termios import tcflush, TCIFLUSH
from print_text import print_centre
from animations import animations
from battle_menu import Menu
from items import Item
import sys
import os


class Store(Menu):
    def __init__(self, hero):
        Menu.__init__(self, hero)
        self._welcome_message()
        self.shopkeep = animations['shopkeep']
        self.main_menu = self.store_menu()
        self.item = None

    def _print_shopkeep(func):
        ''' Decorator that print_centres stuff and clears
            screen after every action.'''
        def inner(self):
            os.system('clear')
            print_centre(self.shopkeep)
            tcflush(sys.stdin, TCIFLUSH)  # clears input
            func(self)
            self._choice = None
            self.store_menu()
        return inner

    @_print_shopkeep
    def _welcome_message(self):
        print_centre('Welcome to my store warrior!')

    @_print_shopkeep
    def store_menu(self):
        print_centre('What would you like to purchase?')
        print_centre('1. Potion\n2. Ether\n3. Steroids\n4.Cocaine')
        self.choice = input('>> ')
        exec_dict = {'1': Item('Potion', 'hp', 50, 'Increase HP by 50.'),
                     '2': Item('Ether', 'mp', 10, 'Increase MP by 10.'),
                     '3': Item('Steroids', 'st', 20, 'Increase ST by 20.'),
                     '4': Item('Cocaine', 'ag', 20, 'Increase AG by 20.')}
        self.item = self.get_menu_item(exec_dict)

    def _check_price(self):
        price = self._item_price(self.item)
        if self.hero.gold > price:
            self.hero.gold -+ price
            self.hero.inventory = self.item
            # some message
        else:
            # some message(cant buy that)
            return


    def _item_price(self):
        price_list = {'Potion': 50, 'Ether': 500,
                      'Steroids': 1500, 'Cocaine': 3000}
        return price_list[self.item]

