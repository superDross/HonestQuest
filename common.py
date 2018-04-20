import random


def weighted_choice(d):
    ''' A weighted version of random.choice that takes a dict
        where key is what needs to be randomised and the value
        is the weight of the key.
    '''
    # this should belong else where as its used by other classes
    choice = random.choice([k for k in d for _ in range(d[k])])
    return choice