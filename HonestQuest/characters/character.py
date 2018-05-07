from HonestQuest.utils.print_text import print_centre
from HonestQuest.items.inventory import Inventory
from HonestQuest.utils.common import sleep
from operator import add, sub


class Character(object):
    ''' Base class for all battle characters.

    Attributes:
        name (str): name of character.
        hp (int): hit points.
        mp (int): magic points.
        st (int): strength.
        ag (int): agility.
        lv (int): level of enemy.
        gold (int): money the character is holding.
        inventory (Inventory: Item): all Item objects the character has stored.
        attack (Attack): allows one to attack a target.
        dead (bool): determines whether character has been defeated.
    '''

    def __init__(self, name, hp, mp, st, ag, lv, gold=0):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.st = st
        self.ag = ag
        self.lv = lv
        self._max_hp = hp
        self._max_mp = mp
        self._max_ag = 1000
        self._max_st = 1000
        self._min_hp = 0
        self._min_mp = 0
        self._min_st = 1
        self._min_ag = 1
        self._gold = gold
        self.inventory = Inventory()
        self.dead = False

    def __str__(self):
        return '{}(LV={}, HP={}, MP={}, ST={}, AG={})'.format(
            self.name, self.lv, self.hp, self.mp, self.st, self.ag)

    def attack(self, target):
        ''' Basic physical attack.

        Args:
            target (Character): object to deduct hp from.
        '''
        print_centre('\n{} attacks {}!'.format(self.name, target.name))
        target.alter_stat('hp', self.st, '-')

    def check_hp(self):
        ''' Determine whether object is dead.'''
        if self.hp <= 0:
            self._death()

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, amount):
        if amount < 0:
            print_centre('You do not have enough gold.')
            sleep()
        else:
            self._gold = amount

    def alter_stat(self, stat, value, operator):
        ''' Alter the targets hp, mp, st or ag attribute.

        Args:
            stat (str): hp, mp, st or ag.
            value (int): number to increase the stat by.
            operator (str): '+' or '-'
        '''
        op_func = add if operator == '+' else sub
        if op_func == add:
            value = self._adjust_value_around_max(stat, value)
        else:
            value = self._adjust_value_around_min(stat, value)
        current_stat = getattr(self, stat)
        calc = op_func(current_stat, value)
        setattr(self, stat, calc)
        self._communicate_stat_change(stat, operator, value)
        self.check_hp()

    def _death(self):
        ''' Communicate death to user and change state.'''
        print_centre('{} is dead!'.format(self.name))
        self.dead = True

    def _adjust_value_around_max(self, stat, value):
        ''' Adjusts the parsed value such that it cannot increase
            the stat value above its maximum limit.

        Args:
            stat (str): hp, mp, st or ag.
            value (int): valueber to increase the stat by.
        '''
        max_stat = getattr(self, '_max_{}'.format(stat))
        current_stat = getattr(self, stat)
        if current_stat == max_stat:
            msg = '{} is already at the maximum value\n'
            print_centre(msg.format(stat.upper()))
            sleep()
            return 0
        elif value + current_stat > max_stat:
            return max_stat - current_stat
        else:
            return value

    def _adjust_value_around_min(self, stat, value):
        current_stat = getattr(self, stat)
        if current_stat < 1:
            min_stat = getattr(self, '_min_{}'.format(stat))
            return min_stat
        else:
            return value

    def _communicate_stat_change(self, stat, operator, value):
        ''' Print character stat changes.'''
        upordown = 'increases' if operator == '+' else 'decreases'
        msg = '{} {} {} by {}\n'.format(self.name, stat.upper(),
                                        upordown, value)
        print_centre(msg)
        sleep()
