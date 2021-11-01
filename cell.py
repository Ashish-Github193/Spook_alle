import pygame, random

class Battery(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        self.image = pygame.image.load('assets/cell.png')
        self.rect = self.image.get_rect(topleft = [position[0] + random.randint(0, 55), position[1]+59])

    def update(self, x_shift):
        self.rect.x += x_shift