__author__ = 'Matej'

import pygame
import Utilities

class Dead(pygame.sprite.Sprite):

    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)

        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.image, self.rect = Utilities.load_image('dead.png')
        self.rect.move_ip(rect)

        self.active = False

