from movement import OverWorld
from hero import Hero
from enemies import Enemy
from battle_menu import BattleMenu
from animations import animations
from print_text import print_middle, midscreen, centre_string
import pickle
import random
import time
import sys
import os


def main():
    h, w = (40, 93)
    resize_terminal(h, w)
    title_animation()
    guy = generate_hero()
    overworld = intiate_overworld(h, w)
    while True:
        enemy = enemy_generator(guy)
        animate_overworld(overworld, guy)
        battle_animation()
        battle(guy, enemy)
        guy.hp = guy._max_hp
        guy.mp = guy._max_mp
        guy.save()


def title_animation():
    os.system('clear')
    print_middle(animations['Title'])
    time.sleep(4)


def resize_terminal(height=40, width=93):
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=height, cols=width))


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


def intiate_overworld(height=40, width=93):
    ''' Initiate OverWorld class using terminal height and width as input.'''
    world = OverWorld(height=int(height * .9),
                      width=int(width / 2))
    # size = os.get_terminal_size()
    # world = OverWorld(height=int(size.lines * .9),
    #                   width=int(size.columns / 2))
    return world


def enemy_generator(hero):
    ''' Random enemy generator.'''
    low = hero.lv - 2 if hero.lv > 2 else 1
    high = hero.lv + 2
    lv = random.randint(low, high)
    return Enemy(lv)


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
