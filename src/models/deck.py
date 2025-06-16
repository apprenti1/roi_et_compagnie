import json

class Deck:
    def __init__(self, empty=False):
        self.cards = [] if empty else self.load_cards_from_json()

    def load_cards_from_json(self):
        with open('data/habitants.json') as f:
            return json.load(f)
