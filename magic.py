''' Magic spells that can be used by Human class at specific levels.'''


class Spells(object):
    def __init__(self, character):
        self.character = character


class LV1(Spells):
    def __init__(self, character):
        super().__init__(character)

    def heal(self):
        self.character.white_magic(att_name='Heal', stat='hp', num=1,
                                   mp_cost=1)


class LV3(LV1):
    def __init__(self, character):
        super().__init__(character)

    def rage(self):
        self.character.white_magic(att_name='Rage', stat='st', num=1,
                                   mp_cost=1)


class LV6(LV3):
    def __init__(self, character):
        super().__init__(character)

    def fireball(self):
        self.character.black_magic(att_name='Fireball', stat='hp', num=10,
                                   mp_cost=10)


class LV10(LV6):
    def __init__(self, character):
        super().__init__(character)

    def midheal(self):
        self.character.white_magic(att_name='Midheal', stat='hp', num=5,
                                   mp_cost=5)


class LV15(LV10):
    def __init__(self, character):
        super().__init__(character)

    def snort_coke(self):
        self.character.white_magic(att_name='Snort Coke', stat='ag', num=5,
                                   mp_cost=5)


class LV20(LV15):
    def __init__(self, character):
        super().__init__(character)

    def firewhirl(self):
        self.character.black_magic(att_name='Fire Whirl', stat='hp', num=25,
                                   mp_cost=25)
