import pygame
import config

class Background:


    def splash (screen):
        Background.update(screen)
        splash = pygame.image.load(config.base().splash_screen_image)
        splash = pygame.transform.scale(splash, (screen.get_height()*(splash.get_width()/splash.get_height()), screen.get_height()))
        screen.blit(splash, (screen.get_width() / 2 - splash.get_width() / 2, screen.get_height() / 2 - splash.get_height() / 2))
        
    def update(screen):
        background_image = pygame.image.load('assets/images/backgrounds/'+config.base().background_image)
        scale_factor = screen.get_width()/background_image.get_width() if background_image.get_width()/background_image.get_height()<screen.get_width()/screen.get_height() else screen.get_height()/background_image.get_height()
        background_image = pygame.transform.scale(background_image, (int(background_image.get_width()*scale_factor), int(background_image.get_height()*scale_factor)))
        
        screen.blit(background_image, ((screen.get_width()-background_image.get_width())//2, (screen.get_height()-background_image.get_height())//2))
