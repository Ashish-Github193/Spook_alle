import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, tile_size):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill('Black')
        self.rect = self.image.get_rect(topleft = position)

    def update(self, x_shift):
        self.rect.x += x_shift
