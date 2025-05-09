class Player: # takie przykładowe, do zmiany ofc
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.lvl = 1
        self.xp = 0
        self.inventory = []
        self.weapon = None
        self.effects = []

    def take_damage(self, amount):
        self.hp -= amount
        print(f"You took damage of {amount} HP.")
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        self.hp += amount
        print(f"You healed {amount} HP.")
        if self.hp > 100:
            self.hp = 100

    def is_alive(self):
        return self.hp > 0
    
    def gain_experience(self, amount):
        self.xp += amount
        print(f"You gained {amount} XP.")
        if self.xp > 100 * self.lvl:
            self.lvl += 1
            print(f"{self.name} has leveled up!")