from death_functions import kill_monster


# v14 death for victory condition.

class Death:
    def __init__(self, death_function=kill_monster):
        self.death_function = death_function
