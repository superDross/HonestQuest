from HonestQuest.sequences.store_sequence import StoreSequence
from HonestQuest.characters.hero import Hero
from HonestQuest.items import items
from unittest.mock import patch

import unittest


hero = Hero('Dummy', 1)
hero.gold += 1000

STORE = StoreSequence(hero)


class TestStoreBuyingSelling(unittest.TestCase):
    def test_buying_transfer(self):
        STORE.purchase(items.Potion())
        inv_list = [x.name for x in hero.inventory]
        self.assertTrue('Potion' in inv_list)

    def test_buying_cost(self):
        old_gold = hero.gold
        STORE.purchase(items.Potion())
        difference = old_gold - hero.gold
        self.assertEqual(difference, items.Potion().cost)

    def test_selling_transfer(self):
        old_inv_len = len(hero.inventory)
        STORE.sell(items.Potion())
        new_inv_len = len(hero.inventory)
        self.assertEqual(new_inv_len, (old_inv_len - 1))

    def test_selling_cost(self):
        old_gold = hero.gold
        STORE.sell(items.Potion())
        difference = hero.gold - old_gold
        self.assertEqual(difference, items.Potion().sell)


class TestStoreSubMenus(unittest.TestCase):
    def test_sell_menu_sale(self):
        with patch('builtins.input', lambda _: '1'):
            old_inv_len = len(hero.inventory)
            STORE.execute_submenu(STORE.main_menu.sell_menu)
            new_inv_len = len(hero.inventory)
            # self.assertEqual(new_inv_len, (old_inv_len - 1))

    def test_buy_menu_purchase(self):
        with patch('builtins.input', lambda _: '1'):
            STORE.execute_submenu(STORE.main_menu.buy_menu)
            inv_list = [x.name for x in hero.inventory]
            statements = all(['Potion' in inv_list, len(hero.inventory) == 1])
            self.assertTrue(statements)


if __name__ == '__main__':
    unittest.main()
