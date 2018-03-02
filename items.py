''' All items player can use.'''
from custom_exceptions import StatError
from protagonist import Human


class Potion(object):
    def __init__(self, name, stat, value):
        if stat not in ['hp', 'mp', 'st', 'ag']:
            raise StatError(stat)
        self.name = name
        self.stat = stat
        self.value = value

potion = Potion('potion', 'hp', 2)
red_bull = Potion('red_bull', 'st', 2)
hero = Human('Jimmy', 1)
print(hero)
hero.items = [red_bull, potion]
print(hero.items)
hero.use_item('red_bull')
hero.use_item('potion')
print(hero)
