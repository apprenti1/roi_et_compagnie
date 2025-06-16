import pygame
import config
import ui
import src.models as models
import time

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        ui.Background.splash(self.screen)
        self.dices = None
        pygame.display.flip()
        pygame.time.wait(config.base().splash_screen_duration)

    def run(self):
        self.dices = models.Dices(self.screen)
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.dices.event(event, self.screen)
                    
            ui.Background.update(self.screen)
            
            
            self.dices.show(self.screen)
            pygame.display.flip()
                    
            
            
        pygame.quit()
