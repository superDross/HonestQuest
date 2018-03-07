from movement import OverWorld
from protagonist import Human
from menu import Menu
import enemies
import random
import time
import os


def get_name():
    os.system('clear')
    name = input('Type your name: ')
    print('Are you sure you want the name {}?'.format(name))
    confirm_name(name)
    return name


def confirm_name(name):
    decision = input('Press any y to confirm or n to renenter.\n')
    if decision == 'y':
        return name
    elif decision == 'n':
        get_name()
    else:
        return confirm_name(name)


def main(world):
    ''' Overworld animation.'''
    n = 0
    while n != 1:
        os.system('clear')
        print(world.x, world.y)
        print(world.height, world.width)
        print(world.render())
        world.set_move()
        world.move()
        n = random.randint(1, 20)


def battle_transition():
    ''' Battle transition sequence.'''
    size = os.get_terminal_size()
    w = int(size.columns)
    h = int(size.lines)
    nothing = ' ' * (int(w / 2) - 1)
    nl = '\n' * (int(h / 2))
    for battle in ['battle', 'Battle!', 'BATTLE!!!']:
        os.system('clear')
        print(nl + nothing + battle + nothing)
        time.sleep(0.4)


def enemy_generator(hero):
    ''' Random enemy generator.'''
    lv = hero.lv
    baddies = [enemies.Rodent('Rat', lv),
               enemies.Goblin('Red Goblin', lv)]
    return random.choice(baddies)


def battle(character, enemy):
    ''' Initiate battle menu.'''
    menu = Menu(character, enemy)
    menu.battle_menu()


if __name__ == '__main__':
    name = get_name()
    guy = Human(name, 1)
    size = os.get_terminal_size()
    world = OverWorld(height=int(size.lines / 2), width=int(size.columns / 2))
    while True:
        enemy = enemy_generator(guy)
        main(world)
        battle_transition()
        battle(guy, enemy)
