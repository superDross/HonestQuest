from HonestQuest.utils.print_text import print_centre


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
