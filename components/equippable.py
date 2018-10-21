class Equippable:
    def __init__(self, slot, str_bonus=0, dex_bonus=0, resistance_bonus=0, defense_bonus=0, max_hp_bonus=0):
        self.slot = slot
        self.resistance_bonus = resistance_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.str_bonus = str_bonus
        self.dex_bonus = dex_bonus
