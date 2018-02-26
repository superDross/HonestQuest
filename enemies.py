import stats
import sys
import csv


class Character(object):
    def __init__(self, name, hp, mp, st, ag, lv):
        self.name = name
        self.hp = hp
        self.mp = mp
        self.st = st
        self.ag = ag
        self.lv = lv
        self.leveling = stats.leveling
        self._exp = 0
        self.gold = 0

    def __sub__(self, target):
        ''' Basic Attack.'''
        target.hp = target.hp - self.st
        msg = '{} does {} damage to {}'.format(
            self.name, self.st, target.name)
        print(msg)
        print('{} HP = {}\n'.format(target.name, target.hp))
        if target.hp <= 0:
            print('{} is dead!\n'.format(target.name))
            target.death(self)

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
                    msg = '{} has reached level {}!\n'.format(
                        self.name, self.lv)
                    print(msg)
                    break


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
        msg = '{} gained {} exp and {} gold\n'
        print(msg.format(target.name, self.exp, self.gold))
        target.exp += self.exp
        target.gold += self.gold


class Human(Character):
    def __init__(self, name, lv):
        hp, mp, ag, st = self.determine_stats(lv)
        Character.__init__(self, name, hp, mp, st, ag, lv)

    def determine_stats(self, lv):
        hp = lv * 10
        mp = lv * 2
        ag = lv * 4
        st = lv * 4
        return (hp, mp, ag, st)

    def death(self, *args):
        print('GAME OVER!!!!')
        sys.exit()

    def get_exp(self):
        msg = '{} has {} exp\n{} exp to the next level'
        next_lv_exp = self.leveling.get(self.lv + 1)
        exp_to_next_lv = next_lv_exp - self.exp
        print(msg.format(self.name, self.exp, exp_to_next_lv))


Guy = Human('Gohan',  1)
Goblin = Monster('Goblin', 2, species='goblin')
Goblin - Guy
Guy - Goblin
Guy - Goblin
Guy - Goblin
Guy - Goblin
