''' Protagonist (Human) classes.

A diamond shape MixIn is used here where Stats and Actions both inherit from
Chracter base class before bing mixed together as Human. In C++ this is called
the diamond of dread as it can result in base class methods being called twice.
Another problem would be if Stats and Actions have a method with the same name.
This doesn't seem to be a problem here (virtual inheritence in python
maybe?). However, there is probably a better way to design this all as it is
currently a glorified vesion of multiple inheritence.
'''
from character import Character
import stats
import sys


class Stats(Character):
    ''' Stats '''

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


class Actions(Character):
    def __init__(self, name, lv):
        hp, mp, ag, st = self._determine_stats(lv)
        Character.__init__(self, name, hp, mp, st, ag, lv)
        # some weird stuff going on
        # the below attr (test) isnt initilised. dunno why.
        # INVESTIGATE
        self.test = 1

    def heal(self):
        self.white_magic(att_name='heal', stat='hp', num=1,
                         mp_cost=1)

    def rage(self):
        self.white_magic(att_name='rage', stat='st', num=1,
                         mp_cost=1)

    def death(self, *args):
        print('GAME OVER!!!!')
        sys.exit()


class Human(Stats, Actions):
    def __init__(self, name, lv):
        super().__init__(name, lv)
