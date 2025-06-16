import dice
import deck

class Board:
    def __init__(self):
        self.deck = deck.Deck()
        self.citizens = []
        self.players = []
        self.malus = []
        self.places = []
        self.dices = dice.Dices()
        
    def set_players(self, players):
        self.players = players
        
    def set_citizens(self, citizens):
        self.citizens = citizens
    
    def set_places(self, places):
        self.places = places
        
    def set_malus(self, malus):
        self.malus = malus
        