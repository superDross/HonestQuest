''' Protagonist (Human) classes.'''
from character import Character
import magic as mg
import stats
import sys


class Human(Character):
    def __init__(self, name, lv):
        Character.__init__(self, name, 1, 1, 1, 1, lv)
        self.leveling = stats.leveling
        self._exp = 0
        self._determine_stats()
        self.dead = False

    def _determine_stats(self):
        self.hp = (self.lv * 5) - (self._max_hp - self.hp)
        self._max_hp = self.lv * 5
        self.mp = (self.lv * 2) - (self._max_mp - self.mp)
        self._max_mp = self.lv * 2
        self.ag = self.lv * 1
        self.st = self.lv * 1

    @property
    def magic(self):
        ''' Returns magic spells available to players current level.'''
        class_dict = {tuple(range(0, 3)): mg.LV1,
                      tuple(range(3, 6)): mg.LV3,
                      tuple(range(6, 10)): mg.LV6,
                      tuple(range(10, 15)): mg.LV10,
                      tuple(range(15, 20)): mg.LV15,
                      tuple(range(20, 24)): mg.LV20}
        for k, v in class_dict.items():
            if k[0] <= self.lv <= k[-1]:
                return v(self)

    def death(self, *args):
        print('GAME OVER!!!!')
        # self.dead = True
        sys.exit()

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value):
        ''' Determine level after increasing exp.'''
        self._exp += value
        self._determine_level()

    def _determine_level(self):
        ''' Determine level based upon exp value.'''
        before_mglv = self.magic
        next_level_exp = self.leveling.get(self.lv + 1)
        for leveled, experience in self.leveling.items():
            if self._exp >= next_level_exp:
                if experience > self._exp:
                    self.lv = leveled - 1
                    msg = '{} has reached level {}!'.format(
                        self.name, self.lv)
                    self._determine_stats()
                    print(msg)
                    self._determine_new_magic(before_mglv)
                    print(self)
                    break

    def _determine_new_magic(self, before_mglv):
        ''' Communicate new speel learned after leveling up.'''
        if type(before_mglv) != type(self.magic):
            new_spell = set(dir(self.magic)) - \
                set(dir(before_mglv))
            print('\nLearned {}!\n'.format(list(new_spell)[0].title()))

    def get_exp(self):
        ''' Print EXP.'''
        msg = '{} has {} exp\n{} exp to the next level'
        next_lv_exp = self.leveling.get(self.lv + 1)
        exp_to_next_lv = next_lv_exp - self.exp
        print(msg.format(self.name, self.exp, exp_to_next_lv))


if __name__ == '__main__':
    guy = Human('GUY', 2)
    from enemies import Enemy
    enemy = Enemy(2)
    enemy.mp = 20
    guy.target = enemy
    enemy.target = guy
    print(guy)
    print(enemy)
    enemy.attack()
    guy.magic.heal()
    print(guy)
    guy.attack()
    enemy.buff()
    enemy.debuff()
    enemy.big_attack()
