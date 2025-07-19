import os
from src.models.card import Card
import json
import random
import copy
import pygame
class DataLoader:
    def load_habitants():
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
            print("fichier habitants.json non trouvé load habitants")
        except Exception as e:
            print(f"erreur lors du chargement des habitants: {e}")
    
    def load_malus():
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
    
    def load_lieux():
        try:
            with open('data/lieux.json', 'r', encoding='utf-8') as f:
                lieux_data = json.load(f)
            
            deck_lieux = []
            
            for lieu in lieux_data:
                card = Card(
                    nom=lieu['nom'],
                    texture=lieu['texture'],
                    lieu=lieu['lieu'],
                    id_lieu=lieu['id_lieu'],
                    condition=lieu['condition'],
                    code_condition=lieu['code_condition'],
                    points=lieu['points'],
                    effet_special=None,
                    id_effet_special=-1,
                    card_type="lieu"
                )
                
                deck_lieux.append([3, card])
            
            return deck_lieux
            
        except FileNotFoundError:
            print("Fichier lieux.json non trouvé")
        except Exception as e:
            print(f"Erreur lors du chargement des lieux: {e}")
    
    def load_images():
        try:
            with open('data/habitants.json', 'r', encoding='utf-8') as f:
                habitants_data = json.load(f)
            print("DEBUG: habitants.json ouvert avec succès")
            
            habitants = {}
            
            for habitant in habitants_data:
                texture = habitant['texture']
                habitants[texture] = pygame.transform.scale(pygame.image.load(f"assets/images/cards/habitants/{texture}.png"), (150, 209))
                
            print("DEBUG: habitants.json ouvert avec succès")
            
            with open('data/penalites.json', 'r', encoding='utf-8') as f:
                malus_data = json.load(f)
            print("DEBUG: penalites.json ouvert avec succès")
            
            for malus in malus_data:
                texture = malus['texture']
                img = pygame.image.load(f"assets/images/cards/penalites/{texture}.png").convert_alpha()
                img = pygame.transform.scale(img, (150, 209))
                habitants[texture] = pygame.transform.scale(pygame.image.load("assets/images/cards/back/1.png"), (150, 209))
            
            backs = []
            for filename in os.listdir("assets/images/cards/back/"):
                if filename.endswith(".png"):
                    img = pygame.image.load(f"assets/images/cards/back/{filename}").convert_alpha()
                    img = pygame.transform.scale(img, (150, 209))
                    backs.append(img)

            
            decorations = []
            for filename in os.listdir("assets/images/cards/decorations/vertical/"):
                if filename.endswith(".png"):
                    img = pygame.image.load(f"assets/images/cards/decorations/vertical/{filename}").convert_alpha()
                    img = pygame.transform.scale(img, (150, 209))
                    decorations.append(img)
                    print(f"DEBUG: Chargement de l'image {filename} réussi")
                
            horizontal_decorations = []
            for filename in os.listdir("assets/images/cards/decorations/horisontal/"):
                if filename.endswith(".png"):
                    img = pygame.image.load(f"assets/images/cards/decorations/horisontal/{filename}").convert_alpha()
                    img = pygame.transform.scale(img, (209, 150))
                    horizontal_decorations.append(img)
                    print(f"DEBUG: Chargement de l'image {filename} réussi")
                
            
            lieux = {}
            for filename in os.listdir("assets/images/cards/lieux/"):
                if filename.endswith(".png"):
                    img = pygame.image.load(f"assets/images/cards/lieux/{filename}").convert_alpha()
                    img = pygame.transform.scale(img, (209, 150))
                    lieux[os.path.splitext(filename)[0]] = img
                    print(f"DEBUG: Chargement de l'image {filename} réussi")
                
                
            textures = {
                "habitants": habitants,
                "backs": backs,
                "decorations": decorations,
                "horizontal_decorations": horizontal_decorations,
                "lieux": lieux
            }
            
            
            return textures
            
        except FileNotFoundError as e:
            print(f"Fichier non trouvé: {e}")
            return {
                "habitants": {},
                "backs": [],
                "decorations": []
            }
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
            return {
                "habitants": {},
                "backs": [],
                "decorations": []
            }