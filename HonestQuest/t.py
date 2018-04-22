class Menu(object):
    def __init__(self, opt):
        self._options = opt

    def __call__(self):
        self.handle_options()

    def handle_options(self):
        print(self._options)
        choice = input(">> ")
        self._options.get(choice)()


class MagicMenu(Menu):
    def __init__(self, hero, enemy):
        self.hero = hero
        self.enemy = enemy
        Menu.__init__(self, {'1': self.meteor})

    def meteor(self):
        print('Meteor!')
        self.enemy -= 2
        print('Enemy HP: {}'.format(self.enemy))


class MainMenu(Menu):
    def __init__(self, hero, enemy):
        self.hero = hero
        self.enemy = enemy
        self.magic_menu = MagicMenu(self.hero, self.enemy)
        self.items = None
        opts = {'1': self.attack,
                '2': self.magic_menu,
                '3': self.items}
        Menu.__init__(self, opts)

    def attack(self):
        print('Did damage!')
        self.enemy -= 1
        print('Enemy HP: {}'.format(self.enemy))


m = MainMenu(10, 10)
#m.handle_options()
import os
print(os.path.realpath(__file__).split('/'))
