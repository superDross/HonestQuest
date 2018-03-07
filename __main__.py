from movement import OverWorld
from protagonist import Human
from enemies import Rodent
from menu import Menu
import random
import time
import os


def main():
    ''' Overworld animation.'''
    size = os.get_terminal_size()
    world = OverWorld(height=int(size.lines / 2), width=int(size.columns / 2))
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
    nothing = ' '*(int(w/2)-1)
    nl = '\n'*(int(h/2))
    for battle in ['battle', 'Battle!', 'BATTLE!!!']:
        os.system('clear')
        print(nl+nothing+battle+nothing)
        time.sleep(0.4)


def battle(character, enemy):
    ''' Initiate battle menu.'''
    menu = Menu(character, enemy)
    menu.battle_menu()


if __name__ == '__main__':
    guy = Human('Guy', 1)
    while True:
        # some func thatrandomly generates enemy
        rat = Rodent('rat', 2)
        main()
        battle_transition()
        battle(guy, rat)
