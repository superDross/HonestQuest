from movement import OverWorld
from hero import Hero
from enemies import Enemy
from battle_menu import BattleMenu
import pickle
import random
import time
import sys
import os


def main():
    guy = generate_hero()
    overworld = intiate_overworld()
    while True:
        enemy = enemy_generator(guy)
        animate_overworld(overworld, guy)
        battle_animation()
        battle(guy, enemy)
        guy.hp = guy._max_hp
        guy.save()


def generate_hero():
    ''' Create hero object or load hero data from save file.'''
    loaded_data = load()
    if loaded_data:
        return loaded_data
    else:
        name = get_name()
        guy = Hero(name, 1)
        return guy


def load():
    ''' Load character data from save file.'''
    if os.path.exists('save_file.pkl'):
        with open('save_file.pkl', 'rb') as infile:
            return pickle.load(infile)


def get_name():
    ''' Ask player for hero name.'''
    os.system('clear')
    msg = 'Type your name.\n'
    print_middle(msg)
    name = input(midscreen(msg))
    confirm_name(name)
    return name


def confirm_name(name):
    ''' Ask player to confirm name or to re-enter name.'''
    os.system('clear')
    print_middle('Are you sure you want the name {}?'.format(name))
    print(centre_string((('Press Y to confirm or N to renenter\n.'))))
    decision = input(midscreen(''))
    if decision in ['y', 'Y']:
        return name
    elif decision in ['n', 'N']:
        get_name()
    else:
        return confirm_name(name)


def intiate_overworld():
    ''' Initiate OverWorld class using terminal height and width as input.'''
    size = os.get_terminal_size()
    # sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=32, cols=100))
    # world = OverWorld(height=int(32*.9), width=int(100/2))
    world = OverWorld(height=int(size.lines * .9), width=int(size.columns / 2))
    return world


def enemy_generator(hero):
    ''' Random enemy generator.'''
    return Enemy(hero.lv)


def animate_overworld(world, guy):
    ''' Overworld animation.'''
    n = 0
    while n != 1:
        os.system('clear')
        print(guy)
        print(world.x, world.y)
        print(world.render())
        world.set_move()
        world.move()
        n = random.randint(1, 20)


def print_middle(string):
    ''' Prints a string at the center of the terminal.'''
    h = get_terminal_height()
    centered = centre_string(string)
    nl = '\n' * (int(h / 2))
    print(nl + centered)


def centre_string(string):
    ''' Place the string in the middle of a terminal line.'''
    nothing = midscreen(string)
    centered_string = nothing + string + nothing
    return centered_string


def midscreen(string):
    w = get_terminal_width()
    nothing = ' ' * int(((int(w - len(string)) - 1) / 2))
    return nothing


def get_terminal_width():
    size = os.get_terminal_size()
    return int(size.columns)


def get_terminal_height():
    size = os.get_terminal_size()
    return int(size.lines)


def battle_animation():
    ''' Animation that precedes battle.'''
    for battle in ['battle', 'Battle!', 'BATTLE!!!']:
        os.system('clear')
        print_middle(battle)
        time.sleep(0.4)


def battle(character, enemy):
    ''' Initiate battle menu.'''
    menu = BattleMenu(character, enemy)
    menu.battle_menu()


if __name__ == '__main__':
    main()
