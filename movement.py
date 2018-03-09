''' Overworld and movement.'''
import os
import sys
import termios
import tty
import time


class Field(object):
    def __init__(self, height, width):
        self.hero = u"\U0001F6B6"
        self.tile = '.'
        self.height = height
        self.width = width
        self._field = None

    @property
    def field(self):
        f = [[self.tile for j in range(self.width)]
             for i in range(self.height)]
        self._field = f
        return f


class Movement(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = None

    def set_move(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if ch in ['w', 'W', 'a', 'A', 's', 'S', 'd', 'D']:
            self.direction = ch
        else:
            os.system('clear')
            print('Press WASD to move.')
            time.sleep(1)
            print(self.render())
            self.set_move()

    def move(self):
        if self.direction in ['w', 'W']:
            self.x = self._min_max(self.x-1, 0, self.height-1)
        elif self.direction in ['s', 'S']:
            self.x = self._min_max(self.x+1, 0, self.height-1)
        elif self.direction in ['d', 'D']:
            self.y = self._min_max(self.y+1, 0, self.width-1)
        elif self.direction in ['a', 'A']:
            self.y = self._min_max(self.y-1, 0, self.width-1)

    @staticmethod
    def _min_max(n, minn, maxn):
        return max(min(maxn, n), minn)


class OverWorld(Field, Movement):
    def __init__(self, height, width):
        Field.__init__(self, height, width)
        Movement.__init__(self)

    def render(self):
        mapped = ''
        new_field = self.field
        new_field[self.x][self.y] = self.hero
        for i in new_field:
            i.append('\n')
            mapped += ' '.join(i)
        return mapped
