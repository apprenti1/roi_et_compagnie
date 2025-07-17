import pygame
import pygame.freetype
from typing import List, Dict, Any, Tuple, Optional, Union, Callable
from enum import Enum
from ui.inputs import InputField, SubmitButton, Form, InputType, LabelPosition
from ui.background import Background

class Player:
    def __init__(self, name=""):
        self.name = name
        
    def __str__(self):
        return f"Joueur: {self.name}"

class Board:
    def __init__(self, screen=None):
        self.citizens = []
        self.players = []
        self.malus = []
        self.places = []
        self.screen = screen
        
        # État pour la gestion des formulaires
        self.setup_state = "ask_num_players"  # "ask_num_players" -> "ask_player_names" -> "done"
        self.num_players_form = None
        self.player_names_form = None
        self.num_players = 0
        
    def set_players(self, players):
        self.players = players
        
    def set_citizens(self, citizens):
        self.citizens = citizens
    
    def set_places(self, places):
        self.places = places
        
    def set_malus(self, malus):
        self.malus = malus
        
    def set_dices(self, dices):
        self.dices = dices
    
    def create_num_players_form(self):
        """Crée le formulaire pour demander le nombre de joueurs."""
        center_x = 640  # Centre de l'écran 1280x720
        center_y = 360
        
        field = InputField(
            name="num_players",
            input_type=InputType.INTEGER,
            x=self.screen.get_width() // 2 - 150, y=self.screen.get_height() // 2 - 25,  # Centré
            width=300, height=50,
            label_text="Nombre de joueurs (2-5)",
            label_position=LabelPosition.TOP,
            label_color=(255, 255, 255),
            placeholder="Entrez le nombre de joueurs",
            required=True,
            min_value=2,
            max_value=5,
            border_radius=8,
            font_size=18
        )
        
        button = SubmitButton(
            text="Valider",
            x=center_x - 60, y=center_y + 50,
            width=120, height=45,
            border_radius=8
        )
        
        def on_submit(data):
            self.num_players = data.get("num_players", 2)
            self.setup_state = "ask_player_names"
            self.create_player_names_form()
        
        self.num_players_form = Form(
            fields=[field],
            submit_button=button,
            on_submit=on_submit
        )
    
    def create_player_names_form(self):
        """Crée le formulaire pour demander les noms des joueurs."""
        fields = []
        start_x = 200
        start_y = 150
        field_spacing = 80  # Espacement entre les champs
        
        for i in range(self.num_players):
            field = InputField(
                name=f"player_{i}",
                input_type=InputType.TEXT,
                x=start_x, y=start_y + i * field_spacing,
                width=400, height=50,
                label_text=f"Nom du joueur {i + 1}",
                label_position=LabelPosition.TOP,
                placeholder=f"Joueur {i + 1}",
                required=True,
                max_length=20,
                border_radius=8,
                font_size=16
            )
            fields.append(field)
        
        button_y = start_y + self.num_players * field_spacing + 30
        button = SubmitButton(
            text="Créer les joueurs",
            x=start_x, y=button_y,
            width=180, height=50,
            border_radius=8
        )
        
        def on_submit(data):
            # Créer les joueurs avec les noms fournis
            players = []
            for i in range(self.num_players):
                name = data.get(f"player_{i}", f"Joueur {i + 1}")
                if not name or not name.strip():
                    name = f"Joueur {i + 1}"
                players.append(Player(name.strip()))
            
            self.set_players(players)
            self.setup_state = "done"
            print(f"Joueurs créés: {[str(player) for player in self.players]}")
        
        self.player_names_form = Form(
            fields=fields,
            submit_button=button,
            on_submit=on_submit
        )
    
    def handle_event(self, event):
        if self.setup_state == "ask_num_players":
            if not self.num_players_form:
                self.create_num_players_form()
            return self.num_players_form.handle_event(event)
        
        elif self.setup_state == "ask_player_names":
            if self.player_names_form:
                return self.player_names_form.handle_event(event)
        
        return False
    
    def update(self, dt):
        if self.setup_state == "ask_num_players" and self.num_players_form:
            self.num_players_form.update(dt)
        elif self.setup_state == "ask_player_names" and self.player_names_form:
            self.player_names_form.update(dt)
    
    def show(self, screen):
        """Affiche le board selon l'état actuel."""
        
        font_title = pygame.freetype.Font(None, 28)
        if self.setup_state == "ask_num_players":
            if self.num_players_form:
                title_text = f"Nombre de joueurs"
                title_rect = font_title.get_rect(title_text)
                font_title.render_to(screen, ((screen.get_width() - title_rect.width) // 2, 80), title_text, (255, 255, 255))
                self.create_num_players_form()
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
            # Affichage du plateau de jeu normal
            self.show_game_board(screen)
    
    def show_game_board(self, screen):
        """Affiche le plateau de jeu une fois les joueurs configurés."""
        font = pygame.freetype.Font(None, 24)
        font.render_to(screen, (50, 50), "Joueurs:", (255, 255, 255))
        
        # Afficher la liste des joueurs
        y = 100
        font_players = pygame.freetype.Font(None, 18)
        for i, player in enumerate(self.players):
            font_players.render_to(screen, (70, y), f"{i + 1}. {player.name}", (200, 200, 255))
            y += 25
            
        
    
    def reset_setup(self):
        """Remet à zéro la configuration."""
        self.players = []
        self.setup_state = "ask_num_players"
        self.num_players_form = None
        self.player_names_form = None
        self.num_players = 0