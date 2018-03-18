## Characters
### Inherit
```
Rat ---> Enemy ---> Character


	 ---> Stats ---> Character
	|
Human --
	|
	 ---> Actions -> Character
```
### Idea
Perhaps have everything as a class (Stats, Attack, Movement, Overworld, Magic, Item) and a Character is stored in the Items e.g. self.character. 

### Classes
Character:
	- Name
	- Stats (HP, MP, ST, AG, LEVEL, MAX\_HP, MAX\_MP)
	- Basic Attack
	- Black Magic
	- White Magic
	- Item storage
	- Item usage

Character has a lot of methods with LOTS of ARGS being passed around. Perhap

Enemy:
	- Species
	- Means to determine stats
	- EXP and Gold to reward Protagonist
	- Death and means to transfer EXP & Gold


Specific Enemy:
	- Attacks


Hero:
	- Leveling dict {lv:exp}
	- Means to determine initial stats
	- Means to determine stats upon level up 
	- Attacks
	- Death
