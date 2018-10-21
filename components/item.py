from damage_types import DamageType

class Item:
    def __init__(self, stack=1, use_function=None, targeting=None, targeting_message=None, power=None, to_cast=False,
                 radius=None, damage_type=DamageType.UNKNOWN, **kwargs):

        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.stack = stack
        self.function_kwargs = kwargs
        self.power = power
        self.to_cast = to_cast
        self.radius = radius
        self.damage_type = damage_type
