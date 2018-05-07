''' python3 ./test_modules.py -b '''
from HonestQuest.characters.enemy import EnemyFactory
from HonestQuest.characters.hero import Hero
from HonestQuest.items.items import Potion
from HonestQuest.menus import battle_menus
from HonestQuest.menus.menu import Menu
from HonestQuest.menus import store
from unittest.mock import patch
import unittest

# Create a menu for testing
option = {'1': 'A', '2': 'B'}
choices = '1. A\n2. B'
M = Menu(option, choices)

# Create a submenu for tesing
options = {'1': 'C', '2': 'D'}
choices = '1. C\n2. D'
SM = Menu(options, choices, M)

# Create a hero to test the StoreMenu
hero = Hero('Dummy', 1)
hero.inventory.add_items(Potion(), Potion())
STORE = store.StoreMenu(hero)

# Create an enemy to test the BattleMenu
factory = EnemyFactory()
enemy = factory.generate_enemy('Goblin', 1)
BATTLE = battle_menus.TopMenu(hero, enemy)


class TestMenu(unittest.TestCase):
    @patch('builtins.input', lambda _: '1')
    def test_menu_option_1(self):
        choice = M.handle_options()
        self.assertEqual(choice, 'A')

    @patch('builtins.input', lambda _: '2')
    def test_menu_option_2(self):
        choice = M.handle_options()
        self.assertEqual(choice, 'B')

    def test_from_list(self):
        l = ['A', 'B']
        new_menu = Menu.from_list(l)
        t = all([M.options == new_menu.options, M.choices == new_menu.choices])
        self.assertTrue(t)


class TestSubMenu(unittest.TestCase):
    @patch('builtins.input', lambda _: '3')
    def test_back(self):
        parent_menu = SM.handle_options()
        self.assertEqual(parent_menu.choices, M.choices)


class TestStoreMenu(unittest.TestCase):
    @patch('builtins.input', lambda _: '1')
    def test_enter_buy_menu(self):
        buy_menu = STORE.handle_options()
        self.assertEqual(type(buy_menu), store.BuyMenu)

    @patch('builtins.input', lambda _: '1')
    def test_buying_potion(self):
        buy_menu = STORE.handle_options()
        item_choice = buy_menu.handle_options()
        self.assertEqual(item_choice.name, 'Potion')

    @patch('builtins.input', lambda _: '2')
    def test_enter_sell_menu(self):
        sell_menu = STORE.handle_options()
        self.assertEqual(type(sell_menu), store.SellMenu)

    @patch('builtins.input', lambda _: '2')
    def test_selling_potion(self):
        sell_menu = STORE.handle_options()
        item_choice = sell_menu.handle_options()
        self.assertEqual(item_choice.name, 'Potion')

    def test_back_button(self):
        with patch('builtins.input', lambda _: '1') as o:
            buy_menu = STORE.handle_options()
            with patch('builtins.input', lambda _: '5') as p:
                main_menu = buy_menu.handle_options()
                self.assertEqual(type(main_menu), store.StoreMenu)

    @patch('builtins.input', lambda _: '3')
    def test_exit(self):
        exit_command = STORE.handle_options()
        exit_command()
        self.assertTrue(STORE.exit_status)

    def test_lv20_buy(self):
        hero = Hero('Big20', 20)
        new_store = store.StoreMenu(hero)
        with patch('builtins.input', lambda _: '1') as o:
            buy_menu = new_store.handle_options()
            with patch('builtins.input', lambda _: '8') as p:
                item_choice = buy_menu.handle_options()
                self.assertEqual(item_choice.name, 'Vodka Shots')


class TestBattleMenu(unittest.TestCase):
    @patch('builtins.input', lambda _: '1')
    def test_attack(self):
        attack_command = BATTLE.handle_options()
        self.assertEqual(attack_command, BATTLE.attack)

    def test_magic(self):
        with patch('builtins.input', lambda _: '2') as o:
            magic_menu = BATTLE.handle_options()
            with patch('builtins.input', lambda _: '1') as p:
                magic_choice = magic_menu.handle_options()
                self.assertEqual(magic_choice.__func__,
                                 BATTLE.hero.magic.heal.__func__)

    def test_item(self):
        with patch('builtins.input', lambda _: '3') as o:
            item_menu = BATTLE.handle_options()
            with patch('builtins.input', lambda _: '1') as p:
                item_choice = item_menu.handle_options()
                self.assertEqual(item_choice.name, 'Potion')

    @patch('builtins.input', lambda _: '4')
    def test_flee(self):
        flee_command = BATTLE.handle_options()
        flee_boolean = flee_command()
        self.assertTrue(type(flee_boolean) == bool)

    def test_lv20_buy(self):
        hero = Hero('Big20', 20)
        new_store = store.StoreMenu(hero)
        with patch('builtins.input', lambda _: '1') as o:
            item_menu = new_store.handle_options()
            with patch('builtins.input', lambda _: '8') as p:
                item_choice = item_menu.handle_options()
                self.assertEqual(item_choice.name, 'Vodka Shots')


if __name__ == '__main__':
    unittest.main()
