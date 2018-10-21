# v16 Spellbook.


class Spell:
    def __init__(self, damage_type, mana_cost=50, power=0, to_cast=False, spell_function=None, targeting=None, targeting_message=None, **kwargs):
        # the spell effect
        self.spell_function = spell_function
        # kind of targeting. None : Self auto, Enemy, Radius, Floor
        self.targeting = targeting
        # targeting message
        self.targeting_message = targeting_message
        self.to_cast = to_cast

        # spell stats
        self.mana_cost = mana_cost
        self.power = power
        self.damage_type = damage_type

        # specific functions, from the spell itself.
        self.function_kwargs = kwargs
