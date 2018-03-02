''' Base class for all playable characters and enemies.'''
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

    def __sub__(self, target):
        self._attack(target)

    def _attack(self, target, multiplier=1):
        att = self.st * multiplier
        target.hp = target.hp - att
        msg = '{} does {} damage to {}'.format(
            self.name, att, target.name)
        print(msg)
        print('{} HP = {}\n'.format(target.name, target.hp))
        if target.hp <= 0:
            print('{} is dead!\n'.format(target.name))
            target.death(self)

    def _magic(self, att_name, mp_cost):
        if self.mp >= mp_cost:
            self.mp -= mp_cost
            print('{} uses {}!'.format(self.name, att_name))
            return True
        elif self.mp < mp_cost:
            print("You don't have enough mp to use {}.\n".format(att_name))
            return False

    def black_magic(self, target, multiplier, att_name, mp_cost):
        per = self._magic(att_name, mp_cost)
        if per:
            self._attack(target, multiplier)

    def white_magic(self, att_name, stat, num, mp_cost, inc=True):
        per = self._magic(att_name, mp_cost)
        if per:
            self._alter_stat(stat, num, inc)

    def _alter_stat(self, stat, num, inc=True):
        ''' Alter this objects hp, mp, st or ag attributes.

        Note: currently only used to increase own stats.
        '''
        self.stat_error(stat)
        op = operator.add if inc else operator.sub
        max_stat = self.get_max_stat(stat)
        # Tried placing the below nonsense in a dict ('hp': self.hp...}
        # but it doesn't work as it returns the value of self.hp rather
        # than the object self.hp itself
        if stat == 'hp':
            if num+self.hp > max_stat:
                self.hp = max_stat
            else:
                self.hp = op(self.hp, num)
        elif stat == 'mp':
            if num+self.mp > max_stat:
                self.mp = max_stat
            else:
                self.mp = op(self.mp, num)
        elif stat == 'st':
            self.st = op(self.st, num)
        elif stat == 'ag':
            self.ag = op(self.ag, num)

        msg = '{} {} increases by {}\n'.format(self.name, stat.upper(), num)
        print(msg)

    def stat_error(self, stat):
        stats = ['hp', 'mp', 'st', 'ag']
        if stat not in stats:
            msg = 'The statistic variable must be one of {}'
            raise ValueError(msg.format(', '.join(stats)))

    def get_max_stat(self, stat):
        max_stat_d = {'hp': self._max_hp, 'mp': self._max_mp,
                      'st': self.st, 'ag': self.ag}
        return max_stat_d[stat]
