from HonestQuest.characters.hero import Hero
from HonestQuest.characters.enemy import EnemyFactory
from HonestQuest.items import items
import logging
import unittest

log = logging.getLogger()
log.disabled = True

HERO = Hero('Dummy', 99)
factory = EnemyFactory()
ENEMY = factory.generate_enemy('Goblin', 99)


class ItemUsage(unittest.TestCase):
    def setUp(self):
        HERO.inventory.add_items(items.Potion(), items.Ether(),
                                 items.ProteinShake(), items.RedBull(),
                                 items.Molotov(), items.ManaCleaner(),
                                 items.VodkaShots(), items.MegaPhone())

    def test_potion(self):
        HERO.hp -= 10
        old_hp = HERO.hp
        HERO.inventory.use_item('Potion', HERO)
        self.assertGreater(HERO.hp, old_hp)

    def test_ether(self):
        HERO.mp -= 10
        old_mp = HERO.mp
        HERO.inventory.use_item('Ether', HERO)
        self.assertGreater(HERO.mp, old_mp)

    def test_redbull(self):
        HERO.ag -= 10
        old_ag = HERO.ag
        HERO.inventory.use_item('Red Bull', HERO)
        self.assertGreater(HERO.ag, old_ag)

    def test_protein(self):
        HERO.st -= 10
        old_st = HERO.st
        HERO.inventory.use_item('Protein Shake', HERO)
        self.assertGreater(HERO.st, old_st)

    def test_manacleaner(self):
        old_mp = ENEMY.mp
        HERO.inventory.use_item('Mana Cleaner', ENEMY)
        self.assertLess(ENEMY.mp, old_mp)

    def test_molotov(self):
        old_hp = ENEMY.hp
        HERO.inventory.use_item('Molotov Cocktail', ENEMY)
        self.assertLess(ENEMY.hp, old_hp)

    def test_megaphone(self):
        old_st = ENEMY.st
        HERO.inventory.use_item('Mega Phone', ENEMY)
        self.assertLess(ENEMY.st, old_st)

    def test_vodka(self):
        HERO.hp = 10
        HERO.mp = 10
        HERO.ag = 10
        HERO.st = 10
        old_stats = [HERO.hp, HERO.mp, HERO.ag, HERO.st]
        HERO.inventory.use_item('Vodka Shots', HERO)
        new_stats = [HERO.hp, HERO.mp, HERO.ag, HERO.st]
        self.assertGreater(new_stats, old_stats)


if __name__ == '__main__':
    unittest.main()
