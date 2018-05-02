from HonestQuest.menus.battle_menus import ItemMenu
from HonestQuest.menus.menu import Menu, SubMenu
from HonestQuest.utils.common import merge_two_dicts
from HonestQuest.items import items


class BuyMenu(SubMenu):
    ''' Menu allowing player to select and buy items.

    Attributes:
        hero (Hero): the player avatar object.
    '''

    def __init__(self, hero, parent_menu):
        self.hero = hero
        options = self._set_options()
        choices = self._set_choices(options)
        SubMenu.__init__(self, options, choices, parent_menu)

    def _set_options(self):
        ''' Set the available items to buy, dependent upon hero level.'''
        options = {'1': items.Potion(),
                   '2': items.Ether(),
                   '3': items.ManaCleaner(),
                   '4': items.MegaPhone()}
        if self.hero.lv >= 10:
            lv10_options = {'5': items.ProteinShake(),
                            '6': items.RedBull()}
            options = merge_two_dicts(options, lv10_options)
        if self.hero.lv >= 15:
            lv15_options = {'7': items.Molotov()}
            options = merge_two_dicts(options, lv15_options)
        if self.hero.lv >= 20:
            lv20_options = {'8': items.VodkaShots()}
            options = merge_two_dicts(options, lv20_options)
        return options

    def _set_choices(self, options):
        ''' Set the choices for the Menu.'''
        choices = []
        for num, item in sorted(options.items()):
            selection = '{}. {}   {} gold'.format(num, item.name, item.cost)
            choices.append(selection)
        return '\n'.join(choices)


class SellMenu(ItemMenu):
    ''' Menu allowing player to select and sell their inventory items.

    Attributes:
        hero (Hero): the player avatar object.
    '''

    def __init__(self, hero, parent_menu):
        ItemMenu.__init__(self, hero, parent_menu)
        self._modify_choices()

    def _modify_choices(self):
        new_choices = []
        for num, item in enumerate(self.hero.inventory, 1):
            new_choice = '{}. {}   {} gold'.format(num, item.name, item.sell)
            new_choices.append(new_choice)
        self.choices = '\n'.join(new_choices)


class StoreMenu(Menu):
    ''' Top level store menu.

    Attributes:
        hero (Hero): the player avatar object.
    '''
    def __init__(self, hero):
        self.hero = hero
        self.buy_menu = BuyMenu(hero, self)
        self.sell_menu = SellMenu(hero, self)
        options = {'1': self.buy_menu,
                   '2': self.sell_menu,
                   '3': self.exit}
        choices = '1. Buy\n2. Sell\n3. Exit'
        Menu.__init__(self, options, choices)
        self.exit_status = False

    def exit(self):
        self.exit_status = True
