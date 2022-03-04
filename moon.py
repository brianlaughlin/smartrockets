import pygame

import constants


class Moon():
    def __init__(self):
        self.x = constants.MOON_X
        self.y = constants.MOON_Y
        self.image = pygame.image.load("assets/moon.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.width = self.rect.width
        self.height = self.rect.height

    def draw(self, WIN):
        WIN.blit(self.image, (self.x, self.y))
