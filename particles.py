import pygame, random, math

class Dynamic_leaves:
    def __init__(self,position):

        self.image = pygame.Surface((4,4))
        self.image.fill((0,0,0))
        self.life = 100
        self.speed = random.randint(1, 3)
        self.velocity = [0,0]
        self.velocity[0] = math.cos(math.radians(random.randint(220, 260))) * self.speed
        self.velocity[1] = self.speed
        self.rect = self.image.get_rect(topleft = [position[0]+random.randint(40, 128), position[1]+128])

    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def update(self, x_shift):
        self.move()
        self.rect.x += x_shift
        self.life -= 0.1