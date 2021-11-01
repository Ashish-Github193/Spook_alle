import pygame

from sounds import *

image_dead = [pygame.image.load('char/on_spikesr.png'), pygame.image.load('char/on_spikesl.png')]
image_ghosted = [pygame.image.load('char/ghostedr.png'), pygame.image.load('char/ghostedl.png')]

class Player(pygame.sprite.Sprite):
    def __init__ (self, position):
        super().__init__()

        #animation
        self.images_left = []
        self.images_right = []
        self.images_left.append(pygame.image.load('char/l0.png'))
        self.images_left.append(pygame.image.load('char/l1.png'))
        self.images_left.append(pygame.image.load('char/l2.png'))
        self.images_right.append(pygame.image.load('char/r0.png'))
        self.images_right.append(pygame.image.load('char/r1.png'))
        self.images_right.append(pygame.image.load('char/r2.png'))
        self.torch_right = pygame.image.load('char/torch_right.png')
        self.torch_left = pygame.image.load('char/torch_left.png')
        self.grass = []
        for i in range(5):
            self.grass.append(pygame.image.load("assets/particle_effect/" + str(i+1) + ".png"))
        self.torch = self.torch_right
        self.facing_right = True
        self.index = 0
        self.index_grass = 0
        self.animation_speed = 0.2
        self.battery = 30000
        self.torch_status = True
        self.torch_on_time = 30
        self.gate_in = False
        self.foot_freq = 40
        #image
        self.image = self.images_left[0]

        self.rect = self.image.get_rect(topleft = [position[0], position[1]-10])
        self.direction = pygame.math.Vector2(0,0)
        self.landing_status = 1

        #movement
        self.speed = 1
        self.jump_speed = -16
        self.gravity = 0.7
        self.hold = 100
        self.on_ground = True

        #fire
        self.fire_pos = False
        self.dead = False
        self.ghosted = False
        self.on_moving_block = 0
        
        
    #getting input
    def get_input(self):
        keys = pygame.key.get_pressed()

        #moveing right
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
            self.torch = self.torch_right
            if self.on_ground and not pygame.mixer.Channel(2).get_busy():
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(walk))
            elif not self.on_ground:
                pygame.mixer.Channel(2).stop()
        
        #moving left
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
            self.torch = self.torch_left
            if self.on_ground and not pygame.mixer.Channel(2).get_busy():
                pygame.mixer.Channel(2).play(pygame.mixer.Sound(walk))
            elif not self.on_ground:
                pygame.mixer.Channel(2).stop()

        else:
            self.direction.x = 0
            pygame.mixer.Channel(2).stop()

        if keys[pygame.K_w]:
            self.gate_in = True

        if keys[pygame.K_s]:
            self.gate_in = False

        #jump
        if keys[pygame.K_SPACE] and self.landing_status > 0 and self.fire_pos == False:
            self.landing_status = -1
            self.jump()
        else:
            # self.gravity = self.gravity
            self.landing_status = -1

        if keys[pygame.K_LSHIFT] and self.torch_on_time == 0:
            pygame.mixer.Channel(6).play(pygame.mixer.Sound(torch[0]))
            if self.torch_status == False:
                self.torch_status = True
            else:
                self.torch_status = False
            self.torch_on_time = 30

    #animation
    def animate(self):
        
        if self.direction.x == 0 and self.facing_right == True:
            self.image = self.images_right[2]

        elif self.direction.x == 0 and self.facing_right == False:
            self.image = self.images_left[2]

        elif self.facing_right == True:
            self.image = self.images_right[int(self.index/2)]
            self.index_grass += self.animation_speed

        else:
            self.image = self.images_left[int(self.index/2)]
            self.index_grass += self.animation_speed

    #jump
    def jump(self):
        self.direction.y = self.jump_speed
        self.on_ground = False

    #fire
    def particle_effect(self, surface):
        
        dust_particle = self.grass[int(self.index_grass)]

        if self.facing_right and self.direction.x != 0 and self.on_ground:
            surface.blit (dust_particle, [self.rect.x, self.rect.y+45])
        elif self.facing_right == False and self.direction.x != 0 and self.on_ground:
            flipped = pygame.transform.flip(dust_particle, True, False)
            surface.blit (flipped, [self.rect.x+25, self.rect.y+45])

    def dead_movement(self):
        if self.dead == True:
            self.speed = 0
            self.gravity = 0

    #appling gravity
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    #updating player attributes 
    def update(self, surface):

        #inputs
        if self.dead == False and self.ghosted == False:
            self.get_input()
        
        if self.dead == True:
            if self.facing_right == True:
                self.image = image_dead[0]
            else:
                self.image = image_dead[1]

        elif self.ghosted == True:
            if self.facing_right == True:
                self.image = image_ghosted[0]
            else:
                self.image = image_ghosted[1]
        else:
            self.animate()

        self.dead_movement() 

        #animation
        self.index += self.animation_speed
        if self.index > 5:
            self.index = 0
        
        
        if self.index_grass > 5:
            self.index_grass = 0

        if self.torch_status and self.battery > 0:
            surface.blit(self.torch, [self.rect.x, self.rect.y])
            self.battery -= 1
        
        if self.torch_on_time > 0:
            self.torch_on_time -= 1


        self.particle_effect(surface)
        #movement
        self.rect.x += self.direction.x * self.speed
    
    
