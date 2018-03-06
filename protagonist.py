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

    def _determine_stats(self):
        self.hp = (self.lv * 5) - (self._max_hp - self.hp)
        self._max_hp = self.lv * 5
        self.mp = (self.lv * 2) - (self._max_mp - self.mp)
        self._max_mp = self.lv * 2
        self.ag = self.lv * 1
        self.st = self.lv * 1

    @property
    def magic(self):
        # perhaps better with a range anf if elif statements
        class_dict = {1: mg.LV1, 2: mg.LV2}
        spells = class_dict[self.lv](self)
        return spells

    def death(self, *args):
        print('GAME OVER!!!!')
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
        next_level_exp = self.leveling.get(self.lv + 1)
        for leveled, experience in self.leveling.items():
            if self._exp >= next_level_exp:
                if experience > self._exp:
                    self.lv = leveled - 1
                    msg = '{} has reached level {}!'.format(
                        self.name, self.lv)
                    self._determine_stats()
                    print(msg)
                    print(self)
                    break

    def get_exp(self):
        ''' Print EXP.'''
        msg = '{} has {} exp\n{} exp to the next level'
        next_lv_exp = self.leveling.get(self.lv + 1)
        exp_to_next_lv = next_lv_exp - self.exp
        print(msg.format(self.name, self.exp, exp_to_next_lv))
