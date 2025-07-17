import json
class Citizen:
    def __init__(self, data_path):
        data = json.load(open(data_path, 'r'))
        self.nom = nom
        self.texture = texture
        self.lieu = lieu
        self.id_lieu = id_lieu
        self.condition = condition
        self.code_condition = code_condition if code_condition is not None else [
            "all(dice % 2 == 0 for dice in dices.dices)",
            "all(dice % 2 == 1 for dice in dices.dices)"
        ]
        self.texture_conditions = texture_conditions
        self.points = points if points is not None else [2, 4]
        self.effet_special = effet_special

