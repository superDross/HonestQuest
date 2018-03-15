''' Protagonist (Hero) classes.'''
from character import Character
from print_text import print_centre
import magic as mg
import pickle
import stats
import sys
import os


class Hero(Character):
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
        print_centre('GAME OVER!!!!')
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
                    print_centre(msg)
                    self._determine_new_magic(before_mglv)
                    break

    def _determine_new_magic(self, before_mglv):
        ''' Communicate new speel learned after leveling up.'''
        if type(before_mglv) != type(self.magic):
            new_spell = set(dir(self.magic)) - \
                set(dir(before_mglv))
            print_centre('\nLearned {}!\n'.format(list(new_spell)[0].title()))

    def get_exp(self):
        ''' Print EXP.'''
        msg = '{} has {} exp\n{} exp to the next level'
        next_lv_exp = self.leveling.get(self.lv + 1)
        exp_to_next_lv = next_lv_exp - self.exp
        print_centre(msg.format(self.name, self.exp, exp_to_next_lv))

    def save(self):
        ''' Save protagonist attributes to a pickle file.'''
        with open('save_file.pkl', 'wb') as outfile:
            pickle.dump(self, outfile, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    t = Hero('name', 2)
    t.save()
    d = Hero('n', 3)
    d.load()
    print(d.lv)













