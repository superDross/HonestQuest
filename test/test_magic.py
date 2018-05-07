''' python3 ./test_modules.py -b '''
from HonestQuest.characters.hero import Hero
from HonestQuest.characters.enemy import EnemyFactory
from HonestQuest.magic.magic import Magic
import logging
import unittest

log = logging.getLogger()
log.disabled = True

HERO = Hero('Dummy', 1)
factory = EnemyFactory()
ENEMY = factory.generate_enemy('Goblin', 1)


class TestMagic(unittest.TestCase):
    def test_magic_creation(self):
        new_magic = Magic(character=HERO, att_name='Elbow Smash', stat='hp',
                          value=2, mp_cost=1, operator='-', target=ENEMY)
        old_hp = ENEMY.hp
        old_mp = HERO.mp
        new_magic()
        test = all([(old_hp - 2) == ENEMY.hp, (old_mp - 1) == HERO.mp])
        self.assertTrue(test)


if __name__ == '__main__':
    unittest.main()
