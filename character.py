''' Base class for all playable characters and enemies.'''
from custom_exceptions import StatError, InvalidTarget
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
        self._inventory = {}

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

    def attack(self, target, multiplier=1):
        self.__sub__(target, multiplier)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target=None):
        valid_targets = (Character, type(None))
        if not isinstance(target, valid_targets):
            raise InvalidTarget(target, valid_targets)
        if target:
            self._target = target
        else:
            self._target = self

    @property
    def items(self):
        return self._inventory

    @items.setter
    def items(self, items):
        ''' Add items to the inventory.'''
        if not isinstance(items, list):
            items = [items, ]
        for item in items:
            self._inventory[item.name] = item
            print('{} added to inventory.'.format(item.name))

    def use_item(self, item_name):
        ''' Use an item in your inventory.'''
        item = self._inventory.get(item_name)
        print('{} Used {}'.format(self.name, item_name))
        self._alter_stat(item.stat, item.value, inc=True)
        del self._inventory[item_name]

    def black_magic(self, att_name, stat, num, mp_cost, target=None):
        ''' Magic that reduces a targets given stat attribute.'''
        inc = False
        self._magic(att_name, stat, num, mp_cost, inc, target)

    def white_magic(self, att_name, stat, num, mp_cost, target=None):
        ''' Magic that increases a targets given stat attribute.'''
        inc = True
        self._magic(att_name, stat, num, mp_cost, inc, target)

    def _magic(self, att_name, stat, num, mp_cost, inc, target):
        ''' Performs magic and depletes mp.'''
        per = self._reduce_mp(att_name, mp_cost)
        if per:
            self._alter_stat(stat=stat, num=num, inc=inc, target=target)

    def _reduce_mp(self, att_name, mp_cost):
        ''' Lower MP by a given value.'''
        if self.mp >= mp_cost:
            self.mp -= mp_cost
            print('{} uses {}!'.format(self.name, att_name))
            return True
        elif self.mp < mp_cost:
            print("You don't have enough mp to use {}.\n".format(att_name))
            return False

    def _alter_stat(self, stat, num, inc=True, target=None):
        ''' Alter a Character objects hp, mp, st or ag attribute.'''
        if stat not in ['hp', 'mp', 'st', 'ag']:
            raise StatError(stat)
        self.target = target
        op = operator.add if inc else operator.sub
        calc = op(getattr(self._target, stat), num)
        setattr(self._target, stat, calc)
        upordown = 'increases' if op == operator.add else 'decreases'
        msg = '{} {} {} by {}\n'.format(self._target.name, stat.upper(),
                                        upordown, num)
        print(msg)
