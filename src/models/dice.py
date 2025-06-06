import pygame
from enum import Enum
from random import choice


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Number(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6


class Dice:
    def shake(self):
        return choice(list(Color)), choice(list(Number))
    
    
class Dices:
    def __init__(self):
        self.dices = [Dice() for i in range(6)]
    
    def shake(self):
        return [dice.shake() for dice in self.dices]
    
    
    def show(self, screen):
        for i, dice in enumerate(self.dices):
            color, number = dice.shake()
            surface = pygame.Surface((50, 50))
            surface.fill(color.value)
            font = pygame.font.Font(None, 36)
            text = font.render(str(number.value), True, (255, 255, 255))
            surface.blit(text, (25-text.get_width()/2, 25-text.get_height()/2))
            screen.blit(surface, (10+i*60, 10))
