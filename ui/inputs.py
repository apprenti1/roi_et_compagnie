import pygame
import pygame.freetype
from typing import List, Dict, Any, Tuple, Optional, Union, Callable
from enum import Enum
import re

class LabelPosition(Enum):
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    INSIDE = "inside"

class InputType(Enum):
    TEXT = "text"
    INTEGER = "int"
    FLOAT = "float"
    PASSWORD = "password"

class CheckboxStyle(Enum):
    SQUARE = "square"
    CIRCLE = "circle"

class InputField:
    def __init__(self, 
                 name: str,
                 input_type: InputType = InputType.TEXT,
                 x: int = 0, 
                 y: int = 0,
                 width: int = 200,
                 height: int = 40,
                 bg_color: Tuple[int, int, int] = (255, 255, 255),
                 text_color: Tuple[int, int, int] = (0, 0, 0),
                 border_color: Tuple[int, int, int] = (100, 100, 100),
                 border_width: int = 2,
                 border_radius: int = 5,
                 font_size: int = 16,
                 font_name: Optional[str] = None,
                 placeholder: str = "",
                 max_length: Optional[int] = None,
                 min_value: Optional[Union[int, float]] = None,
                 max_value: Optional[Union[int, float]] = None,
                 required: bool = False,
                 active_border_color: Tuple[int, int, int] = (0, 120, 215),
                 error_border_color: Tuple[int, int, int] = (255, 0, 0),
                 label_text: str = "",
                 label_position: LabelPosition = LabelPosition.TOP,
                 label_color: Tuple[int, int, int] = (0, 0, 0),
                 label_font_size: int = 14,
                 label_margin: int = 5):
        
        self.name = name
        self.input_type = input_type
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.font_size = font_size
        self.font_name = font_name
        self.placeholder = placeholder
        self.max_length = max_length
        self.min_value = min_value
        self.max_value = max_value
        self.required = required
        self.active_border_color = active_border_color
        self.error_border_color = error_border_color
        self.label_text = label_text
        self.label_position = label_position
        self.label_color = label_color
        self.label_font_size = label_font_size
        self.label_margin = label_margin
        
        # État interne
        self.text = ""
        self.is_active = False
        self.is_focused = False
        self.has_error = False
        self.error_message = ""
        self.cursor_pos = 0
        self.cursor_visible = True
        self.cursor_timer = 0
        
        # Initialisation des fonts
        try:
            self.font = pygame.freetype.Font(font_name, font_size)
            self.label_font = pygame.freetype.Font(font_name, label_font_size)
        except:
            self.font = pygame.freetype.Font(None, font_size)
            self.label_font = pygame.freetype.Font(None, label_font_size)
        
        # Rectangle de collision
        self.rect = pygame.Rect(x, y, width, height)
    
    def handle_event(self, event: pygame.event.Event) -> str:
        """Gère les événements pour ce champ. Retourne 'consumed', 'tab_next', 'enter', ou 'none'."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                self.is_focused = self.rect.collidepoint(event.pos)
                return 'consumed' if self.is_focused else 'none'
        
        elif event.type == pygame.KEYDOWN and self.is_focused:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
                    self.has_error = False
                return 'consumed'
            elif event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
                    self.has_error = False
                return 'consumed'
            elif event.key == pygame.K_LEFT:
                self.cursor_pos = max(0, self.cursor_pos - 1)
                return 'consumed'
            elif event.key == pygame.K_RIGHT:
                self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
                return 'consumed'
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
                return 'consumed'
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
                return 'consumed'
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return 'enter'  # Laisse le formulaire gérer l'entrée
            elif event.key == pygame.K_TAB:
                return 'tab_next'  # Signal pour passer au champ suivant
            else:
                # Ajout de caractère
                if event.unicode and len(event.unicode) == 1:
                    char = event.unicode
                    if self._is_valid_char(char):
                        if self.max_length is None or len(self.text) < self.max_length:
                            self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                            self.cursor_pos += 1
                            self.has_error = False
                return 'consumed'
        
        return 'none'
    
    def _is_valid_char(self, char: str) -> bool:
        """Vérifie si le caractère est valide pour ce type de champ."""
        if self.input_type == InputType.TEXT or self.input_type == InputType.PASSWORD:
            return True
        elif self.input_type == InputType.INTEGER:
            return char.isdigit() or (char == '-' and self.cursor_pos == 0 and '-' not in self.text)
        elif self.input_type == InputType.FLOAT:
            return (char.isdigit() or 
                   (char == '-' and self.cursor_pos == 0 and '-' not in self.text) or
                   (char == '.' and '.' not in self.text))
        return False
    
    def validate(self) -> bool:
        """Valide le contenu du champ."""
        self.has_error = False
        self.error_message = ""
        
        # Vérification champ requis
        if self.required and not self.text.strip():
            self.has_error = True
            self.error_message = "Ce champ est requis"
            return False
        
        if not self.text.strip():
            return True  # Champ vide mais non requis
        
        # Validation par type
        try:
            if self.input_type == InputType.INTEGER:
                value = int(self.text)
                if self.min_value is not None and value < self.min_value:
                    self.has_error = True
                    self.error_message = f"Valeur minimum: {self.min_value}"
                    return False
                if self.max_value is not None and value > self.max_value:
                    self.has_error = True
                    self.error_message = f"Valeur maximum: {self.max_value}"
                    return False
            
            elif self.input_type == InputType.FLOAT:
                value = float(self.text)
                if self.min_value is not None and value < self.min_value:
                    self.has_error = True
                    self.error_message = f"Valeur minimum: {self.min_value}"
                    return False
                if self.max_value is not None and value > self.max_value:
                    self.has_error = True
                    self.error_message = f"Valeur maximum: {self.max_value}"
                    return False
        
        except ValueError:
            self.has_error = True
            if self.input_type == InputType.INTEGER:
                self.error_message = "Nombre entier requis"
            elif self.input_type == InputType.FLOAT:
                self.error_message = "Nombre décimal requis"
            return False
        
        return True
    
    def get_value(self) -> Union[str, int, float, None]:
        """Retourne la valeur typée du champ."""
        if not self.text.strip():
            return None
        
        try:
            if self.input_type == InputType.INTEGER:
                return int(self.text)
            elif self.input_type == InputType.FLOAT:
                return float(self.text)
            else:
                return self.text
        except ValueError:
            return None
    
    def set_focus(self, focused: bool):
        """Définit le focus du champ."""
        self.is_focused = focused
        if focused:
            self.cursor_visible = True
            self.cursor_timer = 0
    
    def update(self, dt: float):
        """Met à jour le curseur clignotant."""
        if self.is_focused:
            self.cursor_timer += dt
            if self.cursor_timer >= 500:  # 500ms
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
        else:
            self.cursor_visible = True
    
    def draw(self, screen: pygame.Surface):
        """Dessine le champ de saisie."""
        # Dessiner le label
        if self.label_text:
            self._draw_label(screen)
        
        # Couleur de bordure
        current_border_color = self.border_color
        if self.has_error:
            current_border_color = self.error_border_color
        elif self.is_focused:
            current_border_color = self.active_border_color
        
        # Dessiner le fond avec bordure arrondie
        if self.border_radius > 0:
            # Bordure
            pygame.draw.rect(screen, current_border_color, self.rect, border_radius=self.border_radius)
            # Fond
            inner_rect = pygame.Rect(
                self.rect.x + self.border_width,
                self.rect.y + self.border_width,
                self.rect.width - 2 * self.border_width,
                self.rect.height - 2 * self.border_width
            )
            pygame.draw.rect(screen, self.bg_color, inner_rect, border_radius=max(0, self.border_radius - self.border_width))
        else:
            pygame.draw.rect(screen, current_border_color, self.rect)
            pygame.draw.rect(screen, self.bg_color, 
                           (self.rect.x + self.border_width, self.rect.y + self.border_width,
                            self.rect.width - 2 * self.border_width, self.rect.height - 2 * self.border_width))
        
        # Texte à afficher
        display_text = self.text
        if self.input_type == InputType.PASSWORD:
            display_text = '*' * len(self.text)
        elif not self.text and self.placeholder:
            display_text = self.placeholder
        
        # Position du texte
        text_x = self.rect.x + self.border_width + 5
        text_y = self.rect.y + (self.rect.height - self.font_size) // 2
        
        # Dessiner le texte
        if display_text:
            text_color = self.text_color if self.text else (150, 150, 150)
            self.font.render_to(screen, (text_x, text_y), display_text, text_color)
        
        # Dessiner le curseur
        if self.is_focused and self.cursor_visible:
            cursor_text = display_text[:self.cursor_pos] if display_text else ""
            cursor_width = self.font.get_rect(cursor_text).width if cursor_text else 0
            cursor_x = text_x + cursor_width
            cursor_y = text_y
            pygame.draw.line(screen, self.text_color, 
                           (cursor_x, cursor_y), (cursor_x, cursor_y + self.font_size), 1)
        
        # Dessiner le message d'erreur
        if self.has_error and self.error_message:
            error_y = self.rect.bottom + 2
            self.label_font.render_to(screen, (self.rect.x, error_y), self.error_message, self.error_border_color)
    
    def _draw_label(self, screen: pygame.Surface):
        """Dessine le label selon sa position."""
        if not self.label_text:
            return
        
        label_rect = self.label_font.get_rect(self.label_text)
        
        if self.label_position == LabelPosition.TOP:
            label_x = self.rect.x
            label_y = self.rect.y - label_rect.height - self.label_margin
        elif self.label_position == LabelPosition.BOTTOM:
            label_x = self.rect.x
            label_y = self.rect.bottom + self.label_margin
        elif self.label_position == LabelPosition.LEFT:
            label_x = self.rect.x - label_rect.width - self.label_margin
            label_y = self.rect.y + (self.rect.height - label_rect.height) // 2
        elif self.label_position == LabelPosition.RIGHT:
            label_x = self.rect.right + self.label_margin
            label_y = self.rect.y + (self.rect.height - label_rect.height) // 2
        elif self.label_position == LabelPosition.INSIDE:
            label_x = self.rect.x + self.border_width + 5
            label_y = self.rect.y + 2
        
        self.label_font.render_to(screen, (label_x, label_y), self.label_text, self.label_color)


class CheckboxField:
    def __init__(self,
                 name: str,
                 x: int = 0,
                 y: int = 0,
                 size: int = 20,
                 checked: bool = False,
                 bg_color: Tuple[int, int, int] = (255, 255, 255),
                 border_color: Tuple[int, int, int] = (100, 100, 100),
                 check_color: Tuple[int, int, int] = (0, 120, 215),
                 hover_color: Tuple[int, int, int] = (230, 230, 230),
                 border_width: int = 2,
                 style: CheckboxStyle = CheckboxStyle.SQUARE,
                 label_text: str = "",
                 label_position: LabelPosition = LabelPosition.RIGHT,
                 label_color: Tuple[int, int, int] = (0, 0, 0),
                 label_font_size: int = 14,
                 label_margin: int = 8,
                 font_name: Optional[str] = None):
        
        self.name = name
        self.x = x
        self.y = y
        self.size = size
        self.checked = checked
        self.bg_color = bg_color
        self.border_color = border_color
        self.check_color = check_color
        self.hover_color = hover_color
        self.border_width = border_width
        self.style = style
        self.label_text = label_text
        self.label_position = label_position
        self.label_color = label_color
        self.label_font_size = label_font_size
        self.label_margin = label_margin
        
        # État interne
        self.is_hovered = False
        self.is_focused = False
        
        # Initialisation de la font pour le label
        try:
            self.label_font = pygame.freetype.Font(font_name, label_font_size)
        except:
            self.label_font = pygame.freetype.Font(None, label_font_size)
        
        # Rectangle de collision (inclut le label si cliquable)
        self._update_rects()
    
    def _update_rects(self):
        """Met à jour les rectangles de collision."""
        self.checkbox_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
        # Rectangle total incluant le label si présent
        if self.label_text:
            label_rect = self.label_font.get_rect(self.label_text)
            if self.label_position == LabelPosition.RIGHT:
                total_width = self.size + self.label_margin + label_rect.width
                total_height = max(self.size, label_rect.height)
                self.total_rect = pygame.Rect(self.x, self.y, total_width, total_height)
            elif self.label_position == LabelPosition.LEFT:
                total_width = label_rect.width + self.label_margin + self.size
                total_height = max(self.size, label_rect.height)
                self.total_rect = pygame.Rect(self.x - label_rect.width - self.label_margin, 
                                            self.y, total_width, total_height)
            elif self.label_position == LabelPosition.TOP:
                total_width = max(self.size, label_rect.width)
                total_height = self.size + self.label_margin + label_rect.height
                self.total_rect = pygame.Rect(self.x, self.y - label_rect.height - self.label_margin,
                                            total_width, total_height)
            elif self.label_position == LabelPosition.BOTTOM:
                total_width = max(self.size, label_rect.width)
                total_height = self.size + self.label_margin + label_rect.height
                self.total_rect = pygame.Rect(self.x, self.y, total_width, total_height)
            else:
                self.total_rect = self.checkbox_rect
        else:
            self.total_rect = self.checkbox_rect
    
    def handle_event(self, event: pygame.event.Event) -> str:
        """Gère les événements pour cette checkbox. Retourne 'consumed', 'tab_next', ou 'none'."""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.total_rect.collidepoint(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.total_rect.collidepoint(event.pos):
                self.is_focused = True
                self.checked = not self.checked
                return 'consumed'
        
        elif event.type == pygame.KEYDOWN and self.is_focused:
            if event.key == pygame.K_SPACE:
                self.checked = not self.checked
                return 'consumed'
            elif event.key == pygame.K_TAB:
                return 'tab_next'
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return 'enter'
        
        return 'none'
    
    def set_focus(self, focused: bool):
        """Définit le focus de la checkbox."""
        self.is_focused = focused
    
    def get_value(self) -> bool:
        """Retourne la valeur de la checkbox."""
        return self.checked
    
    def validate(self) -> bool:
        """Valide la checkbox (toujours True pour une checkbox simple)."""
        return True
    
    def update(self, dt: float):
        """Met à jour la checkbox (pas d'animation pour l'instant)."""
        pass
    
    def draw(self, screen: pygame.Surface):
        """Dessine la checkbox."""
        # Dessiner le label
        if self.label_text:
            self._draw_label(screen)
        
        # Couleur de fond selon l'état
        current_bg_color = self.hover_color if self.is_hovered else self.bg_color
        border_color = self.check_color if self.is_focused else self.border_color
        
        # Dessiner la checkbox selon le style
        if self.style == CheckboxStyle.SQUARE:
            # Fond
            pygame.draw.rect(screen, current_bg_color, self.checkbox_rect)
            # Bordure
            pygame.draw.rect(screen, border_color, self.checkbox_rect, self.border_width)
            
            # Coche si cochée
            if self.checked:
                # Dessiner une coche
                check_points = [
                    (self.checkbox_rect.x + self.size * 0.2, self.checkbox_rect.y + self.size * 0.5),
                    (self.checkbox_rect.x + self.size * 0.4, self.checkbox_rect.y + self.size * 0.7),
                    (self.checkbox_rect.x + self.size * 0.8, self.checkbox_rect.y + self.size * 0.3)
                ]
                pygame.draw.lines(screen, self.check_color, False, check_points, 3)
        
        elif self.style == CheckboxStyle.CIRCLE:
            center = self.checkbox_rect.center
            radius = self.size // 2
            
            # Fond
            pygame.draw.circle(screen, current_bg_color, center, radius)
            # Bordure
            pygame.draw.circle(screen, border_color, center, radius, self.border_width)
            
            # Point si cochée
            if self.checked:
                inner_radius = max(2, radius - 6)
                pygame.draw.circle(screen, self.check_color, center, inner_radius)
        
        # Indicateur de focus
        if self.is_focused:
            focus_rect = pygame.Rect(self.checkbox_rect.x - 2, self.checkbox_rect.y - 2,
                                   self.checkbox_rect.width + 4, self.checkbox_rect.height + 4)
            pygame.draw.rect(screen, self.check_color, focus_rect, 1)
    
    def _draw_label(self, screen: pygame.Surface):
        """Dessine le label selon sa position."""
        if not self.label_text:
            return
        
        label_rect = self.label_font.get_rect(self.label_text)
        
        if self.label_position == LabelPosition.RIGHT:
            label_x = self.checkbox_rect.right + self.label_margin
            label_y = self.checkbox_rect.y + (self.checkbox_rect.height - label_rect.height) // 2
        elif self.label_position == LabelPosition.LEFT:
            label_x = self.checkbox_rect.x - label_rect.width - self.label_margin
            label_y = self.checkbox_rect.y + (self.checkbox_rect.height - label_rect.height) // 2
        elif self.label_position == LabelPosition.TOP:
            label_x = self.checkbox_rect.x + (self.checkbox_rect.width - label_rect.width) // 2
            label_y = self.checkbox_rect.y - label_rect.height - self.label_margin
        elif self.label_position == LabelPosition.BOTTOM:
            label_x = self.checkbox_rect.x + (self.checkbox_rect.width - label_rect.width) // 2
            label_y = self.checkbox_rect.bottom + self.label_margin
        else:
            return
        
        self.label_font.render_to(screen, (label_x, label_y), self.label_text, self.label_color)


class SubmitButton:
    def __init__(self,
                 text: str = "Valider",
                 x: int = 0,
                 y: int = 0,
                 width: int = 100,
                 height: int = 40,
                 bg_color: Tuple[int, int, int] = (0, 120, 215),
                 text_color: Tuple[int, int, int] = (255, 255, 255),
                 border_color: Tuple[int, int, int] = (0, 120, 215),
                 border_width: int = 0,
                 border_radius: int = 5,
                 font_size: int = 16,
                 font_name: Optional[str] = None,
                 hover_bg_color: Optional[Tuple[int, int, int]] = None,
                 hover_text_color: Optional[Tuple[int, int, int]] = None,
                 disabled_bg_color: Tuple[int, int, int] = (150, 150, 150),
                 disabled_text_color: Tuple[int, int, int] = (200, 200, 200)):
        
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.font_size = font_size
        self.font_name = font_name
        self.hover_bg_color = hover_bg_color or tuple(max(0, c - 30) for c in bg_color)
        self.hover_text_color = hover_text_color or text_color
        self.disabled_bg_color = disabled_bg_color
        self.disabled_text_color = disabled_text_color
        
        self.is_hovered = False
        self.is_pressed = False
        self.is_enabled = True
        
        # Initialisation de la font
        try:
            self.font = pygame.freetype.Font(font_name, font_size)
        except:
            self.font = pygame.freetype.Font(None, font_size)
        
        self.rect = pygame.Rect(x, y, width, height)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Gère les événements pour le bouton. Retourne True si cliqué."""
        if not self.is_enabled:
            return False
        
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed and self.rect.collidepoint(event.pos):
                self.is_pressed = False
                return True
            self.is_pressed = False
        
        return False
    
    def draw(self, screen: pygame.Surface):
        """Dessine le bouton."""
        # Couleurs selon l'état
        if not self.is_enabled:
            bg_color = self.disabled_bg_color
            text_color = self.disabled_text_color
        elif self.is_pressed:
            bg_color = tuple(max(0, c - 50) for c in self.bg_color)
            text_color = self.text_color
        elif self.is_hovered:
            bg_color = self.hover_bg_color
            text_color = self.hover_text_color
        else:
            bg_color = self.bg_color
            text_color = self.text_color
        
        # Dessiner le fond avec bordure
        if self.border_radius > 0:
            if self.border_width > 0:
                pygame.draw.rect(screen, self.border_color, self.rect, border_radius=self.border_radius)
                inner_rect = pygame.Rect(
                    self.rect.x + self.border_width,
                    self.rect.y + self.border_width,
                    self.rect.width - 2 * self.border_width,
                    self.rect.height - 2 * self.border_width
                )
                pygame.draw.rect(screen, bg_color, inner_rect, border_radius=max(0, self.border_radius - self.border_width))
            else:
                pygame.draw.rect(screen, bg_color, self.rect, border_radius=self.border_radius)
        else:
            if self.border_width > 0:
                pygame.draw.rect(screen, self.border_color, self.rect)
                pygame.draw.rect(screen, bg_color, 
                               (self.rect.x + self.border_width, self.rect.y + self.border_width,
                                self.rect.width - 2 * self.border_width, self.rect.height - 2 * self.border_width))
            else:
                pygame.draw.rect(screen, bg_color, self.rect)
        
        # Centrer le texte
        text_rect = self.font.get_rect(self.text)
        text_x = self.rect.x + (self.rect.width - text_rect.width) // 2
        text_y = self.rect.y + (self.rect.height - text_rect.height) // 2
        
        self.font.render_to(screen, (text_x, text_y), self.text, text_color)


class Form:
    def __init__(self,
                 fields: List[Union[InputField, CheckboxField]],
                 submit_button: SubmitButton,
                 on_submit: Optional[Callable[[Dict[str, Any]], None]] = None,
                 validate_on_submit: bool = True):
        
        self.fields = fields
        self.submit_button = submit_button
        self.on_submit = on_submit
        self.validate_on_submit = validate_on_submit
        
        # État du formulaire
        self.is_submitted = False
        self.last_submit_data = {}
        self.focused_field_index = -1  # Index du champ actuellement focus
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Gère les événements pour tout le formulaire."""
        # Gestion des champs avec navigation Tab
        for i, field in enumerate(self.fields):
            result = field.handle_event(event)
            
            if result == 'consumed':
                # Mettre à jour l'index du champ focus
                if field.is_focused:
                    self.focused_field_index = i
                return True
            elif result == 'tab_next':
                # Passer au champ suivant
                self._focus_next_field()
                return True
            elif result == 'enter':
                # Soumettre le formulaire
                self.submit()
                return True
        
        # Gestion du clic sur le bouton submit
        if self.submit_button.handle_event(event):
            self.submit()
            return True
        
        # Gestion globale de Tab (si aucun champ n'était focus)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self._focus_next_field()
            return True
        
        # Gestion de Entrée globale
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.submit()
            return True
        
        return False
    
    def _focus_next_field(self):
        """Passe le focus au champ suivant."""
        if not self.fields:
            return
        
        # Retirer le focus du champ actuel
        if 0 <= self.focused_field_index < len(self.fields):
            self.fields[self.focused_field_index].set_focus(False)
        
        # Passer au champ suivant (avec boucle)
        self.focused_field_index = (self.focused_field_index + 1) % len(self.fields)
        
        # Donner le focus au nouveau champ
        self.fields[self.focused_field_index].set_focus(True)
    
    def _focus_previous_field(self):
        """Passe le focus au champ précédent."""
        if not self.fields:
            return
        
        # Retirer le focus du champ actuel
        if 0 <= self.focused_field_index < len(self.fields):
            self.fields[self.focused_field_index].set_focus(False)
        
        # Passer au champ précédent (avec boucle)
        self.focused_field_index = (self.focused_field_index - 1) % len(self.fields)
        
        # Donner le focus au nouveau champ
        self.fields[self.focused_field_index].set_focus(True)
    
    def focus_first_field(self):
        """Met le focus sur le premier champ."""
        if self.fields:
            # Retirer le focus de tous les champs
            for field in self.fields:
                field.set_focus(False)
            
            # Focus sur le premier
            self.focused_field_index = 0
            self.fields[0].set_focus(True)
    
    def submit(self) -> Dict[str, Any]:
        """Soumet le formulaire et retourne les données."""
        if self.validate_on_submit:
            # Valider tous les champs
            all_valid = True
            for field in self.fields:
                if not field.validate():
                    all_valid = False
            
            if not all_valid:
                return {}
        
        # Collecter les données
        data = {}
        for field in self.fields:
            data[field.name] = field.get_value()
        
        self.last_submit_data = data
        self.is_submitted = True
        
        # Appeler le callback
        if self.on_submit:
            self.on_submit(data)
        
        return data
    
    def reset(self):
        """Remet à zéro le formulaire."""
        for field in self.fields:
            field.text = ""
            field.cursor_pos = 0
            field.has_error = False
            field.error_message = ""
            field.set_focus(False)
        
        self.is_submitted = False
        self.last_submit_data = {}
        self.focused_field_index = -1
    
    def update(self, dt: float):
        """Met à jour le formulaire."""
        for field in self.fields:
            field.update(dt)
    
    def draw(self, screen: pygame.Surface):
        """Dessine le formulaire."""
        for field in self.fields:
            field.draw(screen)
        
        self.submit_button.draw(screen)
    
    def get_field_by_name(self, name: str) -> Optional[Union[InputField, CheckboxField]]:
        """Retourne un champ par son nom."""
        for field in self.fields:
            if field.name == name:
                return field
        return None


# Exemple d'utilisation
def create_example_form():
    """Crée un exemple de formulaire."""
    
    # Création des champs
    fields = [
        InputField(
            name="nom",
            input_type=InputType.TEXT,
            x=50, y=100,
            width=300, height=40,
            label_text="Nom complet",
            label_position=LabelPosition.TOP,
            placeholder="Entrez votre nom",
            required=True,
            border_radius=8
        ),
        
        InputField(
            name="age",
            input_type=InputType.INTEGER,
            x=50, y=180,
            width=150, height=40,
            label_text="Âge",
            label_position=LabelPosition.TOP,
            min_value=0,
            max_value=120,
            border_radius=8
        ),
        
        InputField(
            name="email",
            input_type=InputType.TEXT,
            x=220, y=180,
            width=200, height=40,
            label_text="Email",
            label_position=LabelPosition.TOP,
            placeholder="exemple@email.com",
            border_radius=8
        ),
        
        InputField(
            name="salaire",
            input_type=InputType.FLOAT,
            x=50, y=260,
            width=200, height=40,
            label_text="Salaire (€)",
            label_position=LabelPosition.TOP,
            min_value=0.0,
            border_radius=8
        ),
        
        # Ajout de checkboxes
        CheckboxField(
            name="newsletter",
            x=50, y=320,
            size=20,
            label_text="S'abonner à la newsletter",
            label_position=LabelPosition.RIGHT,
            style=CheckboxStyle.SQUARE
        ),
        
        CheckboxField(
            name="conditions",
            x=50, y=350,
            size=20,
            checked=False,
            label_text="J'accepte les conditions d'utilisation",
            label_position=LabelPosition.RIGHT,
            style=CheckboxStyle.SQUARE,
            check_color=(34, 139, 34)
        ),
        
        CheckboxField(
            name="notifications",
            x=50, y=380,
            size=18,
            label_text="Recevoir des notifications",
            label_position=LabelPosition.RIGHT,
            style=CheckboxStyle.CIRCLE,
            check_color=(255, 140, 0)
        )
    ]
    
    # Création du bouton de soumission
    submit_button = SubmitButton(
        text="Envoyer",
        x=50, y=420,
        width=120, height=45,
        bg_color=(34, 139, 34),
        border_radius=8,
        font_size=18
    )
    
    # Callback de soumission
    def on_submit_callback(data):
        print("Formulaire soumis avec les données:")
        for key, value in data.items():
            print(f"  {key}: {value}")
    
    # Création du formulaire
    form = Form(
        fields=fields,
        submit_button=submit_button,
        on_submit=on_submit_callback
    )
    
    return form


def main():
    """Exemple d'utilisation du package."""
    pygame.init()
    pygame.freetype.init()
    
    screen = pygame.display.set_mode((500, 500))    
    pygame.display.set_caption("Exemple de Formulaire avec Navigation Tab et Checkboxes")
    clock = pygame.time.Clock()
    
    # Créer le formulaire
    form = create_example_form()
    
    # Mettre le focus sur le premier champ au démarrage
    form.focus_first_field()
    
    running = True
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                form.handle_event(event)
        
        # Mettre à jour
        form.update(dt)
        
        # Dessiner
        screen.fill((240, 240, 240))
        form.draw(screen)
        
        # Afficher les données soumises
        if form.is_submitted:
            y = 10
            font = pygame.freetype.Font(None, 16)
            font.render_to(screen, (10, y), "Dernières données soumises:", (0, 0, 0))
            y += 20
            for key, value in form.last_submit_data.items():
                font.render_to(screen, (10, y), f"{key}: {value}", (0, 0, 0))
                y += 18
        
        # Afficher les instructions
        font = pygame.freetype.Font(None, 14)
        instructions = [
            "Instructions:",
            "- Tab: Champ suivant",
            "- Espace: Cocher/décocher (checkbox)",
            "- Entrée: Soumettre",
            "- Clic: Sélectionner champ/checkbox"
        ]
        y = screen.get_height() - len(instructions) * 16 - 10
        for instruction in instructions:
            font.render_to(screen, (10, y), instruction, (100, 100, 100))
            y += 16
        
        pygame.display.flip()
    
    pygame.quit()


if __name__ == "__main__":
    main()