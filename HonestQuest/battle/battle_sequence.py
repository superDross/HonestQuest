from HonestQuest.utils.print_text import print_centre
from HonestQuest.menus.battle_menus import TopMenu
from HonestQuest.menus.menu import Menu
from HonestQuest.utils import common


class BattleSequence(object):
    ''' Ititiates battle.

    Attributes:
        hero (Hero): the players avatar object.
        enemy (Enemy): the players enemy.
        main_menu (TopMenu): top level battle menu.
        magic_menu (MagicMenu): hero magic selection menu.
        item_menu (ItemMenu): hero item selection menu.

    Usage:
        battle = BattleSequence(hero_obj, enemy_obj)
        battle.execute_main_menu()
    '''

    def __init__(self, hero, enemy):
        self.hero = hero
        self.enemy = enemy
        self.main_menu = TopMenu(hero, enemy)

    def __call__(self):
        self.execute_main_menu()

    def construct_battle_screen(self):
        ''' Clears screen and input, prints characters stats and animations.'''
        common.clear()
        print_centre(self.enemy.animation)
        print_centre('\n{}\n{}\n'.format(self.hero, self.enemy))
        common.flush_input()

    def execute_main_menu(self):
        ''' Executes battle sequence starting at the main battle menu.'''
        while not self.hero.dead and not self.enemy.dead:
            self.construct_battle_screen()
            option = self.main_menu.handle_options()
            choice = None
            if option in [self.main_menu.item_menu, self.main_menu.magic_menu]:
                choice = self.execute_submenu(option)
            else:
                choice = option()
            if choice != self.main_menu:
                self.enemy.ai(self.hero)
            self.transfer_gold_exp()
            # recontruct all battle menus.
            self.main_menu = TopMenu(self.hero, self.enemy)

    def execute_submenu(self, submenu):
        ''' Executes player submenu choice and target selection.'''
        self.construct_battle_screen()
        submenu_selection = submenu.handle_options()
        if submenu_selection != self.main_menu:
            target = self.select_target()
            if submenu == self.main_menu.item_menu:
                self.hero.inventory.use_item(submenu_selection.name, target)
            else:
                print('other')
                submenu_selection(target)
            common.sleep()
        else:
            return self.main_menu

    def select_target(self):
        ''' Generates a Menu that asks user to select hero
            or enemy attribute and returns choice.
        '''
        print_centre('Select target:\n')
        target_menu = Menu.from_list([self.hero, self.enemy])
        target = target_menu.handle_options()
        return target

    def transfer_gold_exp(self):
        ''' Transfer gold and exp from enemy to hero if enemy is dead.'''
        if self.enemy.dead:
            msg = '{} recieved {} exp and {} gold!\n'
            msg = msg.format(self.hero.name, self.enemy.exp, self.enemy.gold)
            print_centre(msg)
            self.hero.exp += self.enemy.exp
            self.hero.gold += self.enemy.gold
            common.sleep()
