import pygame
import sys
import time
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from sounds import *
from resources import level1, screen_height, screen_width
from world_generation import World
from settings import *


pygame.init()
COLOR_INACTIVE = pygame.Color("Grey")
COLOR_ACTIVE = pygame.Color("Yellow")
FONT = pygame.font.Font("assets/ariel.TTF", 20)
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spook alle")
icon = pygame.image.load("scarecrow.ico")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.set_num_channels(10)

# channel 0 is for bgm
# channel 1 is for wolf
# channel 2 is for player movement
# channel 3 ghost
# channel 4 soul
# channel 5 blood and more deep elements
# channel 6 torch
# channel 7 player hurt
# channel 8 trident stab
# channel 9 spikes

wolf_interval = random.randint(1000, 2000)
# audio controls
pygame.mixer.Channel(0).set_volume(channel0_volume * int(volume))
pygame.mixer.Channel(1).set_volume(channel1_volume * int(volume))
pygame.mixer.Channel(2).set_volume(channel2_volume * int(volume))
pygame.mixer.Channel(3).set_volume(channel3_volume * int(volume))
pygame.mixer.Channel(4).set_volume(channel4_volume * int(volume))
pygame.mixer.Channel(5).set_volume(channel5_volume * int(volume))
pygame.mixer.Channel(6).set_volume(channel6_volume * int(volume))
pygame.mixer.Channel(7).set_volume(channel7_volume * int(volume))
pygame.mixer.Channel(8).set_volume(channel8_volume * int(volume))
pygame.mixer.Channel(9).set_volume(channel9_volume * int(volume))
pygame.mixer.Channel(1).play(
    pygame.mixer.Sound(random.choice(wolf)), 0, 0, 1000
)  # playing wolf howling randomly

# ----------------------- textures dependencies

top_death = pygame.image.load("assets/top_death.png").convert_alpha()
font = pygame.font.Font("assets/ariel.TTF", 15)
font_welcome = pygame.font.Font("assets/ariel.TTF", 25)
font_internal = pygame.font.Font("assets/ariel.TTF", 45)
mist_dark = pygame.image.load("assets/mist_dark.png").convert_alpha()
mist_light = pygame.image.load("assets/mist_light.png").convert_alpha()
bg = pygame.image.load("assets/background.png").convert_alpha()
bg1 = pygame.image.load("assets/dark_bg.png").convert_alpha()
resume = pygame.image.load("assets/Resume.png").convert()
home = pygame.image.load("assets/home_page.png").convert_alpha()
side_bar = pygame.image.load("assets/side_bar.png").convert_alpha()
help = pygame.image.load("assets/help.png").convert_alpha()
about = pygame.image.load("assets/about.png").convert_alpha()
settings = pygame.image.load("assets/settings.png").convert_alpha()
cursor = pygame.image.load("assets/cursor.png").convert_alpha()
volume_on_font = font_internal.render("ON", True, "Yellow")
volume_off_font = font_internal.render("OFF", True, "Yellow")
start_page = pygame.image.load("assets/banner.png").convert_alpha()

mist = [mist_light, mist_dark][get_save_data()[0]]
volume_font = [volume_off_font, volume_on_font][int(volume)]

if get_save_data()[0] == 0:
    darkness_font = font_internal.render("Level 1", True, "Yellow")
else:
    darkness_font = font_internal.render("Level 2", True, "Yellow")


# defining FPS
def fps():
    fps = "FPS: " + str(int(clock.get_fps()))
    return fps


class InputBox:
    def __init__(self, x, y, w, h, plain_surface, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.plain_surface = plain_surface
        self.end = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    save_game_data("name", self.text)
                    try:
                        get_leader_board_data()[self.text]
                    except:
                        add_new_player_to_database(self.text)
                    self.text = ""
                    self.end = True
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


box = InputBox(1000, 100, 140, 32, screen)
start = True
while 1:
    while start:
        screen.blit(start_page, (0, 0))
        screen.blit(cursor, pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                time.sleep(0.6)
                start = False
        pygame.display.update()
        clock.tick(60)

    while home_page_time:
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]
        screen.blit(home, (0, 0))
        name = font_welcome.render("Player: " + str(get_save_data()[3]), True, "Yellow")
        new_final = font_welcome.render(
            "Score: "
            + str(
                get_leader_board_data()[str(get_save_data()[3])][0]
                + get_leader_board_data()[str(get_save_data()[3])][1]
            ),
            True,
            "Yellow",
        )
        screen.blit(name, (1000, 230))
        screen.blit(new_final, (1000, 280))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            box.handle_event(event)
            if (x >= 66 and x <= 333) and (y >= 233 and y <= 269):  # New game selection
                hover_home_screen = [1, 0, 0, 0, 0, 0]
                if event.type == MOUSEBUTTONDOWN:
                    world = World(level1, screen, 0)
                    add_new_player_to_database(get_save_data()[3])
                    home_page_time = 0

            elif (x >= 64 and x <= 284) and (
                y >= 308 and y <= 345
            ):  # continue game selection
                hover_home_screen = [0, 1, 0, 0, 0, 0]
                if event.type == MOUSEBUTTONDOWN:
                    home_page_time = 0
                    world = World(level1, screen, get_save_data()[2])

            elif (x >= 65 and x <= 266) and (
                y >= 384 and y <= 421
            ):  # settings selection
                hover_home_screen = [0, 0, 1, 0, 0, 0]
                settings_in = True
                if event.type == MOUSEBUTTONDOWN:
                    while settings_in:
                        screen.blit(settings, (0, 0))

                        x = pygame.mouse.get_pos()[0]
                        y = pygame.mouse.get_pos()[1]

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                            elif (
                                (x >= 222 and x <= 448)
                                and (y >= 142 and y < 187)
                                and event.type == MOUSEBUTTONDOWN
                                and settings_click_time[0]
                            ):
                                settings_click_time[0] = 0

                                if not volume:
                                    volume = True
                                    pygame.mixer.Channel(0).set_volume(0.05 * volume)
                                    pygame.mixer.Channel(1).set_volume(0.02 * volume)
                                    pygame.mixer.Channel(2).set_volume(0.2 * volume)
                                    pygame.mixer.Channel(3).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(4).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(5).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(6).set_volume(0.5 * volume)
                                    pygame.mixer.Channel(7).set_volume(0.5 * volume)
                                    pygame.mixer.Channel(8).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(9).set_volume(1 * volume)
                                    volume_font = font_internal.render(
                                        "ON", True, "Yellow"
                                    )

                                else:
                                    volume = False
                                    pygame.mixer.Channel(0).set_volume(0.05 * volume)
                                    pygame.mixer.Channel(1).set_volume(0.02 * volume)
                                    pygame.mixer.Channel(2).set_volume(0.2 * volume)
                                    pygame.mixer.Channel(3).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(4).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(5).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(6).set_volume(0.5 * volume)
                                    pygame.mixer.Channel(7).set_volume(0.5 * volume)
                                    pygame.mixer.Channel(8).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(9).set_volume(1 * volume)
                                    volume_font = font_internal.render(
                                        "OFF", True, "Yellow"
                                    )

                            elif (
                                (x >= 228 and x <= 507)
                                and (y >= 261 and y <= 305)
                                and event.type == MOUSEBUTTONDOWN
                                and settings_click_time[1]
                            ):
                                settings_click_time[1] = 0
                                if not darkness:
                                    darkness = True
                                    darkness_font = font_internal.render(
                                        "Level 2", True, "Yellow"
                                    )
                                    mist = mist_dark
                                else:
                                    darkness = False
                                    darkness_font = font_internal.render(
                                        "Level 1", True, "Yellow"
                                    )
                                    mist = mist_light

                            elif (
                                (x >= 1237 and x <= 1255)
                                and (y >= 23 and y <= 44)
                                and event.type == MOUSEBUTTONDOWN
                            ):
                                settings_in = False
                            elif event.type == MOUSEBUTTONUP:
                                settings_click_time = [1, 1]
                                save_game_data("mist", int(darkness))
                        screen.blit(volume_font, (850, 142))
                        screen.blit(darkness_font, (850, 261))
                        screen.blit(cursor, pygame.mouse.get_pos())
                        pygame.display.update()
                        clock.tick(60)

            elif (x >= 62 and x <= 407) and (y >= 461 and y <= 497):  # about selection
                hover_home_screen = [0, 0, 0, 1, 0, 0]

                if event.type == MOUSEBUTTONDOWN:
                    click_home_screen = [1, 1, 1, 0, 1, 1]

                    while not click_home_screen[3]:
                        x, y = pygame.mouse.get_pos()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                            elif (
                                event.type == pygame.MOUSEBUTTONDOWN
                                and (x >= 1249 and x <= 1267)
                                and (y >= 9 and y <= 30)
                            ):
                                click_home_screen = [1, 1, 1, 1, 1, 1]

                        screen.blit(about, (0, 0))
                        screen.blit(cursor, pygame.mouse.get_pos())
                        pygame.display.update()
                        clock.tick(60)

            elif (x >= 66 and x <= 172) and (y >= 537 and y <= 573):  # help selection
                hover_home_screen = [0, 0, 0, 0, 1, 0]
                if event.type == MOUSEBUTTONDOWN:
                    click_home_screen = [1, 1, 1, 1, 0, 1]

                    while not click_home_screen[4]:
                        x, y = pygame.mouse.get_pos()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                            elif (
                                event.type == pygame.MOUSEBUTTONDOWN
                                and (x >= 1239 and x <= 1257)
                                and (y >= 15 and y <= 36)
                            ):
                                click_home_screen = [1, 1, 1, 1, 1, 1]

                        screen.blit(help, (0, 0))
                        screen.blit(cursor, pygame.mouse.get_pos())
                        pygame.display.update()
                        clock.tick(60)

            elif (x >= 66 and x <= 156) and (y >= 613 and y <= 649):  # exit selection
                hover_home_screen = [0, 0, 0, 0, 0, 1]
                if event.type == MOUSEBUTTONDOWN:
                    sys.exit()

            else:
                hover_home_screen = [0, 0, 0, 0, 0, 0]

        if hover_home_screen[0]:
            screen.blit(side_bar, (60, 233))
            if hover_home_play[0]:
                pygame.mixer.Channel(6).play(pygame.mixer.Sound(torch[2]), 0)
                hover_home_play = [0, 1, 1, 1, 1, 1]

        elif hover_home_screen[1]:
            screen.blit(side_bar, (60, 308))
            if hover_home_play[1]:
                pygame.mixer.Channel(6).play(pygame.mixer.Sound(torch[2]), 0)
                hover_home_play = [1, 0, 1, 1, 1, 1]

        elif hover_home_screen[2]:
            screen.blit(side_bar, (60, 384))
            if hover_home_play[2]:
                pygame.mixer.Channel(6).play(pygame.mixer.Sound(torch[2]), 0)
                hover_home_play = [1, 1, 0, 1, 1, 1]

        elif hover_home_screen[3]:
            screen.blit(side_bar, (60, 461))
            if hover_home_play[3]:
                pygame.mixer.Channel(6).play(pygame.mixer.Sound(torch[2]), 0)
                hover_home_play = [1, 1, 1, 0, 1, 1]

        elif hover_home_screen[4]:
            screen.blit(side_bar, (60, 537))
            if hover_home_play[4]:
                pygame.mixer.Channel(6).play(pygame.mixer.Sound(torch[2]), 0)
                hover_home_play = [1, 1, 1, 1, 0, 1]

        elif hover_home_screen[5]:
            screen.blit(side_bar, (60, 613))
            if hover_home_play[5]:
                pygame.mixer.Channel(6).play(pygame.mixer.Sound(torch[2]), 0)
                hover_home_play = [1, 1, 1, 1, 1, 0]

        box.draw(screen)
        box.update()
        screen.blit(cursor, pygame.mouse.get_pos())
        pygame.display.update()
        clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not pygame.mixer.Channel(1).get_busy() and wolf_interval <= 0:
        pygame.mixer.Channel(1).play(pygame.mixer.Sound(random_track(wolf)), 0)
        wolf_interval = random.randint(1000, 1500)
    wolf_interval -= 1

    if world.battry() == 1:
        screen.blit(bg1, [0, 0])
    else:
        screen.blit(bg, [0, 0])
    dir_font = font.render(fps(), False, (255, 255, 0))
    world.run()
    screen.blit(mist, (0, 0))
    screen.blit(dir_font, dir_font.get_rect(center=(1250, 20)))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        resume_menu = True

    while resume_menu:
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            screen.blit(resume, (0, 2))
            if (x >= 557 and x <= 751) and (y >= 176 and y <= 212):
                r = True
                s = False
                a = False
                if event.type == MOUSEBUTTONDOWN:
                    resume_menu = False

            elif (x >= 553 and x <= 754) and (y >= 279 and y <= 325):
                r = False
                s = True
                a = False
                if event.type == MOUSEBUTTONDOWN:
                    settings_in = True
                    while settings_in:
                        screen.blit(settings, (0, 0))

                        x = pygame.mouse.get_pos()[0]
                        y = pygame.mouse.get_pos()[1]

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                            elif (
                                (x >= 222 and x <= 448)
                                and (y >= 142 and y < 187)
                                and event.type == MOUSEBUTTONDOWN
                                and settings_click_time[0]
                            ):
                                settings_click_time[0] = 0

                                if not volume:
                                    volume = True
                                    pygame.mixer.Channel(0).set_volume(0.05 * volume)
                                    pygame.mixer.Channel(1).set_volume(0.02 * volume)
                                    pygame.mixer.Channel(2).set_volume(0.2 * volume)
                                    pygame.mixer.Channel(3).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(4).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(5).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(6).set_volume(0.5 * volume)
                                    pygame.mixer.Channel(7).set_volume(0.5 * volume)
                                    pygame.mixer.Channel(8).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(9).set_volume(1 * volume)
                                    volume_font = font_internal.render(
                                        "ON", True, "Yellow"
                                    )

                                else:
                                    volume = False
                                    pygame.mixer.Channel(0).set_volume(0.05 * volume)
                                    pygame.mixer.Channel(1).set_volume(0.02 * volume)
                                    pygame.mixer.Channel(2).set_volume(0.2 * volume)
                                    pygame.mixer.Channel(3).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(4).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(5).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(6).set_volume(0.5 * volume)
                                    pygame.mixer.Channel(7).set_volume(0.5 * volume)
                                    pygame.mixer.Channel(8).set_volume(0.1 * volume)
                                    pygame.mixer.Channel(9).set_volume(1 * volume)
                                    volume_font = font_internal.render(
                                        "OFF", True, "Yellow"
                                    )

                            elif (
                                (x >= 228 and x <= 507)
                                and (y >= 261 and y <= 305)
                                and event.type == MOUSEBUTTONDOWN
                                and settings_click_time[1]
                            ):
                                settings_click_time[1] = 0
                                if not darkness:
                                    darkness = True
                                    darkness_font = font_internal.render(
                                        "Level 2", True, "Yellow"
                                    )
                                    mist = mist_dark
                                else:
                                    darkness = False
                                    darkness_font = font_internal.render(
                                        "Level 1", True, "Yellow"
                                    )
                                    mist = mist_light

                            elif (
                                (x >= 1237 and x <= 1255)
                                and (y >= 23 and y <= 44)
                                and event.type == MOUSEBUTTONDOWN
                            ):
                                settings_in = False
                            elif event.type == MOUSEBUTTONUP:
                                settings_click_time = [1, 1]
                                save_game_data("mist", int(darkness))
                                save_game_data("sound", int(volume))
                        screen.blit(volume_font, (850, 142))
                        screen.blit(darkness_font, (850, 261))
                        screen.blit(cursor, pygame.mouse.get_pos())
                        pygame.display.update()
                        clock.tick(60)

            elif (x >= 609 and x <= 699) and (y >= 384 and y <= 420):
                r = False
                s = False
                a = True
                if event.type == MOUSEBUTTONDOWN:
                    home_page_time = 1
                    resume_menu = 0
                    try:
                        save_leaderboard_temp_score(get_save_data()[3], world.run_score)
                    except:
                        add_new_player_to_database(get_save_data()[3])

            else:
                r = False
                s = False
                a = False

        if r == True:
            screen.blit(side_bar, (547, 178))
            if resume_menu_play[0] == 1:
                pygame.mixer.Channel(6).play(pygame.mixer.Sound(torch[2]), 0)
                resume_menu_play = [0, 1, 1]
        elif s == True:
            screen.blit(side_bar, (543, 282))
            if resume_menu_play[1] == 1:
                pygame.mixer.Channel(6).play(pygame.mixer.Sound(torch[2]), 0)
                resume_menu_play = [1, 0, 1]
        elif a == True:
            screen.blit(side_bar, (599, 386))
            if resume_menu_play[2] == 1:
                pygame.mixer.Channel(6).play(pygame.mixer.Sound(torch[2]), 0)
                resume_menu_play = [1, 1, 0]

        screen.blit(cursor, pygame.mouse.get_pos())
        pygame.display.update()

    # print(fps())

    screen.blit(cursor, pygame.mouse.get_pos())
    pygame.display.update()
    clock.tick(60)
