import random
import pygame, sys
from ghost_block import Decor, Ghost_block, Moving_block, Next_stage, Grave, Ramp, Scarecrow, Spike, Souls
from resources import tile_size, screen_width
from tiles import Tile
from player import Player
from trees import Tree
from ghost import Ghost
from cell import Battery
from grass_on_block import Grass
from sounds import *
from settings import get_save_data, save_game_data, save_leaderboard_final_score, save_leaderboard_temp_score, add_new_player_to_database

last_stage = get_save_data()[2]

top_death = pygame.image.load('assets/top_death.png')



class World:
    def __init__(self, level_data, surface, stage):
        self.level_data = level_data
        self.display_surface =  surface 
        self.world_shift = 0
        self.stage = stage
        self.battery_list = []
        self.level_update = level_data[self.stage]
        self.setup_level()
        self.gravity = 0.8
        self.top_rect_velocity = 4
        self.top_rect = top_death.get_rect(topleft = [0, -1000])
        self.game_freeze = False
        self.stunned = 100
        self.impact_repeat = True           #for ghost collsion impact
        self.impact_repeat2 = True          #for trident stab
        self.collision_point_on_moving_block = 0
        self.run_score = 0
        self.resume_screen = False
    def setup_level(self):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound(random_track(bgm)), -1,  0, 10000)
        self.block = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.trees = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()
        self.ghost_b = pygame.sprite.Group()
        self.grass_on = pygame.sprite.Group()
        self.next_stage = pygame.sprite.GroupSingle()
        self.decoration = pygame.sprite.Group()
        self.battery_obj = pygame.sprite.GroupSingle()
        self.graves = pygame.sprite.Group()
        self.scarecrows = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.ramps = pygame.sprite.Group()
        self.moving_blocks = pygame.sprite.Group()
        self.souls = pygame.sprite.GroupSingle()
        self.claimed = False
        self.soul_music_played = False

        for col_num, i in enumerate(self.level_update):
            for row_num, j in enumerate(i):

                x = row_num * tile_size
                y = col_num * tile_size

                if j == 'X':
                    tile  = Tile((x,y), tile_size)
                    self.block.add(tile)

                elif j == 'P':
                    player = Player((x,y))
                    self.player.add(player)

                elif j == 'T':
                    tree = Tree((x,y))
                    self.trees.add(tree)

                elif j == 'G':
                    ghost = Ghost((x,y))
                    self.ghosts.add(ghost)

                elif j == 'Z':
                    ghost_block = Ghost_block((x,y))
                    self.ghost_b.add(ghost_block)

                elif j == 'N':
                    n_stage = Next_stage((x,y))
                    self.next_stage.add(n_stage)

                elif j == 'D':
                    decor = Decor((x,y))
                    self.decoration.add(decor)

                elif j == 'Y':
                    decor = Grave((x,y))
                    self.graves.add(decor)
                
                elif j == 'S':
                    decor = Scarecrow((x,y))
                    self.scarecrows.add(decor)

                elif j == '0':
                    spike = Spike((x,y))
                    self.spikes.add(spike)

                elif j == '1':
                    ramp = Ramp((x,y), 1)
                    self.ramps.add(ramp)

                elif j == '2':
                    ramp = Ramp((x,y), 2)
                    self.ramps.add(ramp)
                
                elif j == '3':
                    ramp = Ramp((x,y), 3)
                    self.ramps.add(ramp)
                
                elif j == '4':
                    ramp = Ramp((x,y), 4)
                    self.ramps.add(ramp)

                elif j == '5':
                    moving_block = Moving_block((x,y), 'x')
                    self.moving_blocks.add(moving_block)

                elif j == '6':
                    moving_block = Moving_block((x,y), 'y')
                    self.moving_blocks.add(moving_block)

                elif j == 's':
                    soul = Souls((x,y))
                    self.souls.add(soul)

                elif j == 'B':
                    self.battery_list.append((x, y))

                if col_num < len(self.level_update)-1 and (self.level_update[col_num + 1])[row_num] == 'X' and j != 'X':
                    grass = Grass((x,y), 0)
                    self.grass_on.add(grass)

                if (j == ' ' or j == 'N' or j == 'P' or j == '0' or j == 'Z') and row_num > 0 and i[row_num - 1] == 'X':
                     grass = Grass((x-20,y-64), 1)
                     self.grass_on.add(grass)

                if (j == ' ' or j == 'N' or j == 'P' or j == '0' or j == 'Z') and row_num < len(i)-1 and i[row_num + 1] == 'X':
                     grass = Grass((x+54,y-64), -1)
                     self.grass_on.add(grass)

        self.battery_func()
        
    def battery_func(self):
        self.random_pos = random.choice(self.battery_list) 
        battery = Battery(self.random_pos)
        self.battery_obj.add(battery)

    def scroll_x(self):
    
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width/4 + 64 and direction_x < 0:
            self.world_shift = 4
            player.speed = 0
        elif player_x > 1200 - (screen_width/4) and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 1

        self.run_score -= self.world_shift


    def gate_collision(self):
        gate = self.next_stage.sprite
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        if gate.rect.colliderect(player.rect) and player.rect.x - gate.rect.x <= 185 and player.rect.x - gate.rect.x > 70 and player.gate_in and self.claimed:
            self.stage += 1
            try:
                self.level_update = self.level_data[self.stage]
                self.setup_level()
                try:
                    save_leaderboard_final_score(get_save_data()[3], self.run_score)
                except:
                    add_new_player_to_database(get_save_data()[3])
            except:
                print("well played! :)")
                sys.exit()

    def battery_collision(self):
        battery = self.battery_obj.sprite
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        if (battery.rect.x >= player.rect.x and battery.rect.x <= player.rect.x+23) and (battery.rect.y >= player.rect.y and battery.rect.y <= player.rect.y+59):
            pygame.mixer.Channel(8).play(pygame.mixer.Sound(torch[1]))
            player.battery = 3000
            self.battery_func()

    def soul_collision(self):
        soul = self.souls.sprite
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        if (soul.rect.x-10 <= player.rect.x and soul.rect.x+74 > player.rect.x) and (soul.rect.y+64 > player.rect.y and soul.rect.y <= player.rect.y):
            if self.soul_music_played == False:
                pygame.mixer.Channel(4).play(pygame.mixer.Sound(soul_sound))
                self.soul_music_played = True
            self.claimed = True

    def ghost_horizontal_movement_collisions(self):
        for ghosts in self.ghosts.sprites():
            ghosts.rect.x += ghosts.direction.x * ghosts.speed
            for sprite in self.block.sprites():
                if sprite.rect.colliderect(ghosts.rect):
                    if ghosts.direction.x < 0:
                        ghosts.rect.left = sprite.rect.right
                        ghosts.direction.x *= -1

                    elif ghosts.direction.x > 0:
                        ghosts.rect.right = sprite.rect.left
                        ghosts.direction.x *= -1

        for ghosts in self.ghosts.sprites():
            ghosts.rect.x += ghosts.direction.x * ghosts.speed
            for sprite in self.ghost_b.sprites():
                if sprite.rect.colliderect(ghosts.rect):
                    if ghosts.direction.x < 0:
                        ghosts.rect.left = sprite.rect.right
                        ghosts.direction.x *= -1

                    elif ghosts.direction.x > 0:
                        ghosts.rect.right = sprite.rect.left
                        ghosts.direction.x *= -1

    def ghost_player_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for ghosts in self.ghosts.sprites():
            ghosts.rect.x += ghosts.direction.x * ghosts.speed
            if ghosts.rect.colliderect(player.rect):
                if not pygame.mixer.Channel(3).get_busy() and self.impact_repeat:
                    self.impact_repeat = False
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound(impact[1]))
                pygame.mixer.Channel(2).stop()
                self.game_freeze = True
                self.top_rect.x = player.rect.x - 18
                player.ghosted = True
                player.direction.x = 0
                player.direction.y = 0
                ghosts.direction.x = 0

    def moving_block_horizontal_movement_collision(self):
        for moving_block in self.moving_blocks.sprites():
            if moving_block.type == 'x':
                for sprite in self.ghost_b.sprites():
                    if sprite.rect.colliderect(moving_block.rect):
                        if moving_block.velocity < 0:
                            moving_block.rect.left = sprite.rect.right
                            moving_block.velocity *= -1

                        elif moving_block.velocity > 0:
                            moving_block.rect.right = sprite.rect.left
                            moving_block.velocity *= -1

        for moving_block in self.moving_blocks.sprites():
            if moving_block.type == 'x':
                for sprite in self.block.sprites():
                    if sprite.rect.colliderect(moving_block.rect):
                        if moving_block.velocity < 0:
                            moving_block.rect.left = sprite.rect.right
                            moving_block.velocity *= -1

                        elif moving_block.velocity > 0:
                            moving_block.rect.right = sprite.rect.left
                            moving_block.velocity *= -1

    def moving_block_vertical_movement_collision(self):
        for moving_block in self.moving_blocks.sprites():
            if moving_block.type == 'y':
                moving_block.rect.y += moving_block.velocity
                for sprite in self.ghost_b.sprites():
                    if sprite.rect.colliderect(moving_block.rect):
                        if moving_block.velocity < 0:
                            moving_block.rect.top = sprite.rect.bottom
                            moving_block.velocity *= -1

                        elif moving_block.velocity > 0:
                            moving_block.rect.bottom = sprite.rect.top
                            moving_block.velocity *= -1
        
        for moving_block in self.moving_blocks.sprites():
            if moving_block.type == 'y':
                for sprite in self.block.sprites():
                    if sprite.rect.colliderect(moving_block.rect):
                        if moving_block.velocity < 0:
                            moving_block.rect.top = sprite.rect.bottom
                            moving_block.velocity *= -1

                        elif moving_block.velocity > 0:
                            moving_block.rect.bottom = sprite.rect.top
                            moving_block.velocity *= -1

    def horizontal_movement_collisions(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.block.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.direction.x = 0
                    if player.hold > 0:
                        player.landing_status = 1
                        player.hold -= 40
                    else:
                        player.landing_status = 0

                elif player.direction.x > 0:
                    player.direction.x = 0
                    player.rect.right = sprite.rect.left
                    player.hold = 50
                    player.landing_status = 0


        for ramp in self.ramps.sprites():
            if ramp.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = ramp.rect.right
                    player.direction.x = 0
                    if player.hold > 0:
                        player.landing_status = 1
                        player.hold -= 40
                    else:
                        player.landing_status = 0

                elif player.direction.x > 0:
                    player.direction.x = 0
                    player.rect.right = ramp.rect.left
                    player.hold = 50
                    player.landing_status = 0

    def vertical_movement_collisions(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.block.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0 and player.rect.y-1<=sprite.rect.y:
                    player.rect.bottom = sprite.rect.top
                    player.landing_status = 1
                    player.direction.y = 0
                    player.on_ground = True

                elif player.direction.y < 0 and player.rect.y-1>=sprite.rect.y:
                    player.rect.top = sprite.rect.bottom
                    player.landing_status = 0
                    player.direction.y = 0
                    player.on_ground = False 
        
        for ramp in self.ramps.sprites():
            if ramp.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = ramp.rect.top
                    player.landing_status = 1
                    player.direction.y = 0
                    player.on_ground = True

                elif player.direction.y < 0:
                    player.rect.top = ramp.rect.bottom
                    player.landing_status = 0
                    player.direction.y = 0
                    player.on_ground = False

    def moving_block_player_vertical_collision(self):
        player = self.player.sprite
        player.rect.x+= player.direction.x*player.speed

        for sprite in self.moving_blocks.sprites():
            if sprite.rect.colliderect(player.rect):
                self.collision_point_on_moving_block = player.rect.x - sprite.rect.x
                if player.direction.y >= 0 and player.rect.y - sprite.rect.y <= 64:
                    player.rect.bottom = sprite.rect.top
                    player.landing_status = 1
                    player.direction.y = 0
                    player.rect.x =  sprite.rect.x + 10
                    player.on_ground = True
                    if sprite.rect.x <= (1/4)* screen_width:
                        player.direction.x = -1
                    elif sprite.rect.x >= (3/4)* screen_width:
                        player.direction.x = 1
                    else:
                        player.direction.x = 0
                else:
                    player.on_moving_block = False
                    
    def spikes_collisions(self):
        player = self.player.sprite
        for sprite in self.spikes.sprites():
            if sprite.rect.colliderect(player.rect) and player.rect.y > 680:
                if player.direction.y > 0:
                    pygame.mixer.Channel(9).play(pygame.mixer.Sound(spike_stab), 0, 0, 10000)
                    player.torch_status = False
                    player.rect.bottom = sprite.rect.bottom
                    player.direction.x = 0
                    player.direction.y = 0
                    player.dead = True
                    save_game_data("stage", self.stage)
                    try:
                        save_leaderboard_temp_score(get_save_data()[3], self.run_score)
                    except:
                        add_new_player_to_database(get_save_data()[3])

    def battry(self):
        player = self.player.sprite
        if player.battery <= 0 or player.torch_status == False and (player.dead == False and player.ghosted == False):
            return 1
        else:
            return 0

    def dead(self, surface):
        player = self.player.sprite
        if player.ghosted == True:
            try:
                save_leaderboard_temp_score(get_save_data()[3], self.run_score)
            except:
                add_new_player_to_database(get_save_data()[3])
            self.stunned -=1
        if player.ghosted == True and self.stunned <= 0:
            if player.rect.y - self.top_rect.y > 700:
                self.top_rect_velocity += 0.8
                self.top_rect.y += self.top_rect_velocity

            else:
                player.torch_status = False
                if self.impact_repeat2:
                    self.impact_repeat2 = False
                    pygame.mixer.Channel(7).play(pygame.mixer.Sound(trident_stab))
                    save_game_data('stage', self.stage)
            surface.blit(top_death, self.top_rect)

    def run (self):
        self.gate_collision()
        self.scroll_x()
        self.battery_collision()
        self.soul_collision()
        
        self.grass_on.draw(self.display_surface)
        self.grass_on.update(self.world_shift)

        self.battery_obj.draw(self.display_surface)
        self.battery_obj.update(self.world_shift)
        
        self.block.update(self.world_shift)
        self.block.draw(self.display_surface)

        self.ramps.update(self.world_shift)
        self.ramps.draw(self.display_surface)

        self.moving_blocks.update(self.world_shift)
        self.moving_blocks.draw(self.display_surface)

        self.souls.update(self.world_shift, self.claimed)
        self.souls.draw(self.display_surface)

        self.graves.draw(self.display_surface)
        self.graves.update(self.world_shift)

        self.scarecrows.draw(self.display_surface)
        self.scarecrows.update(self.world_shift)

        self.trees.draw(self.display_surface)
        self.trees.update(self.world_shift, self.display_surface)
    
        self.ghosts.draw(self.display_surface)
        self.ghosts.update(self.world_shift)

        self.ghost_b.draw(self.display_surface)
        self.ghost_b.update(self.world_shift)

        self.decoration.draw(self.display_surface)
        self.decoration.update(self.world_shift, self.display_surface)

        self.spikes.update(self.world_shift)
        self.spikes.draw(self.display_surface)

        self.next_stage.update(self.world_shift, self.claimed)
        self.next_stage.draw(self.display_surface)

        self.player.update(self.display_surface)
        self.player.draw(self.display_surface)

        self.moving_block_vertical_movement_collision()
        self.moving_block_horizontal_movement_collision()
        self.ghost_player_collision()
        self.horizontal_movement_collisions()
        self.ghost_horizontal_movement_collisions()
        self.vertical_movement_collisions()
        self.dead(self.display_surface)
        self.spikes_collisions()
        self.moving_block_player_vertical_collision()

        
        
        