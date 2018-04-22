from HonestQuest.magic.magic import Magic


class EnemyMagic(object):
    ''' Magic spells used by enemies.

    Attributes:
        enemy (Enemy): enemy object who the magic is assigned to.
        attack_name (str): name assigned to big attack spell.
        buff_name (str): name assigned to buff spell.
        debuff_name (str): name assigned to debuff spell.
        stat (str): statistic attribute (hp/mp/st/ag) used in
                    debuff/buff spells.
    '''

    def __init__(self, enemy, magic_names):
        '''
        Parameters:
            magic_names (dict): holds the values to the attack_name,
                                buff_name and debuff_name attributes.
        '''
        self.enemy = enemy
        self._set_attributes(magic_names)

    def _set_attributes(self, magic_names):
        ''' Transforms _magic_names dict into attributes.'''
        for k, v in magic_names.items():
            if not v.isdigit():
                setattr(self, k, v)

    def big_attack(self, target):
        ''' Large magic attack that deducts the enemy targets hp.'''
        mag = Magic(character=self.enemy, att_name=self.attack_name,
                    stat='hp', num=self.enemy.st * self.enemy.lv,
                    mp_cost=2 * self.enemy.lv, inc=False,
                    target=target)
        mag()

    def buff(self, target):
        ''' Increases the enemies statistic attribute (self.stat).'''
        mag = Magic(character=self.enemy, att_name=self.buff_name,
                    stat=self.stat, num=2 * self.enemy.lv,
                    mp_cost=2 * self.enemy.lv, inc=True,
                    target=target)
        mag()

    def debuff(self, target):
        ''' Decreases the enemies target statistic attribute (self.stat).'''
        mag = Magic(character=self.enemy, att_name=self.debuff_name,
                    stat=self.stat, num=2 * self.enemy.lv,
                    mp_cost=2 * self.enemy.lv, inc=False,
                    target=target)
        mag()
