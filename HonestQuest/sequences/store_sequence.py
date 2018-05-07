from HonestQuest.animations.animations import animations
from HonestQuest.utils.print_text import print_centre
from HonestQuest.menus.store import StoreMenu
from HonestQuest.menus.menu import Menu
from HonestQuest.utils import common


class StoreSequence(object):
    def __init__(self, hero):
        self.hero = hero
        self.main_menu = StoreMenu(hero)

    def __call__(self):
        self.execute()

    def execute(self):
        while self.main_menu.exit_status is False:
            self.main_menu = StoreMenu(self.hero)
            self.construct_store_screen()
            option = self.main_menu.handle_options()
            if isinstance(option, Menu):
                self.execute_submenu(option)
            else:
                # exit
                option()

    def construct_store_screen(self):
        common.clear()
        print_centre(animations.get('Shopkeep'))
        print_centre('{}:\t{} gold'.format(self.hero.name, self.hero.gold))
        print_centre('Welcome to my store! How may I serve you today?\n')
        common.flush_input()

    def execute_submenu(self, submenu):
        self.construct_store_screen()
        submenu_selection = submenu.handle_options()
        if submenu_selection == self.main_menu:
            return self.main_menu
        elif submenu == self.main_menu.buy_menu:
            self.purchase(submenu_selection)
        elif submenu == self.main_menu.sell_menu:
            self.sell(submenu_selection)

    def purchase(self, item):
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
        self.hero.inventory.remove_item(item.name)
        self.hero.gold += item.sell
        print_centre('Thank you for selling your {} to me!'.format(
            item.name))
        common.sleep()
