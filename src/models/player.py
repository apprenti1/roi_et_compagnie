from .card import Card
class Player:
    def __init__(self, name):
        self.name = name
        self.deck : list[Card] = []
        self.shake_count = 3
        self.score = 0
        
    def calculate_score(self):
        self.score = sum(card.points for card in self.deck)