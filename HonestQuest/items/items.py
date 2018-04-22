''' All items player can use.'''
from HonestQuest.utils.custom_exceptions import StatError


class Item(object):
    def __init__(self, name, stat, value, description):
        if stat not in ['hp', 'mp', 'st', 'ag']:
            raise StatError(stat)
        self.name = name
        self.stat = stat
        self.value = value
        self.description = description

    def __str__(self):
        return '{}:\t{}'.format(self.name, self.description)
