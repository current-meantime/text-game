class Weapon: # unfinished
    def __init__(self, name, damage, effect=None):
        self.name = name
        self.damage = damage
        self.effect = effect

    def __str__(self):
        return f"{self.name} (DMG: {self.damage})"
