""" python3 ./test_modules.py -b

Tests attacking and magic interaction between hero and enemy objects.
"""
import logging
import os
import sys
import unittest

from HonestQuest.characters.enemy import EnemyFactory
from HonestQuest.characters.hero import Hero

sys.stdout = open(os.devnull, "w")

log = logging.getLogger()
log.disabled = True

HERO = Hero("Dummy", 99)
factory = EnemyFactory()
ENEMY = factory.generate_enemy("Goblin", 99)


class CharacterAttack(unittest.TestCase):
    def test_hero_attack_enemy(self):
        old_hp = ENEMY.hp
        HERO.attack(ENEMY)
        self.assertLess(ENEMY.hp, old_hp)

    def test_enemy_attack_hero(self):
        old_hp = HERO.hp
        ENEMY.attack(HERO)
        self.assertLess(HERO.hp, old_hp)

    def tearDown(self):
        HERO.hp = HERO._max_hp
        ENEMY.hp = ENEMY._max_hp


class CharacterMagic(unittest.TestCase):
    def setUp(self):
        HERO.hp = int(HERO.hp / 2)

    def test_hero_heal(self):
        old_hp = HERO.hp
        HERO.magic.heal(HERO)
        self.assertGreater(HERO.hp, old_hp)

    def test_hero_rage(self):
        old_st = HERO.st
        HERO.magic.rage(HERO)
        self.assertGreater(HERO.st, old_st)

    def test_hero_midheal(self):
        old_hp = HERO.hp
        HERO.magic.midheal(HERO)
        self.assertGreater(HERO.hp, old_hp)

    def test_firewhirl(self):
        old_hp = ENEMY.hp
        HERO.magic.firewhirl(ENEMY)
        self.assertLess(ENEMY.hp, old_hp)

    def test_fireball(self):
        old_hp = ENEMY.hp
        HERO.magic.fireball(ENEMY)
        self.assertLess(ENEMY.hp, old_hp)

    def test_coke(self):
        old_ag = HERO.ag
        HERO.magic.snort_coke(HERO)
        self.assertGreater(HERO.ag, old_ag)

    def tearDown(self):
        HERO.hp = HERO._max_hp
        ENEMY.hp = ENEMY._max_hp


class GoblinMagic(unittest.TestCase):
    def test_big_attack(self):
        HERO.hp = 999999999999
        old_hp = HERO.hp
        ENEMY.magic.big_attack(HERO)
        self.assertLess(HERO.hp, old_hp)

    def test_buff(self):
        ENEMY.mp = 200
        old_st = ENEMY.st
        ENEMY.magic.buff(ENEMY)
        self.assertGreater(ENEMY.st, old_st)

    def test_debuff(self):
        ENEMY.mp = 200
        old_st = HERO.st
        ENEMY.magic.debuff(HERO)
        self.assertLess(HERO.st, old_st)

    def tearDown(self):
        HERO.hp = HERO._max_hp
        ENEMY.hp = ENEMY._max_hp


if __name__ == "__main__":
    unittest.main()
