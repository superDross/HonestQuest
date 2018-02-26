import curses


class Field(object):
    def __init__(self, size=10):
        self.hero = u"\U0001F6B6"
        self.tile = '.'
        self.size = size
        self._field = None

    @property
    def field(self):
        f = [[self.tile for j in range(self.size)] for i in range(self.size)]
        self._field = f
        return f


class Movement(object):
    def __init__(self):
        self.x = 0
        self.y = 0

    def set_move(self, button):
        if button in [curses.KEY_UP, curses.KEY_DOWN,
                      curses.KEY_LEFT, curses.KEY_RIGHT]:
            self.direction = button
        else:
            raise IOError('Button must be an arrow key')

    def move(self, direction):
        if direction == curses.KEY_UP:
            self.x = max(0, (self.x - 1))
        elif direction == curses.KEY_DOWN:
            self.x = max(0, (self.x + 1))
        elif direction == curses.KEY_RIGHT:
            self.y = max(0, (self.y + 1))
        elif direction == curses.KEY_LEFT:
            self.y = max(0, (self.y - 1))


class OverWorld(Field, Movement):
    def __init__(self, size=10):
        Field.__init__(self, size)
        Movement.__init__(self)

    def render(self):
        mapped = ''
        new_field = self.field
        print(new_field)
        new_field[self.x][self.y] = self.hero
        for i in new_field:
            i.append('\n')
            mapped += ' '.join(i)
        return mapped
