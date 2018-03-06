''' All items player can use.'''
from custom_exceptions import StatError
from protagonist import Human


class Item(object):
    def __init__(self, name, stat, value, description):
        if stat not in ['hp', 'mp', 'st', 'ag']:
            raise StatError(stat)
        self.name = name
        self.stat = stat
        self.value = value
        self.description = description

    def __str__(self):
        return '{}:\t{}'.format(self.name, self.description)


class Consumable(Item):
    def __init__(self, name, stat, value, description):
        super().__init__(name, stat, value, description)


class Weapon(Item):
    def __init__(self, name, stat, value, description):
        super().__init__(name, stat, value, description)


potion = Consumable('potion', 'hp', 2, 'Increases HP by 2')
red_bull = Consumable('red_bull', 'st', 2, 'Increase ST by 2')
hero = Human('Jimmy', 1)
print(hero)
hero.items = [red_bull, potion]
print(hero.items)
hero.use_item('red_bull')
hero.use_item('potion')
print(hero)
print(potion)
