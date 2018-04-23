from HonestQuest.overworld.overworld import OverWorld
from HonestQuest.characters.hero import Hero
from HonestQuest.characters.enemy import EnemyFactory
from HonestQuest.battle.battle_sequence import BattleSequence
from HonestQuest.animations.animations import animations
from HonestQuest.utils.print_text import print_middle, midscreen, centre_string
from HonestQuest.utils.common import clear
from HonestQuest.config import MODULE_PATH
import pickle
import random
import time
import sys
import os


def main():
    h, w = (40, 93)
    resize_terminal(h, w)
    title_animation()
    hero = generate_hero()
    overworld = intiate_overworld(h, w)
    while True:
        overworld.animate()
        enemy_lv = level_randomiser(hero)
        enemy = enemy_generator(enemy_lv)
        initiate_battle(hero, enemy)
        hero.regenerate_max_stats()
        hero.save()


def resize_terminal(height=40, width=93):
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=height, cols=width))


def title_animation():
    clear()
    print_middle(animations['Title'])
    time.sleep(4)


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


def battle_animation():
    ''' Animation that precedes battle.'''
    for battle in ['battle', 'Battle!', 'BATTLE!!!']:
        clear()
        print_middle(battle)
        time.sleep(0.4)


def initiate_battle(hero, enemy):
    battle_animation()
    battle = BattleSequence(hero, enemy)
    battle.execute_main_menu()


def level_randomiser(hero):
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


if __name__ == '__main__':
    main()
