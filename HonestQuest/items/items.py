""" All items player can use."""
from HonestQuest.utils.common import sleep
from HonestQuest.utils.print_text import print_centre


class Item(object):
    """ Items stored and used by Character classes.

    Attributes:
        name (str): name of the item.
        stat (str): the Character stat to modify (hp, mp, st or ag).
        operator (str): increase ('+') or decrease ('-') the Character stat.
        value (int): the number to increase or decrease the stat by.
        cost (int): amount of gold the item costs to buy.
        sell (int): amount of gold the item costs to sell.
        description (str): a summary of the items effects.
    """

    def __init__(self, name, stat, operator, value, cost, description):
        self.name = name
        self.stat = stat
        self.operator = operator
        self.value = value
        self.cost = cost
        self.sell = int(cost / 2)
        self.description = description

    def __call__(self, target):
        self.use(target)

    def __str__(self):
        return "{}:\t{}".format(self.name, self.description)

    def use(self, target):
        """ Increase/decrease the targets stat/attribute by the given value.

        Args:
             target (Character): object to use the item on.
        """
        self._use_msg()
        target.alter_stat(self.stat, self.value, self.operator)

    def _use_msg(self):
        print_centre("{} has been used!\n".format(self.name.title()))
        sleep()


class Potion(Item):
    def __init__(self):
        Item.__init__(
            self,
            name="Potion",
            stat="hp",
            operator="+",
            value=10,
            cost=10,
            description="Increase targets HP",
        )


class Ether(Item):
    def __init__(self):
        Item.__init__(
            self,
            name="Ether",
            stat="mp",
            operator="+",
            value=10,
            cost=30,
            description="Increase targets MP",
        )


class ProteinShake(Item):
    def __init__(self):
        Item.__init__(
            self,
            name="Protein Shake",
            stat="st",
            operator="+",
            value=10,
            cost=40,
            description="Increase targets ST",
        )

    def _use_msg(self):
        print_centre("Lets BRO DOWN with a {}!\n".format(self.name))
        sleep()


class RedBull(Item):
    def __init__(self):
        Item.__init__(
            self,
            name="Red Bull",
            stat="ag",
            operator="+",
            value=10,
            cost=30,
            description="Increase targets AG",
        )


class Molotov(Item):
    def __init__(self):
        Item.__init__(
            self,
            name="Molotov Cocktail",
            stat="hp",
            operator="-",
            value=50,
            cost=100,
            description="Decrease target HP",
        )

    def _use_msg(self):
        print_centre("You threw a {}!\n".format(self.name))
        sleep()


class ManaCleaner(Item):
    def __init__(self):
        Item.__init__(
            self,
            name="Mana Cleaner",
            stat="mp",
            operator="-",
            value=5,
            cost=20,
            description="Decrease target MP",
        )

    def _use_msg(self):
        print_centre("You uncorked a bottle of {}.\n".format(self.name))
        sleep()


class MegaPhone(Item):
    def __init__(self):
        Item.__init__(
            self,
            name="Mega Phone",
            stat="st",
            operator="-",
            value=10,
            cost=25,
            description="Decrease target ST",
        )

    def _use_msg(self):
        print_centre("You shrieked into a {}!!!\n".format(self.name))
        sleep()


class VodkaShots(Item):
    def __init__(self):
        super().__init__(
            name="Vodka Shots",
            stat="all",
            operator="+",
            value=50,
            cost=2000,
            description="All stats increase",
        )

    def use(self, target):
        for stat in ["hp", "mp", "ag", "st"]:
            self.stat = stat
            super().use(target)

    def _use_msg(self):
        print_centre("You slammed a {}!\n".format(self.name[:-1]))
        sleep()
