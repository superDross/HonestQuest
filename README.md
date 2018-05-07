# HonestQuest
A simple dependency free turn based terminal JRPG written in Python3.

## About

[![Demo Video - Image](docs/HonestQuestTitleScreen1.png?raw=True)](https://asciinema.org/a/knun7V2aC6wTb0Njf9P6BQ1ZA)

This game is inspired by the original [Dragon Quest](https://en.wikipedia.org/wiki/Dragon_Quest_(video_game)). It features magic that can be gained when leveling up, an item store, and random turn-based battles with enemy ascii art. The enemy type generation and move choice is performed by a weight random system, which keeps the player on their toes! 

## Installation
```
git clone https://github.com/superDross/HonestQuest
PYTHONPATH=$PYTHONPATH:/path/to/HonestQuest/
cd HonestQuest/
python3 HonestQuest
```

## Testing
```
cd HonestQuest/test
python3 -m unittest *.py -b
```
