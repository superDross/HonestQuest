from HonestQuest.characters.hero import Hero
from HonestQuest.items.items import Potion

jim = Hero('jim', 10)
print(jim)
jim.inventory.add_item(Potion())
print(jim.inventory)
jim.inventory.use_item('Potion', jim)
print(jim)
#
