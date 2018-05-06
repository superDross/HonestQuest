from HonestQuest.items import items
from HonestQuest.menus.battle_menus import ItemMenu
from HonestQuest.menus.menu import Menu, SubMenu
from HonestQuest.characters.hero import Hero


jim = Hero('jim', 10)
jim.inventory = [items.Ether(), items.Potion()]

d = Menu({1: 'one', 2: 'two'}, 'onetwo')
m = ItemMenu(jim, d)
# m.handle_options()

# b.handle_options()

import operator


class Item(object):
    def __init__(self, name, stat, value, operation):
        self.name = name
        self.stat = stat
        self.value = value
        self.op = {'+': operator.add,
                   '-': operator.sub}
        self.op_func = self.op.get(operation)

    def _use_msg(self):
        print('{} has been used!\n'.format(self.name.title()))


class Inventory(list):
    def __str__(self):
        all_items = []
        for x in self:
            all_items.append(x.name)
        return '\n'.join(all_items)

    def use_item(self, item, target):
        ''' Increase/decrease the targets stat/attribute by the given value.

        Args:
            target (Character): object to use the item on.
        '''
        item = self._extract_item(item)
        item._use_msg()
        target_stat = getattr(target, item.stat)
        updated_target_stat = item.op_func(target_stat, item.value)
        setattr(target, item.stat, updated_target_stat)
        updown = 'increased' if item.op_func == operator.add else 'decreased'
        print('{} {} {} by {}\n'.format(target.name, item.stat.upper(),
                                        updown, item.value))
        self.remove(item)

    def _extract_item(self, item):
        index = [x.name for x in self].index(item)
        return self[index]


jim.inventory = Inventory([Item('Potion', 'hp', 10, '+'),
                           Item('Ether', 'mp', 5, '+')])
print(jim.inventory)
# jim.inventory.use_item('Potion', jim)


jim.hp = 49
print(jim.above_max('hp', 3))

