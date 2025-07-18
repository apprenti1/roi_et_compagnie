import pygame
import pygame.freetype
import json
import copy
import random
from .dice import Dices
from .card import Card
from .player import Player
from services.data_loader import DataLoader
from typing import List, Dict, Any, Tuple, Optional, Union, Callable
from enum import Enum
from ui.inputs import InputField, SubmitButton, Form, InputType, LabelPosition
from ui.background import Background



class Board:
    def __init__(self, screen=None):
        self.screen = screen
        
        # Les 4 listes principales
        self.players = []  # List[Player]
        self.deck_habitants = []  # List[Card]
        self.deck_malus = []  # List[Card]
        self.lieux_remaining = {}  # Dict[int, int] - {id_lieu: nombre_restant}
        
        # État du jeu
        self.current_player_index = 0
        self.current_turn = 1
        self.remaining_throws = 3
        
        # Initialiser les données
        self.initialize_game_data()
        
        
        # État pour la gestion des formulaires
        self.setup_state = "ask_num_players"  # "ask_num_players" -> "ask_player_names" -> "done"
        self.tour = 0

        self.num_players_form = None
        self.player_names_form = None    
        
        self.dices = Dices(screen)  
        
        # Préchargement des images
        self.dos_habitant_image = pygame.transform.scale(pygame.image.load("assets/images/cards/back/1.png"), (150, 209))  
    
    def handle_event(self, event):
        if self.setup_state == "ask_num_players":
            if self.num_players_form:
                return self.num_players_form.handle_event(event)
        
        elif self.setup_state == "ask_player_names":
            if self.player_names_form:
                return self.player_names_form.handle_event(event)
        
        elif self.setup_state == "done":  # ← AJOUTER ÇA
            if self.dices:
                self.dices.event(event, self.screen)
                return True
        
        return False
    
        
    
    def reset_setup(self):
        """Remet à zéro la configuration."""
        self.players = []
        self.setup_state = "ask_num_players"
        self.num_players_form = None
        self.player_names_form = None
        self.num_players = 0
        
    def initialize_game_data(self):
        try:
            self.lieux_remaining = {0: 3, 1: 3, 2: 3, 3: 3, 4: 3}
            self.deck_habitants = DataLoader.load_habitants(self)
            self.deck_malus = DataLoader.load_malus(self)
        except Exception as e:
            print(f"Erreur lors de l'initialisation: {e}")
        

    def update(self, dt):
        if self.setup_state == "ask_num_players" and self.num_players_form:
            self.num_players_form.update(dt)
        elif self.setup_state == "ask_player_names" and self.player_names_form:
            self.player_names_form.update(dt)
    
    
    def show(self, screen):
        
        font_title = pygame.freetype.Font(None, 28)
        if self.setup_state == "ask_num_players":
            if not self.num_players_form:
                from ui.numplayerform import create_num_players_form
                create_num_players_form(self)
            
            if self.num_players_form:
                title_text = f"Nombre de joueurs"
                title_rect = font_title.get_rect(title_text)
                font_title.render_to(screen, ((screen.get_width() - title_rect.width) // 2, 80), title_text, (255, 255, 255))
                
                # Ne PAS recréer le formulaire ici - juste l'afficher
                self.num_players_form.draw(screen)
            
        elif self.setup_state == "ask_player_names":
            if self.player_names_form:
                # Titre
                title_text = f"Noms des {self.num_players} joueurs"
                title_rect = font_title.get_rect(title_text)
                font_title.render_to(screen, ((screen.get_width() - title_rect.width) // 2, 80), title_text, (255, 255, 255))
                
                # Formulaire
                self.player_names_form.draw(screen)
        
        elif self.setup_state == "done":
            
            if self.dices:
                self.dices.show(screen)
            
            
            # Affichage du plateau de jeu
            font = pygame.freetype.Font(None, 24)
            font_small = pygame.freetype.Font(None, 18)
            
            
            
            # encadré des informations du tour
            max_line_width = 0
            for i, player in enumerate(self.players):
                line_text = f"{i + 1}. {player.name}"
                line_width = font_small.get_rect(line_text).width
                max_line_width = max(max_line_width, line_width)
                
            info_rect = pygame.Rect(30, 40, 40+max(font.get_rect("Joueurs:").width, max_line_width), 70+25*len(self.players))
            pygame.draw.rect(screen, (0x282C34), info_rect, border_radius=10)
            pygame.draw.rect(screen, (0xFFFFFF), info_rect, 2, border_radius=10)
            
            # joueurs
            font.render_to(screen, (50, 60), "Joueurs:", (255, 255, 255))
            y = 90
            for i, player in enumerate(self.players):
                color = (255, 255, 0) if i == self.current_player_index else (200, 200, 255)
                font_small.render_to(screen, (70, y), f"{i + 1}. {player.name}", color)
                y += 25
            

            
            # Deck habitants
            deck_x, deck_y = 50, 180
            deck_surface = pygame.Surface((150, 209))

            # AVANT : deck_surface.fill((100, 100, 100))
            # APRÈS : Charger et blitter l'image # Redimensionner
            deck_surface.blit(self.dos_habitant_image, (0, 0))

            pygame.draw.rect(deck_surface, (255, 255, 255), (0, 0, 150, 209), 2, border_radius=10)
            habitants_count = str(len(self.deck_habitants))
            count_rect = font.get_rect(habitants_count)
            font.render_to(deck_surface, (60 - count_rect.width//2, 40 - count_rect.height//2), habitants_count, (255, 255, 255))
            screen.blit(deck_surface, (deck_x, deck_y))
            
            
            # # Deck malus
            # deck_y += 100
            # pygame.draw.rect(screen, (150, 50, 50), (deck_x, deck_y, 120, 80))
            # pygame.draw.rect(screen, (255, 255, 255), (deck_x, deck_y, 120, 80), 2)
            # font_small.render_to(screen, (deck_x + 10, deck_y + 10), "Malus", (255, 255, 255))
            # malus_count = str(len(self.deck_malus))
            # count_rect = font.get_rect(malus_count)
            # font.render_to(screen, (deck_x + 60 - count_rect.width//2, deck_y + 40), malus_count, (255, 255, 255))
            
            # # Lieux restants
            # deck_y += 100
            # pygame.draw.rect(screen, (50, 100, 150), (deck_x, deck_y, 120, 80))
            # pygame.draw.rect(screen, (255, 255, 255), (deck_x, deck_y, 120, 80), 2)
            # font_small.render_to(screen, (deck_x + 10, deck_y + 10), "Lieux", (255, 255, 255))
            # lieux_total = str(sum(self.lieux_remaining.values()))
            # count_rect = font.get_rect(lieux_total)
            # font.render_to(screen, (deck_x + 60 - count_rect.width//2, deck_y + 40), lieux_total, (255, 255, 255))