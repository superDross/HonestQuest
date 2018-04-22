''' Magic to be assigned to Hero object upon accension to the described level.

Args:
    target (Character): character to cast spell upon.
'''
from HonestQuest.magic.magic import Magic


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
