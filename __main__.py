from movement import OverWorld
from protagonist import Human
from enemies import Rodent
from menu import Menu
import curses
import random
import time
import os


def main(screen):
    ''' Overworld animation.'''
    size = os.get_terminal_size()
    world = OverWorld(height=int(size.lines / 2), width=int(size.columns / 2))
    n = 0
    while n != 1:
        screen.addstr(world.render())
        button = screen.getch()
        world.move(button)
        screen.refresh()
        screen.clear()
        n = random.randint(1, 20)


def battle_transition(screen):
    ''' Battle transition sequence.'''
    n = 0
    while n != 50:
        screen.addstr(n, n, 'BATTLE')
        screen.refresh()
        time.sleep(0.02)
        n += 1


def battle(character, enemy):
    ''' Initiate battle menu.'''
    menu = Menu(character, enemy)
    menu.battle_menu()


if __name__ == '__main__':
    guy = Human('Guy', 2)
    rat = Rodent('rat', 2)
    while True:
        curses.wrapper(main)
        curses.wrapper(battle_transition)
        battle(guy, rat)
