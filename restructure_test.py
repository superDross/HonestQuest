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
from animations import animations
from print_text import print_centre
from common import weighted_choice
import operator
import time
import sys
import csv


# characters/character.py
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


# magic/attack.py
class Attack(object):
    ''' Basic physical attack.

    Attributes:
        target (Character): object to deduct hp from.
    '''
    def __init__(self, character):
        self._character = character

    def __call__(self, target):
        ''' Basic attack which reduces target HP by ST value.'''
        target.hp -= self._character.st
        msg = '\n{} does {} damage to {}'.format(
            self._character.name, self._character.st, target.name)
        print_centre(msg)
        print_centre('{} HP = {}\n'.format(target.name, target.hp))
        target.check_hp()


# magic/magic.py
class Magic(object):
    ''' Base class for a magic spell.

    Attributes:
        character (Character): object whom the spell will be assigned to.
        target (Character): object that will be the reciever of the spell.
        att_name (str): attack name.
        stat (str): targets statistical attribute to alter (hp, mp, ag or st).
        num (int): number to add/subtract from targets stat.
        mp_cost (int): number to deduct from character mp.
        inc (bool): whether to increase or decrease stat.
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
                                       >= self._character._max_mp)):
            print_centre('{} is already at the maximum value'.format(
                         self.stat.upper()))
            return
        self._magic()

    def _magic(self):
        ''' Performs magic and depletes _character mp.'''
        per = self._reduce_mp()
        if per:
            self._alter_stat()

    def _reduce_mp(self):
        ''' Lower _character mp by a given value.'''
        if self._character.mp >= self.mp_cost:
            self._character.mp -= self.mp_cost
            print_centre('{} uses {}!'.format(self._character.name,
                                              self.att_name))
            return True
        elif self._character.mp < self.mp_cost:
            print_centre("You don't have enough mp to use {}.\n".format(
                  self.att_name))
            return False

    def _alter_stat(self):
        ''' Alter the targets hp, mp, st or ag attribute.'''
        valid_stats = ['hp', 'mp', 'st', 'ag']
        if self.stat not in valid_stats:
            raise IOError(self.stat)
        op = operator.add if self.inc else operator.sub
        calc = op(getattr(self.target, self.stat), self.num)
        if self.stat in valid_stats[1:] and calc < 1:
            calc = 1
        setattr(self.target, self.stat, calc)
        upordown = 'increases' if op == operator.add else 'decreases'
        msg = '{} {} {} by {}\n'.format(self.target.name, self.stat.upper(),
                                        upordown, self.num)
        print_centre(msg)


# magic/enemy_magic.py
class EnemyMagic(object):
    ''' Magic spells used by enemies.

    Attributes:
        enemy (Enemy): enemy object who the magic is assigned to.
        attack_name (str): name assigned to big attack spell.
        buff_name (str): name assigned to buff spell.
        debuff_name (str): name assigned to debuff spell.
        stat (str): statistic attribute (hp/mp/st/ag) used in
                    debuff/buff spells.
    '''

    def __init__(self, enemy, magic_names):
        '''
        Parameters:
            magic_names (dict): holds the values to the attack_name,
                                buff_name and debuff_name attributes.
        '''
        self.enemy = enemy
        self._set_attributes(magic_names)

    def _set_attributes(self, magic_names):
        ''' Transforms _magic_names dict into attributes.'''
        for k, v in magic_names.items():
            if not v.isdigit():
                setattr(self, k, v)

    def big_attack(self, target):
        ''' Large magic attack that deducts the enemy targets hp.'''
        mag = Magic(character=self.enemy, att_name=self.attack_name,
                    stat='hp', num=self.enemy.st * self.enemy.lv,
                    mp_cost=2 * self.enemy.lv, inc=False,
                    target=target)
        mag()

    def buff(self, target):
        ''' Increases the enemies statistic attribute (self.stat).'''
        mag = Magic(character=self.enemy, att_name=self.buff_name,
                    stat=self.stat, num=2 * self.enemy.lv,
                    mp_cost=2 * self.enemy.lv, inc=True,
                    target=target)
        mag()

    def debuff(self, target):
        ''' Decreases the enemies target statistic attribute (self.stat).'''
        mag = Magic(character=self.enemy, att_name=self.debuff_name,
                    stat=self.stat, num=2 * self.enemy.lv,
                    mp_cost=2 * self.enemy.lv, inc=False,
                    target=target)
        mag()


# magic/hero_magic.py
''' Magic to be assigned to Hero object upon accension to the described level.

Args:
    target (Character): character to cast spell upon.
'''


class LV1(object):
    def __init__(self, character):
        self._character = character

    def heal(self, target):
        ''' Increase hp attribute of target object.'''
        mag = Magic(character=self._character, att_name='Heal', stat='hp',
                    num=1, mp_cost=1, inc=True, target=target)
        mag()


class LV3(LV1):
    ''' Increase st attribute of target object.'''

    def rage(self, target):
        mag = Magic(character=self._character, att_name='Rage', stat='st',
                    num=1, mp_cost=1, inc=True, target=target)
        mag()


class LV6(LV3):
    ''' Decrease hp attribute of target object.'''

    def fireball(self, target):
        mag = Magic(character=self._character, att_name='Fireball', stat='hp',
                    num=10, mp_cost=10, inc=False, target=target)
        mag()


# character/hero.py
class Hero(Character):
    ''' Players character.

    Attributes:
        name (str): name of character.
        hp (int): hit points.
        mp (int): magic points.
        st (int): strength.
        ag (int): agility.
        lv (int): level of enemy.
        attack (Attack): basic physical attack.
        gold (int): money the character is holding.
        dead (bool): determines whether character has been defeated.
    '''

    def __init__(self, name, lv):
        Character.__init__(self, name, 1, 1, 1, 1, lv)

    def death(self):
        ''' Communicate death to user and change state.'''
        print_centre('{} is dead!'.format(self.name))
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
                return v(self)


# character/enemy.py
class Enemy(Character):
    ''' Creates an enemy character.

    Attributes:
        name (str): name of species.
        hp (int): hit points.
        mp (int): magic points.
        st (int): strength.
        ag (int): agility.
        lv (int): level of enemy.
        attack (Attack): basic physical attack.
        gold (int): money to transfer to Hero upon death.
        dead (bool): Boolean defining if character has been defeated.
        exp (int): experience points to transfer to Hero upon death.
        random (int): used to determine liklihood of randomly
                      appearing in game battle.
        animation (list: str): ASCII image of enemy.
        magic (EnemyMagic): magic attacks.
    '''

    def __init__(self, species, hp, mp, st, ag,
                 lv, exp, gold, random, animation,
                 magic_names):
        '''
        Parameters:
            magic_names (dict): names of enemy magic attacks.
        '''
        Character.__init__(self, species, hp, mp, st, ag, lv, gold)
        self.exp = exp
        self.random = random
        self.animation = animation
        self.magic = EnemyMagic(self, magic_names)

    def death(self):
        ''' Communicate death to user and change state.'''
        print_centre('{} is dead!'.format(self.name))
        print_centre('I got gold and exp to give!')
        self.dead = True

    def ai(self, target):
        ''' Enemy action determined by if else block.'''
        if not self.dead:
            actions = {'attack': 10, 'magic': 3}
            action = weighted_choice(actions)
            if self.mp > 1 and action == 'magic':
                spells = {'big_attack': 10, 'buff': 2, 'debuff': 1}
                choice = weighted_choice(spells)
                spell = getattr(self.magic, choice)
                target = target if choice != 'buff' else self
                spell(target)
                time.sleep(1.5)
            else:
                self.attack(target)
                time.sleep(1.5)


class EnemyFactory(object):
    ''' Creates an Enemy class.

    Generates an Enemy class by extracting the row
    in species_stats.csv that matches the species
    parameter. The row is then transformed into a
    dictionary, the values of which are parsed to
    the Enemy class as parameters.

    If a species parameter is not parsed to this
    class, the species, and therefore the Enemy
    class generated, is determined via a weighted
    random selection process defined by the 'random'
    column in species_stat.csv.

    Attributes:
        lv (int): desired enemy level.
        species (str, optional): determines which enemy to create.
        magic_names (dict): names of enemy magic attacks.
    '''

    def __init__(self, lv, species=None):
        self.lv = lv
        self.species = self._determine_species(species)
        self._species_dict = self._species_stats_dict(lv)[self.species]
        self.magic_names = {k: v for k, v in self._species_dict.items()
                            if not isinstance(v, int)}

    def generate(self):
        ''' Returns an Enemy object.'''
        animation = animations[self.species]
        enemy = Enemy(species=self._species_dict['species'],
                      hp=self._species_dict['hp'],
                      mp=self._species_dict['mp'],
                      st=self._species_dict['st'],
                      ag=self._species_dict['ag'],
                      lv=self.lv,
                      exp=self._species_dict['exp'],
                      gold=self._species_dict['gold'],
                      random=self._species_dict['random'],
                      animation=animation,
                      magic_names=self.magic_names)
        return enemy

    def _determine_species(self, species):
        ''' Weighted random determination of the enemy species,
            if a species name is not given.
        '''
        if not species:
            species2rate = {k: int(v['random'])
                            for k, v in self._species_stats_dict().items()}
            species = weighted_choice(species2rate)
        return species

    @staticmethod
    def _species_stats_dict(lv=None):
        ''' Open the stats sheet and return as a nested dict.
            {species: {stat: value, ...}

        Args:
            lv: desired enemy level, used to evaluate stats.
        '''
        all_species_dict = {}
        with open('species_stats.csv', mode='r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            header = next(reader)
            for row in reader:
                if lv:
                    row = [int(x) * lv if x.isdigit() else x for x in row]
                else:
                    row = [int(x) if x.isdigit() else x for x in row]
                mydict = dict(zip(header, row))
                all_species_dict[mydict['species']] = mydict
        return all_species_dict


# TESTING
# Create Objects
factory = EnemyFactory(2, 'Goblin')
enemy = factory.generate()
guy = Hero('Guy', 7)

# Set HP & MP for Test
guy.mp = 200
guy.hp = 200
enemy.mp = 200
print(guy)
print(enemy)

# Test Hero Stats
assert guy.lv == 7
assert guy.hp == 200 and guy.mp == 200
assert guy.st == 1 and guy.ag == 1
assert guy._max_hp == 1 and guy._max_mp == 1

# Test Enemies Stats
assert enemy.name == 'Goblin'
assert enemy.lv == 2
assert enemy.hp == 6
assert enemy.mp == 200
assert enemy.st == 4
assert enemy.ag == 6
assert enemy._max_hp == 6
assert enemy._max_mp == 4
assert enemy.gold == 6
assert enemy.exp == 12
assert enemy.random == 14

# Hero Attack
guy.attack(enemy)
assert enemy.hp == 5

# Hero Magic
guy.magic.rage(guy)
guy.magic.heal(guy)
guy.magic.fireball(enemy)
assert guy.st == 2 and guy.hp == 200
assert guy.mp == 189
assert enemy.dead is True and enemy.hp == -5

# Enemy Attack
enemy.attack(guy)
assert guy.hp == 196

# Enemy Magic
enemy.magic.big_attack(guy)
enemy.magic.buff(enemy)
enemy.magic.debuff(guy)
assert guy.hp == 188
assert enemy.st == 8
assert guy.st == 1
