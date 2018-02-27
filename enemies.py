import stats
import sys
import csv


class Character(object):
    def __init__(self, name, hp, mp, st, ag, lv):
        self.name = name
        self.hp = hp
        self._max_hp = hp
        self.mp = mp
        self.st = st
        self.ag = ag
        self.lv = lv
        self._exp = 0
        self.gold = 0

    def __sub__(self, target):
        ''' Basic Attack.'''
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

    @property
    def exp(self):
        return self._exp


class Monster(Character):
    def __init__(self, name, lv, species):
        self.species = species
        hp, mp, ag, st, exp, gold = self.get_species_stats(lv)
        Character.__init__(self, name, hp, mp, st, ag, lv)
        self._exp = exp
        self.gold = gold

    @staticmethod
    def _species_stats_dict():
        ''' Open the stats sheet as a dict.'''
        with open('species_stats.csv', mode='r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            next(reader)
            mydict = {rows[0]: rows[1:] for rows in reader}
            return mydict

    def get_species_stats(self, lv):
        ''' Determine monster stats based on species and level.'''
        d = self._species_stats_dict()
        stats = [int(x) * lv for x in d.get(self.species)]
        return stats

    def death(self, target):
        ''' Protagonist rewards upon death.'''
        msg = '{} gained {} exp and {} gold\n'
        print(msg.format(target.name, self.exp, self.gold))
        target.exp += self.exp
        target.gold += self.gold
        sys.exit()


class Rodent(Monster):
    def __init__(self, name, lv):
        Monster.__init__(self, name, lv, species='rat')

    def bite(self, target):
        self.black_magic(target, multiplier=1.5, att_name='bite', mp_cost=1)

    def heal(self):
        self.white_magic(multiplier=1, att_name='lick wounds', mp_cost=1)


class Human(Character):
    def __init__(self, name, lv, items=[]):
        hp, mp, ag, st = self.determine_stats(lv)
        Character.__init__(self, name, hp, mp, st, ag, lv)
        self.items = items
        self.leveling = stats.leveling

    def __str__(self):
        return '{}(Level={}, HP={}, MP={}, ST={}, AG={})\n'.format(
            self.name, self.lv, self.hp, self.mp, self.st, self.ag)

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value):
        ''' Determine level after increasing exp.'''
        self._exp += value
        self.determine_level()

    def determine_level(self):
        ''' Determine level based upon exp value.'''
        next_level_exp = self.leveling.get(self.lv + 1)
        for leveled, experience in self.leveling.items():
            if self._exp >= next_level_exp:
                if experience > self._exp:
                    self.lv = leveled - 1
                    msg = '{} has reached level {}!'.format(
                        self.name, self.lv)
                    print(msg)
                    print(self)
                    break

    def determine_stats(self, lv):
        hp = lv * 5
        mp = lv * 2
        ag = lv * 1
        st = lv * 1
        return (hp, mp, ag, st)

    def heal(self):
        self.white_magic(multiplier=1, att_name='heal', mp_cost=1)

    def death(self, *args):
        print('GAME OVER!!!!')
        sys.exit()

    def get_exp(self):
        msg = '{} has {} exp\n{} exp to the next level'
        next_lv_exp = self.leveling.get(self.lv + 1)
        exp_to_next_lv = next_lv_exp - self.exp
        print(msg.format(self.name, self.exp, exp_to_next_lv))


Guy = Human('Gohan',  1)
Rat = Rodent('Rat', 3)
Rat.bite(Guy)
Guy - Rat
Rat.heal()
Guy.heal()
Guy - Rat
Guy - Rat
Guy - Rat
Guy - Rat
