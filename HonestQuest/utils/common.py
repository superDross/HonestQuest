import os
import random
import sys
import time


def weighted_choice(d):
    """ A weighted version of random.choice that takes a dict
        where key is what needs to be randomised and the value
        is the weight of the key.

    Args:
        d (dict):
    """
    choice = random.choice([k for k in d for _ in range(d[k])])
    return choice


def clear():
    """ Platform agnostic way to clear screen."""
    os.system("cls" if os.name == "nt" else "clear")


def flush_input():
    """ Platform agnostic way to clear key input."""
    if os.name == "nt":
        import msvcrt

        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        from termios import tcflush, TCIFLUSH

        tcflush(sys.stdin, TCIFLUSH)


def sleep():
    """ Sleep time used after all printed messages."""
    time.sleep(1.5)


def merge_two_dicts(x, y):
    """ Merge two dictionaries together."""
    z = x.copy()
    z.update(y)
    return z
