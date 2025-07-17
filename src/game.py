import pygame
import config
import ui
import src.models as models
import time

class Game:
    def __init__(self):
        pygame.init()
        pygame.freetype.init()
        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        ui.Background.splash(self.screen)
        self.dices = None
        pygame.display.flip()
        pygame.time.wait(config.base().splash_screen_duration)

    def run(self):
        self.dices = models.Dices(self.screen)
        self.board = models.Board(self.screen)
        running = True
        
        while running:
            dt = self.clock.tick(60)  # Limite à 60 FPS
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Transmettre TOUS les événements au board
                # Le board décidera s'il doit les traiter ou non
                board_handled = self.board.handle_event(event)
                
                # Si le board n'a pas traité l'événement, le traiter ici
                if not board_handled:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.dices.event(event, self.screen)
            
            # Mettre à jour les composants
            self.board.update(dt)  # Important pour les curseurs clignotants
            
            # Dessiner
            ui.Background.update(self.screen)
            self.board.show(self.screen)
            
            pygame.display.flip()
        
        pygame.quit()