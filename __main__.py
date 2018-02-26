from movement import OverWorld
import curses
import random
import time


def main(screen):
    world = OverWorld(30)
    n = 0
    while n != 1:
        screen.addstr(world.render())
        button = screen.getch()
        world.move(button)
        screen.refresh()
        screen.clear()
        n = random.randint(1, 10)


def battle(screen):
    n = 0
    while n != 100:
        screen.addstr(n, n, 'BATTLE')
        screen.refresh()
        time.sleep(0.02)
        n += 1


if __name__ == '__main__':
    curses.wrapper(main)
    curses.wrapper(battle)
