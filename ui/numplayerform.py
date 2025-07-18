from ui.inputs import InputField, SubmitButton, Form, InputType, LabelPosition
from ui.nameplayerform import create_player_names_form

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
        create_player_names_form(self)
    
    self.num_players_form = Form(
        fields=[field],
        submit_button=button,
        on_submit=on_submit
    )
