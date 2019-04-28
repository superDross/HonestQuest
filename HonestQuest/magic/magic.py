from HonestQuest.utils.print_text import print_centre


class Magic(object):
    """ Base class for a magic spell.

    Attributes:
        character (Character): object whom the spell will be assigned to.
        target (Character): object that will be the reciever of the spell.
        att_name (str): attack name.
        stat (str): targets statistical attribute to alter (hp, mp, ag or st).
        value (int): number to add/subtract from targets stat.
        mp_cost (int): number to deduct from character mp.
        operator (bool): whether to operatorrease or decrease stat.
    """

    def __init__(self, character, att_name, stat, value, mp_cost, operator, target):
        self._character = character
        self.att_name = att_name
        self.stat = stat
        self.value = value
        self.mp_cost = mp_cost
        self.operator = operator
        self.target = target

    def __call__(self):
        self._magic()

    def _magic(self):
        """ Performs magic and depletes _character mp."""
        per = self._reduce_mp()
        if per:
            self.target.alter_stat(self.stat, self.value, self.operator)
            self.target.check_hp()

    def _reduce_mp(self):
        """ Lower _character mp by a given value."""
        if self._character.mp >= self.mp_cost:
            self._character.mp -= self.mp_cost
            print_centre("{} uses {}!".format(self._character.name, self.att_name))
            return True
        elif self._character.mp < self.mp_cost:
            print_centre("You don't have enough mp to use {}.\n".format(self.att_name))
            return False
