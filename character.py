''' Base class for all playable characters and enemies.'''
from custom_exceptions import StatError, InvalidTarget
from print_text import print_centre
import operator
import time


class Character(object):
    ''' Base class for player and all enemies.'''
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
        return '{}(LV={}, HP={}, MP={}, ST={}, AG={})'.format(
            self.name, self.lv, self.hp, self.mp, self.st, self.ag)

    def attack(self, multiplier=1):
        ''' Basic attack which reduces target HP by ST value.'''
        self.target.hp -= self.st
        msg = '\n{} does {} damage to {}'.format(
            self.name, self.st, self.target.name)
        print_centre(msg)
        print_centre('{} HP = {}\n'.format(self.target.name, self.target.hp))
        if self.target.hp <= 0:
            print_centre('{} is dead!\n'.format(self.target.name))
            self.target.death()
        time.sleep(2)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        ''' Store an opposing Character object as an attribute.'''
        if not isinstance(target, Character):
            raise InvalidTarget(target, Character)
        self._target = target

    @property
    def items(self):
        return self._inventory

    @items.setter
    def items(self, items):
        ''' Add Item objects to the inventory.'''
        if not isinstance(items, list):
            items = [items, ]
        for item in items:
            self._inventory[item.name] = item
            print_centre('{} added to inventory.'.format(item.name))

    def use_item(self, item_name):
        ''' Use an Item object in your inventory.'''
        item = self._inventory.get(item_name)
        print_centre('{} Used {}'.format(self.name, item_name))
        self._alter_stat(item.stat, item.value, inc=True)
        del self._inventory[item_name]

    def black_magic(self, att_name, stat, num, mp_cost):
        ''' Magic that reduces a targets given stat attribute.'''
        inc = False
        self._magic(att_name, stat, num, mp_cost, inc, target=True)

    def white_magic(self, att_name, stat, num, mp_cost):
        ''' Magic that increases a targets given stat attribute.'''
        inc = True
        if (stat == 'hp' and (num + self.hp > self._max_hp)) \
                or (stat == 'mp' and (num + self.mp >= self._max_mp)):
            print_centre('{} is already at the maximum value'.format(stat.upper()))
            time.sleep(2)
            return
        self._magic(att_name, stat, num, mp_cost, inc, target=False)

    def _magic(self, att_name, stat, num, mp_cost, inc, target):
        ''' Performs magic and depletes mp.'''
        per = self._reduce_mp(att_name, mp_cost)
        if per:
            self._alter_stat(stat=stat, num=num, inc=inc, target=target)

    def _reduce_mp(self, att_name, mp_cost):
        ''' Lower MP by a given value.'''
        if self.mp >= mp_cost:
            self.mp -= mp_cost
            print_centre('{} uses {}!'.format(self.name, att_name))
            return True
        elif self.mp < mp_cost:
            print_centre("You don't have enough mp to use {}.\n".format(att_name))
            return False

    def _alter_stat(self, stat, num, inc=True, target=False):
        ''' Alter a Character objects hp, mp, st or ag attribute.'''
        if stat not in ['hp', 'mp', 'st', 'ag']:
            raise StatError(stat)
        if target:
            reciever = self.target
        else:
            reciever = self
        # self.target = target
        op = operator.add if inc else operator.sub
        calc = op(getattr(reciever, stat), num)
        setattr(reciever, stat, calc)
        upordown = 'increases' if op == operator.add else 'decreases'
        msg = '{} {} {} by {}\n'.format(reciever.name, stat.upper(),
                                        upordown, num)
        print_centre(msg)
        time.sleep(2)
