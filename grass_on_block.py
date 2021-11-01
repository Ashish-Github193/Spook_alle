import pygame
grass = pygame.image.load('assets/grass.png')
grass_left = pygame.image.load('assets/left.png')
grass_right = pygame.image.load('assets/right.png')

class Grass(pygame.sprite.Sprite):
    def __init__(self, position, pos):
        super().__init__()
        if pos == 0:
            self.image = grass
            self.rect = self.image.get_rect(topleft = [position[0], position[1]+60])
        elif pos == -1:
            self.image = grass_left
            self.rect = self.image.get_rect(topleft = [position[0], position[1]+54])
        elif pos == 1:
            self.image = grass_right
            self.rect = self.image.get_rect(topleft = [position[0], position[1]+54])
        

    def update(self, x_shift):
        self.rect.x += x_shift