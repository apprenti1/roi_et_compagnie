from .card import Card
class Player:
    def __init__(self, name):
        self.name = name
        self.deck : list[Card] = []
        self.shake_count = 3