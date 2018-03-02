''' Base class for all playable characters and enemies.'''
from custom_exceptions import StatError
import operator


class Character(object):
    def __init__(self, name, hp, mp, st, ag, lv):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.st = st
        self.ag = ag
        self.lv = lv
        self._max_hp = hp
        self._max_mp = mp
        self.gold = 0
        self._target = None

    def __str__(self):
        return '{}(LV={}, HP={}, MP={}, ST={}, AG={})\n'.format(
            self.name, self.lv, self.hp, self.mp, self.st, self.ag)

    def __sub__(self, target, multiplier=1):
        att = self.st * multiplier
        target.hp = target.hp - att
        msg = '{} does {} damage to {}'.format(
            self.name, att, target.name)
        print(msg)
        print('{} HP = {}\n'.format(target.name, target.hp))
        if target.hp <= 0:
            print('{} is dead!\n'.format(target.name))
            target.death(self)

    def black_magic(self, att_name, stat, num, mp_cost, target=None):
        inc = False
        self._magic(att_name, stat, num, mp_cost, inc, target)

    def white_magic(self, att_name, stat, num, mp_cost, target=None):
        inc = True
        self._magic(att_name, stat, num, mp_cost, inc, target)

    def _magic(self, att_name, stat, num, mp_cost, inc, target):
        per = self._reduce_mp(att_name, mp_cost)
        if per:
            self._alter_stat(stat=stat, num=num, inc=inc, target=target)

    def _reduce_mp(self, att_name, mp_cost):
        if self.mp >= mp_cost:
            self.mp -= mp_cost
            print('{} uses {}!'.format(self.name, att_name))
            return True
        elif self.mp < mp_cost:
            print("You don't have enough mp to use {}.\n".format(att_name))
            return False

    def _alter_stat(self, stat, num, inc=True, target=None):
        ''' Alter a Character objects hp, mp, st or ag attribute.'''
        stat_dict = {'hp': self._alter_hp,
                     'mp': self._alter_mp,
                     'st': self._alter_st,
                     'ag': self._alter_ag}
        if stat not in ['hp', 'mp', 'st', 'ag']:
            raise StatError(stat)
        self._target = self if not target else target
        op = operator.add if inc else operator.sub
        alter_stat_method = stat_dict[stat]
        alter_stat_method(num, op)
        upordown = 'increases' if op == operator.add else 'decreases'
        msg = '{} {} {} by {}\n'.format(self._target.name, stat.upper(),
                                        upordown, num)
        print(msg)

    def _alter_hp(self, num, op):
        max_stat = self._target._max_hp
        if num + self._target.hp > max_stat and op == operator.add:
            self._target.hp = max_stat
        else:
            self._target.hp = op(self._target.hp, num)

    def _alter_mp(self, num, op):
        max_stat = self._target._max_mp
        if num + self._target.mp > max_stat and op == operator.add:
            self._target.mp = max_stat
        else:
            self._target.mp = op(self._target.mp, num)

    def _alter_st(self, num, op):
        self._target.st = op(self._target.st, num)

    def _alter_ag(self, num, op):
        self._target.ag = op(self._target.ag, num)
