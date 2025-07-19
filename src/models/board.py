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
        
        # les 4 listes principales
        self.players = []
        self.deck_habitants = []
        self.deck_malus = []
        self.deck_lieux = []
        
        # etat du jeu
        self.current_player_index = 0
        self.current_turn = 1
        self.remaining_throws = 3
        
        # initialiser les données
        self.initialize_game_data()
        
        
        # etat pour la gestion des formulaires
        self.setup_state = "ask_num_players"  # "ask_num_players" -> "ask_player_names" -> "done"
        self.tour = 0

        self.num_players_form = None
        self.player_names_form = None    
        
        self.dices = Dices(screen)  
        
        # Préchargement des images
        self.textures = DataLoader.load_images()
    
    def handle_event(self, event):
        if self.setup_state == "ask_num_players":
            if self.num_players_form:
                return self.num_players_form.handle_event(event)
        
        elif self.setup_state == "ask_player_names":
            if self.player_names_form:
                return self.player_names_form.handle_event(event)
        
        elif self.setup_state == "done":
            if self.dices:
                self.dices.event(event, self.screen)
                return True
        
        return False
    
        
    
    def reset_setup(self):
        self.players = []
        self.setup_state = "ask_num_players"
        self.num_players_form = None
        self.player_names_form = None
        self.num_players = 0
        
    def initialize_game_data(self):
        try:
            self.deck_lieux = DataLoader.load_lieux()
            self.deck_habitants = DataLoader.load_habitants()
            self.deck_malus = DataLoader.load_malus()
        except Exception as e:
            print(f"Erreur lors de l'initialisation: {e}")
        

    def mouse_in_card(self, x, y, width, height):
        mouse_pos = pygame.mouse.get_pos()
        card_rect = pygame.Rect(x, y, width, height)
        return card_rect.collidepoint(mouse_pos)

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
            
            
            # afichage du plateau de jeu
            font = pygame.freetype.Font(None, 24)
            font_small = pygame.freetype.Font(None, 18)
            
            
            
            # encadré des informations du tour
            max_line_width = 0
            for i, player in enumerate(self.players):
                line_text = f"{i + 1}. {player.name}"
                line_width = font_small.get_rect(line_text).width
                max_line_width = max(max_line_width, line_width)
                
            info_rect = pygame.Rect(30, 40, 40+max(font.get_rect("Joueurs:").width, max_line_width), 60+25*len(self.players))
            pygame.draw.rect(screen, (0x282C34), info_rect, border_radius=10)
            pygame.draw.rect(screen, (0xFFFFFF), info_rect, 2, border_radius=10)
            
            # joueurs
            font.render_to(screen, (50, 60), "Joueurs:", (255, 255, 255))
            y = 90
            for i, player in enumerate(self.players):
                color = (255, 255, 0) if i == self.current_player_index else (200, 200, 255)
                font_small.render_to(screen, (70, y), f"{i + 1}. {player.name}", color)
                y += 25
            

            
            # deck habitants
            deck_x, deck_y = 30, 240
            deck_surface = pygame.Surface((150, 209))
            deck_surface.blit(self.textures["backs"][0], (0, 0))

            pygame.draw.rect(deck_surface, (255, 255, 255), (0, 0, 150, 209), 3, border_radius=10)
            habitants_count = len(self.deck_habitants)
            count_rect = font.get_rect(str(habitants_count-5))
            font.render_to(deck_surface, (75 - count_rect.width//2, 105 - count_rect.height//2), str(habitants_count-5), (255, 255, 255))
            screen.blit(deck_surface, (deck_x, deck_y))
            
            deck_x += 180
            
            for card in self.deck_habitants[:5]:
                deck_surface = pygame.Surface((150, 209))
                deck_surface.blit(self.textures["habitants"][card.texture], (0, 0))
                deck_surface.blit(self.textures["decorations"][card.id_lieu], (0, 0))
                pygame.draw.rect(deck_surface, (255,255,0) if self.mouse_in_card(deck_x, deck_y, 150, 209) else (255, 255, 255), (0, 0, 150, 209), 3, border_radius=10)
                count_rect = font.get_rect(str(card.points))
                font.render_to(deck_surface, (28 - count_rect.width//2, 20 - count_rect.height//2), str(card.points), (255, 255, 255))
                screen.blit(deck_surface, (deck_x, deck_y))
                deck_x += 219
            
            deck_x, deck_y = 180, 70
            for lieu in self.deck_lieux:
                deck_surface = pygame.Surface((209, 150))
                deck_surface.blit(self.textures["lieux"][lieu[1].texture], (0, 0))
                deck_surface.blit(self.textures["horizontal_decorations"][lieu[1].id_lieu], (0, 0))
                pygame.draw.rect(deck_surface, (255, 255, 255), (0, 0, 209, 150), 3, border_radius=10)
                count_rect = font.get_rect(str(lieu[1].points))
                font.render_to(deck_surface, (60 - count_rect.width//2, 132 - count_rect.height//2), str(lieu[1].points), (255, 255, 255))
                screen.blit(deck_surface, (deck_x, deck_y))
                deck_x += 219
            