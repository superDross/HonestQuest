from HonestQuest.overworld.overworld import OverWorld
from HonestQuest.characters.hero import Hero
from HonestQuest.characters.enemy import EnemyFactory
from HonestQuest.sequences.battle_sequence import BattleSequence
from HonestQuest.sequences.store_sequence import StoreSequence
from HonestQuest.animations.animations import animations
from HonestQuest.utils.print_text import print_middle, midscreen, centre_string
from HonestQuest.utils.common import clear
from HonestQuest.config import MODULE_PATH
import pickle
import random
import time
import sys
import os


def resize_terminal(height, width):
    clear()
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=height, cols=width))
    # below code prevents title animation from printing off-centre.
    print('')
    time.sleep(0.1)


def title_animation():
    ''' Show game title screen for a few seconds.'''
    clear()
    print_middle(animations['Title'])
    time.sleep(3)


def generate_hero():
    ''' Create Hero object or load hero data from save file.'''
    loaded_data = load_hero()
    if loaded_data:
        return loaded_data
    else:
        name = get_name()
        hero = Hero(name, 1)
        return hero


def load_hero():
    ''' Load hero character data from save file.'''
    save_file = os.path.join(MODULE_PATH, 'save_file.pkl')
    if os.path.exists(save_file):
        with open(save_file, 'rb') as infile:
            return pickle.load(infile)


# Turn into Menu and place in menu/ dir?
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


# Turn into Menu and place in menu/ dir?
def get_name():
    ''' Ask player for hero name.'''
    os.system('clear')
    msg = 'Type your name.\n'
    print_middle(msg)
    name = input(midscreen(msg))
    confirm_name(name)
    return name


def intiate_overworld(height=40, width=93):
    ''' Initiate OverWorld class using terminal height and width as input.'''
    world = OverWorld(height=int(height * .9),
                      width=int(width / 2))
    return world


# place in animation dir?
def battle_animation():
    ''' Animation that precedes battle.'''
    for battle in ['battle', 'Battle!', 'BATTLE!!!']:
        clear()
        print_middle(battle)
        time.sleep(0.4)


def initiate_battle(hero, enemy):
    ''' Initiates battle sequence.'''
    battle_animation()
    battle = BattleSequence(hero, enemy)
    battle.execute()


def level_randomiser(hero):
    ''' Randomly generates a lv that is +/-2 that of hero.lv'''
    if hero.lv >= 3:
        low = hero.lv - 2
        high = hero.lv + 2
        lv = random.randint(low, high)
    else:
        lv = hero.lv
    return lv


def enemy_generator(lv):
    ''' Random enemy generator.'''
    factory = EnemyFactory()
    enemy = factory.generate_enemy(lv=lv)
    return enemy


def animate_overworld(overworld, hero):
    ''' Overworld animation that moves character upon key press.'''
    n = 0
    while n != 1:
        clear()
        overworld.key_press.print_controls()
        overworld.field.render_field()
        overworld.key_press.set_key()
        overworld.move_hero()
        if overworld.field.x == overworld.field.x_store and \
           overworld.field.y == overworld.field.y_store:
            StoreSequence(hero).execute()
       # n = random.randint(1, 20)


def main():
    h, w = (40, 93)
    resize_terminal(h, w)
    title_animation()
    hero = generate_hero()
    overworld = intiate_overworld(h, w)
    while True:
        # overworld.animate()
        animate_overworld(overworld, hero)
        enemy_lv = level_randomiser(hero)
        enemy = enemy_generator(enemy_lv)
        initiate_battle(hero, enemy)
        hero.regenerate_max_stats()
        hero.save()


if __name__ == '__main__':
    main()
