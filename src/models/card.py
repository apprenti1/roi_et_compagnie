from dataclasses import dataclass

@dataclass
class Card:
    nom: str
    texture: str
    lieu: str
    id_lieu: int
    condition: str
    code_condition: str
    points: int
    effet_special: str
    id_effet_special: int
    card_type: str = "habitant"