from HonestQuest.characters.hero import Hero
from HonestQuest.characters.enemy import EnemyFactory
from HonestQuest.battle.battle_sequence import BattleSequence

# TESTING
# Create Objects
factory = EnemyFactory(2, 'Goblin')
enemy = factory.generate()
guy = Hero('Guy', 7)

# Set HP & MP for Test
guy.mp = 200
guy.hp = 200
enemy.mp = 200
guy.st = 1
guy.ag = 1
guy._max_hp = 1
guy._max_mp = 1
print(guy)
print(enemy)

# Test Hero Stats
assert guy.lv == 7
assert guy.hp == 200 and guy.mp == 200
assert guy.st == 1 and guy.ag == 1
assert guy._max_hp == 1 and guy._max_mp == 1

# Test Enemies Stats
assert enemy.name == 'Goblin'
assert enemy.lv == 2
assert enemy.hp == 6
assert enemy.mp == 200
assert enemy.st == 4
assert enemy.ag == 6
assert enemy._max_hp == 6
assert enemy._max_mp == 4
assert enemy.gold == 6
assert enemy.exp == 12
assert enemy.random == 14

# Hero Attack
guy.attack(enemy)
assert enemy.hp == 5

# Hero Magic
guy.magic.rage(guy)
guy.magic.heal(guy)
guy.magic.fireball(enemy)
assert guy.st == 2 and guy.hp == 200
assert guy.mp == 189
assert enemy.dead is True and enemy.hp == -5

# Enemy Attack
enemy.attack(guy)
assert guy.hp == 196

# Enemy Magic
enemy.magic.big_attack(guy)
enemy.magic.buff(enemy)
enemy.magic.debuff(guy)
assert guy.hp == 188
assert enemy.st == 8
assert guy.st == 1

# Create Objects
factory = EnemyFactory(2, 'Goblin')
enemy = factory.generate()
guy = Hero('Guy', 1)

# Set HP & MP for Test
guy.mp = 200
guy.hp = 200
guy.st = 5
enemy.mp = 200
enemy.exp = 200


m = BattleSequence(guy, enemy)
m.execute_main_menu()
