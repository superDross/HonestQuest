import random
import os


def weighted_choice(d):
    ''' A weighted version of random.choice that takes a dict
        where key is what needs to be randomised and the value
        is the weight of the key.

    Args:
        d (dict):
    '''
    choice = random.choice([k for k in d for _ in range(d[k])])
    return choice


def clear():
    ''' Platform agnostic way to clear screen.'''
    os.system('cls' if os.name == 'nt' else 'clear')
