""" Magic to be assigned to Hero object upon accension to the described level.

Args:
    target (Character): character to cast spell upon.
"""
from HonestQuest.magic.magic import Magic


class LV1(object):
    def __init__(self, character):
        self._character = character

    def heal(self, target):
        """ Increase HP attribute of target object."""

        mag = Magic(
            character=self._character,
            att_name="Heal",
            stat="hp",
            value=3,
            mp_cost=1,
            operator="+",
            target=target,
        )
        mag()


class LV3(LV1):
    """ Increase ST attribute of target object."""

    def rage(self, target):
        mag = Magic(
            character=self._character,
            att_name="Rage",
            stat="st",
            value=1,
            mp_cost=1,
            operator="+",
            target=target,
        )
        mag()


class LV6(LV3):
    """ Decrease HP attribute of target object."""

    def fireball(self, target):
        mag = Magic(
            character=self._character,
            att_name="Fireball",
            stat="hp",
            value=10,
            mp_cost=10,
            operator="-",
            target=target,
        )
        mag()


class LV10(LV6):
    """ Increase hp attribute of traget object."""

    def midheal(self, target):
        mag = Magic(
            character=self._character,
            att_name="Midheal",
            stat="hp",
            value=5,
            mp_cost=5,
            operator="+",
            target=target,
        )
        mag()


class LV15(LV10):
    """ Increase AG attribute of target object."""

    def snort_coke(self, target):
        mag = Magic(
            character=self._character,
            att_name="Snort Coke",
            stat="ag",
            value=5,
            mp_cost=5,
            operator="+",
            target=target,
        )
        mag()


class LV20(LV15):
    """ Decrease HP attribute of target object."""

    def firewhirl(self, target):
        mag = Magic(
            character=self._character,
            att_name="Fire Whirl",
            stat="hp",
            value=25,
            mp_cost=25,
            operator="-",
            target=target,
        )
        mag()
