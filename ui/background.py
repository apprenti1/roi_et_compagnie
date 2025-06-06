import pygame
import config

class Background:


    def update(screen):
        background_image = pygame.image.load('assets/images/backgrounds/'+config.background_image+'.png')
        scale_factor = screen.get_width()/background_image.get_width() if background_image.get_width()/background_image.get_height()<screen.get_width()/screen.get_height() else screen.get_height()/background_image.get_height()
        background_image = pygame.transform.scale(background_image, (int(background_image.get_width()*scale_factor), int(background_image.get_height()*scale_factor)))
        
        screen.blit(background_image, ((screen.get_width()-background_image.get_width())//2, (screen.get_height()-background_image.get_height())//2))
