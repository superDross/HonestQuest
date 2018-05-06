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
        # perhaps the if-elif statements could be placed into their respective
        # classes as modified self.handle_options() methods.
        if submenu_selection == self.main_menu:
            return self.main_menu
        elif submenu == self.main_menu.buy_menu:
            deduction = self.hero.gold - submenu_selection.cost
            if deduction > 0:
                self.hero.inventory.add_items(submenu_selection)
                if self.hero.inventory.full is False:
                    self.hero.gold = deduction
                    print_centre('Enjoy your {}!'.format(
                        submenu_selection.name))
                    common.sleep()
            else:
                print_centre("You don't have enough gold to purchase that!")
                common.sleep()
        elif submenu == self.main_menu.sell_menu:
            self.hero.inventory.remove_item(submenu_selection.name)
            self.hero.gold += submenu_selection.sell
            print_centre('Thank you for selling your {} to me!'.format(
                submenu_selection.name))
            common.sleep()
