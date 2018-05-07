from HonestQuest.items.items import Item
from HonestQuest.utils.print_text import print_centre
from HonestQuest.utils import common
import collections


class Inventory(list):
    ''' Container for all Item objects stored by a Character class.

    Attributes:
        limit (int): maximum number of items that can be stored.
        full (boolean): whether the max number of items held has been reached.
    '''

    def __init__(self):
        self.limit = 8
        self.full = False
        list.__init__(self)

    def __str__(self):
        ''' Prints all Item names and descriptions stored in the Inventory.'''
        all_items = ['The following items are in your inventory:']
        counted = collections.Counter([x.name for x in self])
        for item, num in counted.items():
            all_items.append('{} x{}'.format(item, num))
        return '\n'.join(all_items)

    def add_items(self, *items):
        ''' Store an item, limited to 10.

        Args:
            items (Item): item(s) to store.
        '''
        for item in items:
            self._check_item_type(item)
            self._check_space()
            if self.full is False:
                self.append(item)

    def use_item(self, item, target):
        ''' Selects the Item in the Inventory and then increase/decrease
            the targets stat/attribute by the given Item value.

        Args:
            item (str): should match the desired Item classes name attribute.
            target (Character): object to use the item on.
        '''
        item = self.extract_item(item)
        item.use(target)
        self.remove(item)

    def extract_item(self, item):
        ''' Returns Item from the Inventory.

        Args:
            item (str): the name attribute of the Item you want to return.
        '''
        index = [x.name for x in self].index(item)
        return self[index]

    def remove_item(self, item):
        ''' Remove Item from Inventory.

        Args:
            item (str): the name attribute of the item you want to remove.
        '''
        index = [x.name for x in self].index(item)
        self.pop(index)

    def _check_space(self):
        ''' Mark the Inventory as full or not full.'''
        if len(self) + 1 <= self.limit:
            self.full = False
        else:
            self.full = True
            print_centre('Inventory limit reached.')
            common.sleep()

    def _check_item_type(self, item):
        ''' Raises error if parsed arg is not an Item type.'''
        if not isinstance(item, Item):
            raise TypeError('{} is not an Item type.'.format(item))
