from HonestQuest.characters.character import Character
from HonestQuest.utils.print_text import print_centre
import HonestQuest.magic.hero_magic as hero_magic
import HonestQuest.stats.leveling as leveling
import pickle
import sys


# character/hero.py
class Hero(Character):
    ''' Players character.

    Attributes:
        name (str): name of character.
        hp (int): hit points.
        mp (int): magic points.
        st (int): strength.
        ag (int): agility.
        lv (int): level of enemy.
        attack (Attack): basic physical attack.
        gold (int): money the character is holding.
        dead (bool): determines whether character has been defeated.
    '''

    def __init__(self, name, lv):
        Character.__init__(self, name, 1, 1, 1, 1, lv)
        self._exp = 1
        self.leveling = leveling.leveling
        self._determine_stats()

    def death(self):
        ''' Communicate death to user and change state.'''
        print_centre('{} is dead!'.format(self.name))
        self.dead = True
        sys.exit()

    def save(self):
        ''' Save protagonist attributes to a pickle file.'''
        with open('save_file.pkl', 'wb') as outfile:
            pickle.dump(self, outfile, pickle.HIGHEST_PROTOCOL)

    @property
    def magic(self):
        ''' Returns magic spells available to players current level.'''
        class_dict = {tuple(range(0, 3)): hero_magic.LV1,
                      tuple(range(3, 6)): hero_magic.LV3,
                      tuple(range(6, 9)): hero_magic.LV6}
        for k, v in class_dict.items():
            if k[0] <= self.lv <= k[-1]:
                return v(self)

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value):
        ''' Determine level after increasing exp.'''
        self._exp += value
        self._determine_level()

    def _determine_stats(self):
        ''' Detemine stats from level.'''
        self.hp = (self.lv * 5) - (self._max_hp - self.hp)
        self._max_hp = self.lv * 5
        self.mp = (self.lv * 2) - (self._max_mp - self.mp)
        self._max_mp = self.lv * 2
        self.ag = self.lv * 1
        self.st = self.lv * 1

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
        ''' Communicate new spell learned after leveling up.'''
        if type(before_mglv) != type(self.magic):
            new_spell = set(dir(self.magic)) - \
                set(dir(before_mglv))
            print_centre('\nLearned {}!\n'.format(list(new_spell)[0].title()))
