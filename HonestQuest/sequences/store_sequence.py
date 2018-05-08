from HonestQuest.animations.animations import animations
from HonestQuest.utils.print_text import print_centre
from HonestQuest.menus.store import StoreMenu
from HonestQuest.menus.menu import Menu
from HonestQuest.utils import common


class StoreSequence(object):
    ''' Initiates store.

    Attributes:
        hero (Character): the player avatar object.
        main_menu (StoreMenu): top level shop menu.
    '''

    def __init__(self, hero):
        self.hero = hero
        self.main_menu = StoreMenu(hero)

    def __call__(self):
        self.execute()

    def execute(self):
        ''' Executes store sequence starting at the main store menu.'''
        while self.main_menu.exit_status is False:
            self.main_menu = StoreMenu(self.hero)
            self.construct_store_screen()
            option = self.main_menu.handle_options()
            if isinstance(option, Menu) and option != self.main_menu:
                self.execute_submenu(option)
            else:
                option()

    def construct_store_screen(self):
        ''' Clears screen and input, prints store owner & available gold.'''
        common.clear()
        print_centre(animations.get('Shopkeep'))
        print_centre('{}:\t{} gold'.format(self.hero.name, self.hero.gold))
        print_centre('Welcome to my store! How may I serve you today?\n')
        common.flush_input()

    def execute_submenu(self, submenu):
        ''' Executes player submenu choice and item selection.

        Args:
            submenu (Menu): buy or sell submenu.
        '''
        self.construct_store_screen()
        submenu_selection = submenu.handle_options()
        if submenu_selection == self.main_menu:
            return self.main_menu
        elif submenu == self.main_menu.buy_menu:
            self.purchase(submenu_selection)
        elif submenu == self.main_menu.sell_menu:
            self.sell(submenu_selection)

    def purchase(self, item):
        ''' Transfers the item to the hero inventory and deducts
            the cost from the players gold attr.

        Args:
            item (Item): item to transfer.
        '''
        deduction = self.hero.gold - item.cost
        if deduction >= 0:
            self.hero.inventory.add_items(item)
            if self.hero.inventory.full is False:
                self.hero.gold = deduction
                print_centre('Enjoy your {}!'.format(item.name))
                common.sleep()
        else:
            print_centre("You don't have enough gold to purchase that!")
            common.sleep()

    def sell(self, item):
        ''' Removes the item from the heros inventory and adds
            the sell price of the item to the players sell attr.

        Args:
            item (Item): item to remove.
        '''
        self.hero.inventory.remove_item(item.name)
        self.hero.gold += item.sell
        print_centre('Thank you for selling your {} to me!'.format(
            item.name))
        common.sleep()
