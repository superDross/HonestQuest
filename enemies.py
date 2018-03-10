''' All enemy classes.'''
from character import Character
import random
import csv


class Enemy(Character):
    ''' Randomly creates an enemy from the species stats sheet.'''

    def __init__(self, lv):
        self.species = self._determine_species()
        species_dict = self._species_stats_dict()[self.species]
        for k, v in species_dict.items():
            v = int(v) if v.isdigit() else v
            setattr(self, k, v)
        Character.__init__(self, self.species, self.hp, self.mp,
                           self.st, self.ag, lv)
        self.dead = False

    @staticmethod
    def _species_stats_dict():
        ''' Open the stats sheet as a nested dict.
            {species: {stat: value, ...}
        '''
        all_species_dict = {}
        with open('species_stats.csv', mode='r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            header = next(reader)
            for line in reader:
                mydict = dict(zip(header, line))
                all_species_dict[mydict['species']] = mydict
        return all_species_dict

    def _determine_species(self):
        ''' Weighted random determination of the enemy species.'''
        species2rate = {k: int(v['random'])
                        for k, v in self._species_stats_dict().items()}
        # species = random.choice(
        #     [k for k in species2rate for dummy in range(species2rate[k])])
        species = self.weighted_choice(species2rate)
        return species

    @staticmethod
    def weighted_choice(d):
        choice = random.choice([k for k in d for _ in range(d[k])])
        return choice

    def get_species_stats(self, lv):
        ''' Determine monster stats based on species and level.'''
        d = self._species_stats_dict()
        stats = []
        for stat in d.get(self.species):
            if stat.isdigit():
                stats.append(int(stat) * lv)
        return stats[:-1]

    def death(self, target):
        ''' Protagonist rewards upon death.'''
        msg = '{} gained {} exp and {} gold\n'
        print(msg.format(target.name, self.exp, self.gold))
        target.exp += self.exp
        target.gold += self.gold
        self.dead = True

    def big_attack(self, target):
        self.black_magic(target=target, att_name=self.attack_name,
                         stat='hp', num=2 * self.lv, mp_cost=2 * self.lv)

    def buff(self):
        self.white_magic(att_name=self.buff_name, stat=self.stat,
                         num=2 * self.lv, mp_cost=2 * self.lv)

    def debuff(self, target):
        self.black_magic(target=target, att_name=self.debuff_name,
                         stat=self.stat, num=2 * self.lv, mp_cost=2*self.lv)


if __name__ == '__main__':
    enemy = Enemy(lv=1)
    print(enemy)
    if enemy.mp > enemy.lv*2:
        spells = {'big_attack': 10, 'buff': 2, 'debuff': 1}
        choice = enemy.weighted_choice(spells)
        print(choice)
        getattr(enemy, choice)()



