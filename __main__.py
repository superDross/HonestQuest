from movement import OverWorld
from protagonist import Human
from enemies import Enemy
from menu import Menu
import pickle
import random
import time
import sys
import os


def main():
    guy = generate_hero()
    size = os.get_terminal_size()
    # sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=100))
    # world = OverWorld(height=int(32*.9), width=int(100/2))
    world = OverWorld(height=int(size.lines * .9), width=int(size.columns / 2))
    while True:
        enemy = enemy_generator(guy)
        animate_overworld(world)
        print_middle(strings=['battle', 'Battle!', 'BATTLE!!!'])
        battle(guy, enemy)
        guy.hp = guy._max_hp
        guy.save()


def generate_hero():
    loaded_data = load()
    if loaded_data:
        return loaded_data
    else:
        name = get_name()
        guy = Human(name, 1)
        return guy


def load():
    ''' Load character data from save file.'''
    if os.path.exists('save_file.pkl'):
        with open('save_file.pkl', 'rb') as infile:
            return pickle.load(infile)


def get_name():
    os.system('clear')
    name = input('Type your name: ')
    print('\nAre you sure you want the name {}?'.format(name))
    confirm_name(name)
    return name


def confirm_name(name):
    decision = input('\nPress any Y to confirm or N to renenter.\n>>> ')
    if decision in ['y', 'Y']:
        return name
    elif decision in ['n', 'N']:
        get_name()
    else:
        return confirm_name(name)


def animate_overworld(world):
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


if __name__ == '__main__':
    main()
