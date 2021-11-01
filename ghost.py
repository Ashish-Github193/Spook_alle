import pygame

class Ghost(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.arg = position
        self.direction = pygame.math.Vector2(0,0)
        self.image_right = []
        self.image_left = []
        self.image_left.append(pygame.image.load("assets/ghost_left.png"))
        self.image_left.append(pygame.image.load("assets/ghost_left_1.png"))
        self.image_right.append(pygame.image.load("assets/ghost_right.png"))
        self.image_right.append(pygame.image.load("assets/ghost_right_1.png"))
        self.image = self.image_right[0]
        self.rect = self.image.get_rect(topleft = [position[0], position[1]])
        
        self.direction.x = 1
        self.speed = 1
        self.animation_speed = 0.5
        self.index = 0
        self.gravity = 0

    def animate(self):
        if self.direction.x == 1:
            self.image = self.image_right[int(self.index/16)]
        else:
            self.image = self.image_left[int(self.index/16)]
    
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self, x_shift):
        self.index += self.animation_speed
        if self.index > 16:
            self.index = 0
        self.animate()
        self.rect.x += x_shift
        self.rect.x += self.direction.x * self.speed