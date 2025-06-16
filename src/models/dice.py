import pygame
import time
import config
from enum import Enum
from random import choice

class Color(Enum):
    RED = config.dice().red
    GREEN = config.dice().green
    BLUE = config.dice().blue

class Number(Enum):
    ONE = config.dice().char_numbers[0]
    TWO = config.dice().char_numbers[1]
    THREE = config.dice().char_numbers[2]
    FOUR = config.dice().char_numbers[3]
    FIVE = config.dice().char_numbers[4]
    SIX = config.dice().char_numbers[5]

class Dice:
    def __init__(self, screen=None, index=0):
        self.rect = pygame.Rect(
            config.dice().global_margin_left + (index%3)*(config.dice().size + config.dice().inside_margin),
            screen.get_height() - config.dice().size - (config.dice().size + config.dice().inside_margin)*(index//3) - (config.dice().global_margin_bottom + config.dice().inside_margin + config.dice().size),
            config.dice().size, config.dice().size
        )
        self.selected = True
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.font = pygame.font.Font(config.dice().text_font, config.dice().text_size)
        self.text = None
        self.color = choice(list(Color))
        self.number = choice(list(Number))
        self.set_color(self.color)
        self.set_number(self.number)
        # self.shake(screen)
            
    def shake(self, screen=None):
        self.set_color(choice(list(Color)))
        self.set_number(choice(list(Number)))
        self.show(screen)
        pygame.display.update(self.rect)
        
        
        
    def select(self, screen):
        # t1 = time.time()
        self.selected = not self.selected
        self.show(screen)
        pygame.display.update(self.rect)
        # print("select duration:", time.time() - t1)
        
    def set_color(self, color):
        self.color = color
        pygame.draw.rect(self.surface, color.value, ( 4, 4, self.surface.get_width()-8, self.surface.get_height()-8), border_radius=config.dice().border_radius)
        
    def set_number(self, number):
        self.number = number
        self.text = self.font.render(str(number.value), True, config.dice().text_color)
        
    def show(self, screen):
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, self.color.value, (4, 4, self.surface.get_width()-8, self.surface.get_height()-8), border_radius=config.dice().border_radius)
        if self.selected:
            pygame.draw.rect(self.surface, (255, 255, 255), self.surface.get_rect(), 2, border_radius=config.dice().border_radius)
        else:
            pygame.draw.rect(self.surface, (10, 10, 10), self.surface.get_rect(), 3, border_radius=config.dice().border_radius)
        self.surface.blit(self.text, (self.surface.get_width()/2-self.text.get_width()/2, self.surface.get_height()/2-self.text.get_height()/2))
        screen.blit(self.surface, (self.rect.x, self.rect.y))
    
    
class Dices:
    def __init__(self, screen=None, shake_duration=config.dice().shake_duration):
        self.dices = [Dice(screen, i) for i in range(6)]
        self.rect = pygame.Rect(
            config.dice().global_margin_left,
            screen.get_height() - config.dice().size  - config.dice().global_margin_bottom,
            config.dice().size*3+config.dice().inside_margin*2, config.dice().size
        )
        self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.font = pygame.font.Font(config.dice().shake_text_font, config.dice().shake_text_size)
        self.text = self.font.render("Shake({})".format(shake_duration), True, config.dice().text_color)
        
    
    def shake(self, screen=None, shake_duration=config.dice().shake_duration):
        self.text = self.font.render("Shake({})".format(shake_duration), True, config.dice().text_color)
        screen.blit(self.surface, (self.rect.x, self.rect.y))
        pygame.display.update(self.rect)
        # print("shaked")
        for dice in self.dices:
            dice.shake(screen) if dice.selected else None
    
    
    def show(self, screen):
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, config.dice().shake_button_color, ( 4, 4, self.surface.get_width()-8, self.surface.get_height()-8), border_radius=config.dice().border_radius)
        self.surface.blit(self.text, (self.surface.get_width()/2-self.text.get_width()/2, self.surface.get_height()/2-self.text.get_height()/2))
        for dice in self.dices:
            dice.show(screen)
        screen.blit(self.surface, (self.rect.x, self.rect.y))
        pygame.display.update(self.rect)

    def event(self, event, screen):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for i, dice in enumerate(self.dices):
                if dice.rect.collidepoint(mouse_pos):
                    dice.select(screen)
            if self.rect.collidepoint(mouse_pos):
                self.shake(screen)
                
