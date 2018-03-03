from movement import OverWorld
import curses
import random
import time
import os


def main(screen):
    ''' Overworld animation.'''
    size = os.get_terminal_size()
    world = OverWorld(height=int(size.lines/2), width=int(size.columns/2))
    n = 0
    while n != 1:
        screen.addstr(world.render())
        button = screen.getch()
        world.move(button)
        screen.refresh()
        screen.clear()
        n = random.randint(1, 20)


def battle(screen):
    ''' Battle transition sequence.'''
    n = 0
    while n != 50:
        screen.addstr(n, n, 'BATTLE')
        screen.refresh()
        time.sleep(0.02)
        n += 1


if __name__ == '__main__':
    curses.wrapper(main)
    curses.wrapper(battle)
