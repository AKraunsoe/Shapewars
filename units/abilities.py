
class Ability():
    def __init__(self, name, base_damage, multiplier, cost, multi_target, generate = 0):
        self.name = name
        self.multiplier = multiplier
        self.damage = base_damage*multiplier
        self.cost = cost
        self.generate = generate
        self.multi_target = multi_target
    
    def update_damage(self, damage):
        self.damage = damage*self.multiplier


BASE_ABILITIES = {4: "asdf",
                  5: "asdf",
                  10: "asdf"}

CIRCLE_ABILITIES = {2: "adsf",
                    3: "adsf",
                    6: "asdf",
                    9: "asdf"}

SQUARE_ABILITIES = {2: "adsf",
                    3: "adsf",
                    6: "asdf",
                    9: "asdf"}

TRIANGLE_ABILITIES = {2: "adsf",
                      3: "adsf",
                      6: "asdf",
                      9: "asdf"}