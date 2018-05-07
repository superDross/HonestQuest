''' python3 ./test_modules.py -b '''
from HonestQuest.characters.hero import Hero
from HonestQuest.characters.enemy import EnemyFactory
import logging
import unittest
import os

log = logging.getLogger()
log.disabled = True

HERE = os.path.dirname(os.path.realpath(__file__))
HERO = Hero('Dummy', 10)
factory = EnemyFactory()


class TestEnemyFactory(unittest.TestCase):
    def test_goblin_stats(self):
        goblin = factory.generate_enemy('Goblin', 1)
        stats = [goblin.hp, goblin.mp, goblin.ag, goblin.st,
                 goblin.exp, goblin.gold, goblin.lv, goblin.random]
        expected = [3, 2, 3, 2, 6, 3,  1, 7]
        self.assertEqual(stats, expected)

    def test_bat_stats(self):
        bat = factory.generate_enemy('Bat', 1)
        stats = [bat.hp, bat.mp, bat.ag, bat.st,
                 bat.exp, bat.gold, bat.lv, bat.random]
        expected = [2, 2, 3, 1, 3, 3, 1, 10]
        self.assertEqual(stats, expected)

    def test_dragon_stats(self):
        dragon = factory.generate_enemy('Dragon', 2)
        stats = [dragon.hp, dragon.mp, dragon.ag, dragon.st,
                 dragon.exp, dragon.gold, dragon.lv, dragon.random]
        expected = [20, 20, 20, 20, 100, 30, 2, 2]
        self.assertEqual(stats, expected)


class TestHero(unittest.TestCase):
    def test_level10_stats(self):
        expected = [50, 50, 20, 20, 10, 10]
        stats = [HERO.hp, HERO._max_hp, HERO.mp, HERO._max_mp,
                 HERO.ag, HERO.st]
        self.assertEqual(stats, expected)

    def test_level10_magic(self):
        expected = ['fireball', 'heal', 'midheal', 'rage']
        magic = [x for x in dir(HERO.magic) if not x.startswith('_')]
        self.assertEqual(sorted(magic), sorted(expected))

    def test_level20_magic(self):
        hero = Hero('Dummy', 20)
        expected = ['fireball', 'heal', 'midheal', 'rage',
                    'snort_coke', 'firewhirl']
        magic = [x for x in dir(hero.magic) if not x.startswith('_')]
        self.assertEqual(sorted(magic), sorted(expected))

    def test_regeneration(self):
        HERO.hp = 10
        HERO.mp = 10
        HERO.regenerate_max_stats()
        self.assertEqual([50, 20], [HERO.hp, HERO.mp])

    def test_level_up(self):
        hero = Hero('Dummy', 1)
        old_lv = hero.lv
        hero.exp = 200
        self.assertFalse(old_lv == hero.lv)

    def test_level_up_magic(self):
        hero = Hero('Dummy', 1)
        old_magic = [x for x in dir(hero.magic) if not x.startswith('_')]
        hero.exp = 200
        magic = [x for x in dir(hero.magic) if not x.startswith('_')]
        self.assertEqual(old_magic + ['rage'], magic)

    def check_minus_gold(self):
        HERO.gold = -200
        self.assertEqual(HERO.gold, 0)

    def check_transfer_gold(self):
        HERO.gold = 20
        self.assertEqual(HERO.gold, 20)

    def test_death(self):
        hero = Hero('Dummy', 1)
        with self.assertRaises(SystemExit):
            hero.alter_stat('hp', 700, '-')

    def test_save(self):
        HERO.save()
        save_file = os.path.join(HERE.replace(
            'test', 'HonestQuest'), 'save_file.pkl')
        exists = os.path.isfile(save_file)
        self.assertTrue(exists)

    def test_min_stats(self):
        HERO.alter_stat('mp', 200000, '-')
        HERO.alter_stat('ag', 200000, '-')
        HERO.alter_stat('st', 200000, '-')
        min_stats = [HERO._min_mp, HERO._min_st, HERO._min_ag]
        self.assertEqual(min_stats, [HERO.mp, HERO.st, HERO.ag])

    def test_tear_down(self):
        save_file = os.path.join(HERE.replace(
            'test', 'HonestQuest'), 'save_file.pkl')
        os.remove(save_file)


if __name__ == '__main__':
    unittest.main()
