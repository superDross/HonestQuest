from HonestQuest.utils.print_text import print_centre
import operator


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
            print_centre('{} is already at the maximum value\n'.format(
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
