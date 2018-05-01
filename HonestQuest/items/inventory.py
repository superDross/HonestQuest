from HonestQuest.items.items import Item
import collections


class Inventory(list):
    ''' Container for all Item objects stored by a Character class.'''

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
            if not isinstance(item, Item):
                raise TypeError('{} is not an Item type.'.format(item))
            elif len(self) + 1 <= 10:
                self.append(item)
            else:
                print('Inventory limit reached.')
                break

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
