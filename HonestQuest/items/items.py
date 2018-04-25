''' All items player can use.'''
from HonestQuest.utils.custom_exceptions import StatError
import operator
import time

# The items must be deleteed after used


class Item(object):
    ''' Items stored and used by Character classes.

    Attributes:
        name (str): name of the item.
        stat (str): the Character stat to modify (hp, mp, st or ag).
        operator (str): increase ('+') or decrease ('-') the Character stat.
        value (int): the number to increase or decrease the stat by.
        cost (int): amount of gold the item costs to buy.
        description (str): a summary of the items effects.
    '''

    def __init__(self, name, stat, operator, value, cost, description):
        if stat not in ['hp', 'mp', 'st', 'ag']:
            raise StatError(stat)
        if operator not in ['+', '-']:
            raise ValueError('operator must be + or -')
        self.name = name
        self.stat = stat
        self.operator = operator
        self.value = value
        self.cost = cost
        self.description = description

    def __call__(self, target):
        self.use(target)

    def __str__(self):
        return '{}:\t{}'.format(self.name, self.description)

    def use(self, target):
        ''' Increase/decrease the targets stat/attribute by the given value.

        Args:
            target (Character): object to use the item on.
        '''
        op = {'+': operator.add,
              '-': operator.sub}
        self._use_msg()
        op_func = op.get(self.operator)
        target_stat = getattr(target, self.stat)
        updated_target_stat = op_func(target_stat, self.value)
        setattr(target, self.stat, updated_target_stat)
        updown = 'increased' if self.operator == '+' else 'decreased'
        print('{} {} {} by {}\n'.format(target.name, self.stat.upper(),
                                        updown, self.value))
        time.sleep(1.5)

    def _use_msg(self):
        print('{} has been used!\n'.format(self.name.title()))
        time.sleep(1.5)


class Potion(Item):
    def __init__(self):
        Item.__init__(self, name='Potion', stat='hp', operator='+',
                      value=10, cost=10, description='Increase targets HP')


class Ether(Item):
    def __init__(self):
        Item.__init__(self, name='Ether', stat='mp', operator='+',
                      value=10, cost=30, description='Increase targets MP')


class ProteinShake(Item):
    def __init__(self):
        Item.__init__(self, name='Protein Shake', stat='st', operator='+',
                      value=10, cost=40, description='Increase targets ST')

    def _use_msg(self):
        print('Lets BRO DOWN with a {}!\n'.format(self.name))
        time.sleep(1.5)


class RedBull(Item):
    def __init__(self):
        Item.__init__(self, name='Red Bull', stat='ag', operator='+',
                      value=10, cost=30, description='Increase targets AG')


class Molotov(Item):
    def __init__(self):
        Item.__init__(self, name='Molotov Cocktail', stat='hp', operator='-',
                      value=5, cost=5, description='Decrease target HP')

    def _use_msg(self):
        print('You threw a {}!\n'.format(self.name))
        time.sleep(1.5)


class ManaCleaner(Item):
    def __init__(self):
        Item.__init__(self, name='Mana Cleaner', stat='mp', operator='-',
                      value=5, cost=20, description='Decrease target MP')

    def _use_msg(self):
        print('You uncorked a bottle of {}.\n'.format(self.name))
        time.sleep(1.5)


class MegaPhone(Item):
    def __init__(self):
        Item.__init__(self, name='Mega Phone', stat='st', operator='-',
                      value=10, cost=25, description='Decrease target ST')

    def _use_msg(self):
        print('You shrieked into a {}!!!\n'.format(self.name))
        time.sleep(1.5)


class VodkaShots(Item):
    def __init__(self):
        super().__init__(name='Vodka Shots', stat='hp', operator='+',
                         value=10, cost=25, description='All stats increase')

    def use(self, target):
        for stat in ['hp', 'mp', 'ag', 'st']:
            self.stat = stat
            super().use(target)

    def _use_msg(self):
        print('You slammed a {}!\n'.format(self.name[:-1]))
        time.sleep(1.5)


# TESTING
# from HonestQuest.characters.hero import Hero
# jim = Hero('jim', 10)
# print(jim.inventory)
# # potion = Potion() # Item('potion', 'hp', '+', 2, 10, 'increase HP')
# # potion.use(jim)
# # print(jim.hp)
# 
# shot = VodkaShots()
# shot.use(jim)
# # molotov = Molotov()
# # molotov.use(jim)
# # print(jim.hp)
