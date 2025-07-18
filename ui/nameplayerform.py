from ui.inputs import InputField, SubmitButton, Form, InputType, LabelPosition
from src.models.player import Player
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
            label_color=(255, 255, 255),
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
        
        self.players = players
        self.setup_state = "done"
        print(f"Joueurs créés: {[str(player) for player in self.players]}")
    
    self.player_names_form = Form(
        fields=fields,
        submit_button=button,
        on_submit=on_submit
    )
