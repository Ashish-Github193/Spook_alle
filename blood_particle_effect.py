import pygame, random, math
class Blood_effect:
    def __init__(self,position):

        self.image = pygame.Surface((5, 5))
        self.image.fill((0,0,0))
        self.speed = 2
        self.gravity = 0.6
        self.rect = self.image.get_rect(topleft = position)

    def move (self):
        self.speed += self.gravity
        self.rect.y += self.speed

    def update(self, x_shift):
        self.move()
        self.rect.x += x_shift
