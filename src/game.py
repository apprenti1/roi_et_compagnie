import pygame
#from core.engine import Engine
#from ui.pygame_gui import UI

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        #self.engine = Engine()
        #self.ui = UI(self.screen, self.engine)

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                #self.ui.handle_event(event)

            #self.engine.update()
            #self.ui.render()

        pygame.quit()
