''' All enemy classes.'''
from character import Character
from protagonist import Human
import csv


class Enemy(Character):
    ''' Base class for all enemies.'''

    def __init__(self, name, lv, species):
        self.species = species
        hp, mp, ag, st, exp, gold = self.get_species_stats(lv)
        Character.__init__(self, name, hp, mp, st, ag, lv)
        self.exp = exp
        self.gold = gold
        self.dead = False

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
        self.dead = True


class Rodent(Enemy):
    def __init__(self, name, lv):
        Enemy.__init__(self, name, lv, species='rat')

    def bite(self, target):
        self.black_magic(target=target, att_name='bite', stat='hp',
                         num=1, mp_cost=1)

    def heal(self):
        self.white_magic(att_name='Lick Wounds', stat='hp', num=1,  mp_cost=1)


class Goblin(Enemy):
    def __init__(self, name, lv):
        Enemy.__init__(self, name, lv, species='goblin')

    def punch(self, target):
        self.black_magic(target=target, att_name='Goblin Punch',
                         stat='hp', num=2, mp_cost=2)

    def anger(self):
        num = round(self.lv, -1) / 10 if self.lv >= 10 else 1
        mp = num * 2 if self.lv >= 10 else 1
        self.white_magic(att_name='Fury', stat='st', num=num, mp_cost=mp)

    def drain(self, target):
        self.black_magic(target=target, att_name='Intemidate', stat='st',
                         num=1, mp_cost=1)


# Guy = Human('Gohan',  2)
# print(Guy)
# # G = Goblin('RedGoblin', 1)
# # print(G)
# # Guy.attack(G)
# # # print(G.mp, G.st)
# # # G.anger()
# # # print(G.mp, G.st)
# Rat = Rodent('Rat', 3)
# # Rat.bite(Guy)
# # print(Guy)
# # G.drain(Guy)
# # print(Guy)
# Guy - Rat
# Guy.magic.heal()
# print(Guy)
# Guy.magic.rage()
# # Rat.heal()
# Guy.heal()
# print(Guy)
# Guy.rage()
# print(Guy)
# print(G)
# # Guy - Rat
# # Guy - Rat
# # Guy - Rat
# # Guy - Rat
