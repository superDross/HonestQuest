from HonestQuest.characters.character import Character
from HonestQuest.utils.print_text import print_centre
from HonestQuest.animations.animations import animations
from HonestQuest.magic.enemy_magic import EnemyMagic
import HonestQuest.utils.common as common
from HonestQuest.config import MODULE_PATH
import time
import csv
import os


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
        print_centre('{} is dead!\n'.format(self.name))
        self.dead = True

    def ai(self, target):
        ''' Enemy action determined by if else block.'''
        if not self.dead:
            actions = {'attack': 10, 'magic': 3}
            action = common.weighted_choice(actions)
            if self.mp > 1 and action == 'magic':
                spells = {'big_attack': 10, 'buff': 2, 'debuff': 1}
                choice = common.weighted_choice(spells)
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
        species (str, optional): determines which Enemy object to create.
        magic_names (dict): names of enemy magic attacks.

    Usage:
        factory = EnemyFactory()
        # generate random Enemy object
        enemy = factory.generate_enemy()
        # generate Enemy object that is a level 10 Goblin
        goblin = factory.generate_enemy(species='Goblin', lv=10)

    '''

    def __init__(self):
        self.lv = 1
        self._species = None
        self._species_dict = None
        self.magic_names = None

    def generate_enemy(self, species=None, lv=None):
        ''' Returns an Enemy object.

        If the species arg isn't parsed the the Enemy object
        returned is randomly selected.

        Args:
            species (str): species name used to generate Enemy object.
            lv (int): level of Enemy object.
        '''
        self.lv = self.lv if not lv else lv
        self.species = species
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

    @property
    def species(self):
        ''' str: sets the species attribute and sets the Enemy species stats
            as attributes. If a species arg isn't parsed then the species
            atribute is randomly generated.
        '''
        return self._species

    @species.setter
    def species(self, species):
        self._species = self._determine_species(species)
        self._species_dict = self._species_stats_dict(self.lv)[self.species]
        self.magic_names = {k: v for k, v in self._species_dict.items()
                            if not isinstance(v, int)}

    def _determine_species(self, species):
        ''' Weighted random determination of the enemy species,
            if a species name is not given.
        '''
        if not species:
            species2rate = {k: int(v['random'])
                            for k, v in self._species_stats_dict().items()}
            species = common.weighted_choice(species2rate)
        return species

    @staticmethod
    def _species_stats_dict(lv=None):
        ''' Open the stats sheet and return as a nested dict.
            {species: {stat: value, ...}

        Args:
            lv: desired enemy level, used to evaluate stats.
        '''
        all_species_dict = {}
        enemy_stats = os.path.join(MODULE_PATH, 'stats/enemy_stats.csv')
        with open(enemy_stats, mode='r') as infile:
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
