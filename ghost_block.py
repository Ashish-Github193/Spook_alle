import pygame, random
from blood_particle_effect import Blood_effect
ghost_b = pygame.image.load('assets/ghost_block.png')



class Ghost_block(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = ghost_b
        self.rect = self.image.get_rect(topleft = position)

    def update(self, x_shift):
        self.rect.x += x_shift

n_stage = []
for i in range(5):
    n_stage.append(pygame.image.load('assets/gate_gif/' + str(i) + '.png'))
class Next_stage(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = n_stage[0]
        self.rect = self.image.get_rect(topleft = [position[0]-192, position[1]-192])
        self.animation_index = 0
        self.animation_speed = 1
        
    def image_change(self):
        self.image = n_stage[int(self.animation_index/7)]

    def update(self, x_shift, status):
        if status == False:
            self.image = n_stage[4]
        else:
            self.image_change()
        self.animation_index += self.animation_speed
        if self.animation_index > 21:
            self.animation_index = 0
        self.rect.x += x_shift

from sounds import *
pygame.mixer.init()
decor = [pygame.image.load('assets/decor.png'), pygame.image.load('assets/decor_wc.png')]
class Decor(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = random.choice(decor)
        self.rect = self.image.get_rect(topleft = [position[0]-192, position[1]-192])
        self.blood_list = []
        self.blood_time = 50
    def blood_insert(self):
        if self.blood_time == 0:
            self.blood_list.append(Blood_effect((self.rect.x+64, self.rect.y+128)))
            self.blood_time = 100

    def update(self, x_shift, surface):

        if self.blood_time == 0: 
            self.blood_insert()
            self.blood_time = 100
            if self.rect.x <= 850 and self.rect.x > 100:
                pygame.mixer.Channel(5).play(pygame.mixer.Sound(blood_drip), 0)
        else:
            self.blood_time -= 1

        for blood in self.blood_list:
                if blood.rect.y > 704:
                    self.blood_list.remove(blood)
                else:
                    blood.update(x_shift)
                    surface.blit(blood.image, [blood.rect.x, blood.rect.y])

        self.rect.x += x_shift

grave = [pygame.image.load('assets/grave.png'), pygame.image.load('assets/grave_wc.png')]
class Grave(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = random.choice(grave)
        self.rect = self.image.get_rect(topleft = [position[0], position[1]+12])

    def update(self, x_shift):
        self.rect.x += x_shift

scarecrow = pygame.image.load('assets/scarecrow.png')
class Scarecrow(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = scarecrow
        self.rect = self.image.get_rect(topleft = [position[0], position[1]])
    def update(self, x_shift):
        self.rect.x += x_shift

spikes = []
for i in range(4):
    spikes.append(pygame.image.load('assets/spikes/' + str(i+1) + '.png'))

class Spike(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = random.choice(spikes)
        self.rect = self.image.get_rect(topleft = [position[0], position[1]])
    def update(self, x_shift):
        self.rect.x += x_shift

ramp_l = pygame.image.load('assets/ramp_l.png')
ramp_r = pygame.image.load('assets/ramp_r.png')
ramp_top_l = pygame.image.load('assets/ramp_top_l.png')
ramp_top_r = pygame.image.load('assets/ramp_top_r.png')

class Ramp(pygame.sprite.Sprite):
    def __init__(self, position, type):
        super().__init__()
        if type == 1:
            self.image = ramp_l
        elif type == 2:
            self.image = ramp_r
        elif type == 3:
            self.image = ramp_top_l
        elif type == 4:
            self.image = ramp_top_r
        self.rect = self.image.get_rect(topleft = [position[0], position[1]])

    def update(self, x_shift):
        self.rect.x += x_shift

block = pygame.image.load('assets/moving_block.png')
class Moving_block(pygame.sprite.Sprite):
    def __init__(self, position, type):
        super().__init__()
        self.type = type
        self.image = block
        self.rect = self.image.get_rect(topleft = [position[0], position[1]+40])
        self.velocity = 2
    
    def update(self, x_shift):
        if self.type == 'x':
            self.rect.x += self.velocity
            self.rect.x += x_shift
        if self.type == 'y':
            self.rect.y += self.velocity
            self.rect.x += x_shift

souls = []
for i in range(10):
    souls.append (pygame.image.load('assets/souls/'+str(i)+'.png'))
class Souls(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = souls[9]
        self.rect = self.image.get_rect(topleft = [position[0]-4, position[1]-2])
        self.animation_speed = 0.1
        self.animation_index = 0
    
    def animation(self):
        self.image = souls[int(self.animation_index)]

    def update(self, x_shift, status):
        if self.animation_index > len(souls)-2:
            self.animation_index = 0
        else:    
            self.animation_index += self.animation_speed
        if not status:
            self.animation()
        else:
            self.image = souls[9]
        self.rect.x += x_shift
    