from src.models.card import Card
import json
import random
import copy
class DataLoader:
    def load_habitants(self):
        try:
            with open('data/habitants.json', 'r', encoding='utf-8') as f:
                habitants_data = json.load(f)
            
            deck_habitants = []
            
            for habitant_base in habitants_data:
                for i in range(4):
                    habitant = copy.deepcopy(habitant_base)
                    condition_id = random.randint(0, len(habitant['code_condition']) - 1)
                    deck_habitants.append(
                        Card(
                            nom=habitant['nom'],
                            texture=habitant['texture'],
                            lieu=habitant['lieu'],
                            id_lieu=habitant['id_lieu'],
                            condition=habitant['condition'],
                            code_condition=habitant['code_condition'][condition_id],
                            points=random.choice(habitant['points']),
                            effet_special=habitant['effet_special'],
                            id_effet_special=habitant['id_effet_special'],
                            card_type="habitant"
                        )
                    )
            random.shuffle(deck_habitants)
            return deck_habitants
            
        except FileNotFoundError:
            print("fichier habitants.json non trouvé")
        except Exception as e:
            print(f"erreur lors du chargement des habitants: {e}")
    
    def load_malus(self):
        try:
            with open('data/penalites.json', 'r', encoding='utf-8') as f:
                malus_data = json.load(f)
            
            deck_malus = []
            
            for malus_base in malus_data:
                for i in range(6):
                    malus = copy.deepcopy(malus_base)
                    card = Card(
                        nom=malus['nom'],
                        texture=malus['texture'],
                        lieu=malus['lieu'],
                        id_lieu=-1,
                        condition=None,
                        code_condition=None,
                        points= random.choice(malus['points']),
                        effet_special=None,
                        id_effet_special=-1,
                        card_type="malus"
                    )
                    
                    deck_malus.append(card)
            
            # Mélanger le paquet
            random.shuffle(deck_malus)
            return deck_malus
            
        except FileNotFoundError:
            print("Fichier penalites.json non trouvé")
        except Exception as e:
            print(f"Erreur lors du chargement des malus: {e}")