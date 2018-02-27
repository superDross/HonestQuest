''' All enemy classes.'''
from character import Character
from protagonist import Human
import sys
import csv


class Enemy(Character):
    ''' Base class for all enemies.'''

    def __init__(self, name, lv, species):
        self.species = species
        hp, mp, ag, st, exp, gold = self.get_species_stats(lv)
        Character.__init__(self, name, hp, mp, st, ag, lv)
        self.exp = exp
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


class Rodent(Enemy):
    def __init__(self, name, lv):
        Enemy.__init__(self, name, lv, species='rat')

    def bite(self, target):
        self.black_magic(target, multiplier=1.5, att_name='Bite', mp_cost=1)

    def heal(self):
        self.white_magic(multiplier=1, att_name='Lick Wounds', mp_cost=1)


class Goblin(Enemy):
    def __init__(self, name, lv):
        Enemy.__init__(self, name, lv, species='goblin')

    def punch(self, target):
        self.black_magic(target, multiplier=1.5,
                         att_name='Goblin Punch', mp_cost=2)

    def anger(self):
        inc = (self.lv/2) * self.st
        self.st += inc
        msg = '{} uses {}!\nStrength increase by {}\n'
        print(msg.format(self.name, 'Fury', inc))


Guy = Human('Gohan',  1)
G = Goblin('RedGoblin', 1)
Guy - G
Guy - G
G.punch(Guy)
# Rat = Rodent('Rat', 3)
# Rat.bite(Guy)
# Guy - Rat
# Rat.heal()
# Guy.heal()
# Guy - Rat
# Guy - Rat
# Guy - Rat
# Guy - Rat
