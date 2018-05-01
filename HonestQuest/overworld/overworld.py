''' Overworld and movement.'''
from HonestQuest.utils.common import clear
import sys
import termios
import tty
import random


class Field(object):
    ''' Generates the overworld image.

    Attributes:
        self.hero (str): unicode character representing player avatar.
        self.store (str): unicode character representing the shop.
        self.tile (str): holds a single tile character of the field.
        self.height (int): number of rows the field has.
        self.width (int): number of columns the field has.
        self.x (int): row co-ordinate for hero.
        self.y (int): column co-ordinate for hero.
    '''

    def __init__(self, height, width, x, y):
        self.hero = u"\U0001F6B6"
        self.store = u"\u2302"
        self.tile = '.'
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def generate_field_matrix(self):
        ''' Generates a 2D matrix representing the overworld field.'''
        field = []
        for _ in range(self.height):
            line = []
            for _ in range(self.width):
                line.append(self.tile)
            field.append(line)
        return field

    def generate_field_objects(self, matrix):
        ''' Places the hero and store on the field matrix.'''
        matrix[self.x][self.y] = self.hero
        matrix[int(self.height / 2)][int(self.width / 2)] = self.store
        return matrix

    def render_field(self):
        ''' Renders the full field as a string.'''
        mapped = ''
        matrix = self.generate_field_matrix()
        self.generate_field_objects(matrix)
        for row in matrix:
            row.append('\n')
            mapped += ' '.join(row)
        print(mapped)
        return mapped


class Direction(object):
    ''' Key press representing direction in the overworld.'''

    def __init__(self):
        self.direction = None

    def record_keypress(self):
        ''' Waits for user to press and key and returns it.'''
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def set_key(self):
        ''' Key press is recorded in self.direction variable if it is valid.'''
        ch = self.record_keypress()
        if ch in ['w', 'W', 'a', 'A', 's', 'S', 'd', 'D']:
            self.direction = ch
            return ch
        elif ch in ['x', 'X']:
            sys.exit()
        else:
            clear()
            self.print_controls()
            self.set_key()

    def print_controls(self):
        print('Press WASD to move. Press X to exit.')


class OverWorld(object):
    ''' The overworld of the game.

    Attributes:
        self.height (int): height of field.
        self.width (int): width of field.
        self.field (Field): the overworld field.
        self.key_press (Direction): stores user key press movements.

    Usage:
        world = OverWorld(height=20, width=20)
        world.animate()
    '''

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = Field(height, width, 0, 0)
        self.key_press = Direction()

    def animate(self):
        ''' Overworld animation that moves character upon key press.'''
        n = 0
        while n != 1:
            clear()
            self.key_press.print_controls()
            self.field.render_field()
            self.key_press.set_key()
            self.move_hero()
            n = random.randint(1, 20)

    def move_hero(self):
        ''' Moves hero on field according to the users key press.'''
        if self.key_press.direction in ['w', 'W']:
            self.field.x = self._min_max(
                self.field.x - 1, 0, self.field.height - 1)
        elif self.key_press.direction in ['s', 'S']:
            self.field.x = self._min_max(
                self.field.x + 1, 0, self.field.height - 1)
        elif self.key_press.direction in ['d', 'D']:
            self.field.y = self._min_max(
                self.field.y + 1, 0, self.field.width - 1)
        elif self.key_press.direction in ['a', 'A']:
            self.field.y = self._min_max(
                self.field.y - 1, 0, self.field.width - 1)

    @staticmethod
    def _min_max(n, minn, maxn):
        ''' Ensures n never goes above or below a give min and max number.'''
        return max(min(maxn, n), minn)
