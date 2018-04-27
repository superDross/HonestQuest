from HonestQuest.utils.print_text import print_centre
from HonestQuest.magic.attack import Attack
from HonestQuest.items.items import Inventory, Potion


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
        self.gold = gold
        self.inventory = Inventory([Potion()])
        self.attack = Attack(self)
        self.dead = False

    def __str__(self):
        return '{}(LV={}, HP={}, MP={}, ST={}, AG={})'.format(
            self.name, self.lv, self.hp, self.mp, self.st, self.ag)

    def check_hp(self):
        ''' Determine whether object is dead.'''
        if self.hp <= 0:
            self.death()

    def death(self):
        ''' Communicate death to user and change state.'''
        print_centre('{} is dead!'.format(self.name))
        self.dead = True
