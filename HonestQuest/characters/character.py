from HonestQuest.utils.print_text import print_centre
from HonestQuest.magic.attack import Attack
from HonestQuest.items.items import Inventory, Potion
from HonestQuest.utils.custom_exceptions import StatError
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
        attack (Attack): basic physical attack.
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
        self.gold = gold
        self.inventory = Inventory([Potion()])
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
        sleep()
        target.alter_stat('hp', self.st, '-')

    def check_hp(self):
        ''' Determine whether object is dead.'''
        if self.hp <= 0:
            self.death()

    def death(self):
        ''' Communicate death to user and change state.'''
        print_centre('{} is dead!'.format(self.name))
        self.dead = True

    # NOTE: everything below here could be its own class StatAlter???
    def alter_stat(self, stat, value, operator):
        ''' Alter the targets hp, mp, st or ag attribute.

        Args:
            stat (str): hp, mp, st or ag.
            value (int): number to increase the stat by.
            operator (str): '+' or '-'
        '''
        self._error_check(stat)
        # create operations function
        op = {'+': add, '-': sub}
        op_func = op.get(operator)
        # adjust value if operation function is add
        if op_func == add:
            value = self._adjust_value(stat, value)
        # set stats new value (ensure above 0 for anything not HP)
        current_stat = getattr(self, stat)
        calc = op_func(current_stat, value)
        if stat in ['mp', 'ag', 'st'] and calc < 1:
            calc = 1
        setattr(self, stat, calc)
        # communicate stat change to player
        upordown = 'increases' if op_func == add else 'decreases'
        msg = '{} {} {} by {}\n'.format(self.name, stat.upper(),
                                        upordown, value)
        print_centre(msg)
        sleep()

    def _adjust_value(self, stat, value):
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

    def _error_check(self, stat):
        if stat not in ['hp', 'mp', 'st', 'ag']:
            raise StatError(self.stat)
