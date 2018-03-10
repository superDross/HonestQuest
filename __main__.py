from movement import OverWorld
from protagonist import Human
from enemies import Enemy
from menu import Menu
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


def print_middle(strings, t=0.4):
    ''' Prints list of strings in the middle of
        the screen at a given time interval.'''
    size = os.get_terminal_size()
    w = int(size.columns)
    h = int(size.lines)
    nothing = ' ' * (int(w / 2) - 1)
    nl = '\n' * (int(h / 2))
    for battle in strings:
        os.system('clear')
        print(nl + nothing + battle + nothing)
        time.sleep(t)


def enemy_generator(hero):
    ''' Random enemy generator.'''
    return Enemy(hero.lv)


def battle(character, enemy):
    ''' Initiate battle menu.'''
    menu = Menu(character, enemy)
    menu.battle_menu()


def AI(enemy):
    enemy.attack(enemy.target)


if __name__ == '__main__':
    name = get_name()
    guy = Human(name, 1)
    size = os.get_terminal_size()
    world = OverWorld(height=int(size.lines / 2), width=int(size.columns / 2))
    while True:
        enemy = enemy_generator(guy)
        main(world)
        print_middle(strings=['battle', 'Battle!', 'BATTLE!!!'])
        battle(guy, enemy)
        guy.hp = guy._max_hp
