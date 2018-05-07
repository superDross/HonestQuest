from HonestQuest.items import items
from HonestQuest.menus.battle_menus import ItemMenu
from HonestQuest.menus.menu import Menu
from HonestQuest.characters.hero import Hero
from HonestQuest.characters.enemy import EnemyFactory


HERO = Hero('Dummy', 99)
factory = EnemyFactory()
ENEMY = factory.generate_enemy('Goblin', 99)


HERO.inventory.add_items(items.Potion(), items.Ether(),
                         items.ProteinShake(), items.RedBull(),
                         items.Molotov(), items.ManaCleaner(),
                         items.VodkaShots(), items.MegaPhone())

HERO.inventory.use_item('Potion', HERO)
