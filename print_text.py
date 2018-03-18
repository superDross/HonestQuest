''' A set of functions to aid printing strings.'''
import os


def print_middle(string):
    ''' Prints a string at the center of the terminal.'''
    if isinstance(string, list):
        print_middle(string[0])
        for s in string[1:]:
            print(centre_string(s))
    else:
        h = get_terminal_height()
        centered = centre_string(string)
        nl = '\n' * (int(h / 2))
        print(nl + centered)


def print_centre(string):
    if '\n' in string:
        string = [x for x in string.split('\n')]
    if isinstance(string, list):
        for s in string:
            print(centre_string(s))
    else:
        print(centre_string(string))


def centre_string(string):
    ''' Place the string in the middle of a terminal line.'''
    nothing = midscreen(string)
    centered_string = nothing + string + nothing
    return centered_string


def midscreen(string):
    w = get_terminal_width()
    nothing = ' ' * int(((int(w - len(string)) - 1) / 2))
    return nothing


def get_terminal_width():
    size = os.get_terminal_size()
    return int(size.columns)


def get_terminal_height():
    size = os.get_terminal_size()
    return int(size.lines)
