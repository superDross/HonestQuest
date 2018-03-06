''' Magic spells that can be used by Human class at specific levels.'''


class Spells(object):
    def __init__(self, character):
        self.character = character


class LV1(Spells):
    def __init__(self, character):
        super().__init__(character)

    def heal(self):
        self.character.white_magic(att_name='heal', stat='hp', num=1,
                                   mp_cost=1)


class LV2(LV1):
    def __init__(self, character):
        super().__init__(character)

    def rage(self):
        self.character.white_magic(att_name='rage', stat='st', num=1,
                                   mp_cost=1)
