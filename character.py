''' Base class for all playable characters and enemies.'''


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

    def _magic(self, multiplier, att_name, mp_cost):
        if self.mp >= mp_cost:
            self.mp -= mp_cost
            print('{} uses {}!'.format(self.name, att_name))
            return True
        elif self.mp < mp_cost:
            print("You don't have enough mp to use {}.\n".format(att_name))
            return False

    def black_magic(self, target, multiplier, att_name, mp_cost):
        per = self._magic(multiplier, att_name, mp_cost)
        if per:
            self._attack(target, multiplier)

    def white_magic(self, multiplier, att_name, mp_cost):
        per = self._magic(multiplier, att_name, mp_cost)
        if per:
            self._increase_hp(multiplier)

    def _increase_hp(self, inc):
        self.hp += inc
        if self.hp > self._max_hp:
            self.hp = self._max_hp
        msg = '{} hp increases by {}'.format(self.name, inc)
        print(msg)
        print('{} HP = {}\n'.format(self.name, self.hp))
