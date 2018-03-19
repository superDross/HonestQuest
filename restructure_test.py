''' Changes:
    - target must be specified for each attack/magic
    - Attack, Magic etc. are all split into different classes

    Structure:
        HonestQuest/
            __main__.py
            stats/
                enemy_stats.csv
                leveling.py
            magic/
                attack.py (?)
                magic.py
                hero_magic.py
                enemy_magic.py (?)
            characters/
                character
                hero
                enemy
            menus/
                menu.py
                battle_menu.py
                store_menu.py
            items/
                item.py
                inventory.py
            utils/
                print_text.py
                useful.py (?)
            field/
                overworld.py
            animations/
                animations.py
'''
import operator
import sys


# characters/character.py
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
        self.attack = Attack(self, None)
        self.dead = False

    def check_hp(self):
        ''' Determine whether object is dead.'''
        if self.hp <= 0:
            print('{} is dead!\n'.format(self.name))
            self.death()

    def death(self):
        print('{} is dead!'.format(self.name))
        self.dead = True


# Is this really necessary
class Base(object):
    def __init__(self, character, _data=None):
        self._character = character
        if _data:
            for attribute, value in _data.items():
                setattr(self, attribute, value)


# magic/attack.py
class Attack(Base):
    ''' Basic attack.

    Attributes:
        target: Character object to deduct hp from.
    '''

    def __call__(self, target):
        ''' Basic attack which reduces target HP by ST value.'''
        target.hp -= self._character.st
        msg = '\n{} does {} damage to {}'.format(
            self._character.name, self._character.st, target.name)
        print(msg)
        print('{} HP = {}\n'.format(target.name, target.hp))
        target.check_hp()


# magic/magic.py
class Magic(object):
    ''' Creates a magic spell.

    Attributes:
        character: Character object whom the spell will be assigned to
        target: Character object that will be the reciever of the spell
        att_name: attack name
        stat: the targets statsistic to effect (hp, mp, ag or st)
        num: number to add/subtract from targets stat
        mp_cost: number to deduct from character mp
        inc: whether to increase or decrease stat
    '''

    def __init__(self, character, att_name, stat, num, mp_cost, inc, target):
        self._character = character
        self.att_name = att_name
        self.stat = stat
        self.num = num
        self.mp_cost = mp_cost
        self.inc = inc
        self.target = target

    def __call__(self):
        if self.inc:
            self.white_magic()
        else:
            self.black_magic()

    def black_magic(self):
        ''' Magic that reduces a targets given stat attribute.'''
        self._magic()
        self.target.check_hp()

    def white_magic(self):
        ''' Magic that increases a targets given stat attribute.'''
        if (self.stat == 'hp' and (self.num + self._character.hp
                                   > self._character._max_hp)) \
            or (self.stat == 'mp' and (self.num + self._character.mp
                                       >= self.character._max_mp)):
            print('{} is already at the maximum value'.format(
                  self.stat.upper()))
            return
        self._magic()

    def _magic(self):
        ''' Performs magic and depletes mp.'''
        per = self._reduce_mp()
        if per:
            self._alter_stat()

    def _reduce_mp(self):
        ''' Lower MP by a given value.'''
        if self._character.mp >= self.mp_cost:
            self._character.mp -= self.mp_cost
            print('{} uses {}!'.format(self._character.name, self.att_name))
            return True
        elif self._character.mp < self.mp_cost:
            print("You don't have enough mp to use {}.\n".format(
                  self.att_name))
            return False

    def _alter_stat(self):
        ''' Alter a Character Bases hp, mp, st or ag attribute.'''
        if self.stat not in ['hp', 'mp', 'st', 'ag']:
            raise IOError(self.stat)
        op = operator.add if self.inc else operator.sub
        calc = op(getattr(self.target, self.stat), self.num)
        setattr(self.target, self.stat, calc)
        upordown = 'increases' if op == operator.add else 'decreases'
        msg = '{} {} {} by {}\n'.format(self.target.name, self.stat.upper(),
                                        upordown, self.num)
        print(msg)


# magic/hero_magic.py
class LV1(Base):
    def heal(self, target):
        mag = Magic(character=self._character, att_name='Heal', stat='hp',
                    num=1, mp_cost=1, inc=True, target=target)
        mag()


class LV3(LV1):
    def rage(self, target):
        mag = Magic(character=self._character, att_name='Rage', stat='st',
                    num=1, mp_cost=1, inc=True, target=target)
        mag()


class LV6(LV3):
    def fireball(self, target):
        mag = Magic(character=self._character, att_name='Fireball', stat='hp',
                    num=10, mp_cost=10, inc=False, target=target)
        mag()


# character/hero.py
class Hero(Character):
    def __init__(self, name, lv):
        Character.__init__(self, name, 1, 1, 1, 1, lv)

    def death(self):
        print('{} is dead!'.format(self.name))
        self.dead = True
        sys.exit()

    @property
    def magic(self):
        ''' Returns magic spells available to players current level.'''
        class_dict = {tuple(range(0, 3)): LV1,
                      tuple(range(3, 6)): LV3,
                      tuple(range(6, 9)): LV6}
        for k, v in class_dict.items():
            if k[0] <= self.lv <= k[-1]:
                return v(self, None)


guy = Hero('Guy', 7)
guy.mp = 200
enemy = Character('Enemy', 11, 1, 1, 1, 1)
guy.attack(enemy)
guy.magic.rage(guy)
guy.magic.heal(guy)
guy.magic.fireball(enemy)
