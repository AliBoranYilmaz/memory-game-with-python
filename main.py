import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
# These two lines will prevent the 'Hello from the pygame community' message from appearing

import pygame
import random
from settings import *
from sprites import *
from test import *

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT)) # create the window
        pygame.display.set_caption(TITLE) # set the title of the window
        self.clock = pygame.time.Clock()

        self.colors = [DARKBLUE, DARKYELLOW, DARKGREEN, DARKRED]
        self.clicked_colors = [BLUE, YELLOW, GREEN, RED] # they will flash when clicked

        self.sounds = [Sound(BEEP1), Sound(BEEP2), Sound(BEEP3), Sound(BEEP4)]

        self.buttons = [
            Button(110, 50, DARKBLUE),
            Button(330, 50, DARKYELLOW),
            Button(110, 270, DARKGREEN),
            Button(330, 270, DARKRED)
        ]

    def new(self): # new game
        self.waiting_input = False
        self.pattern = []
        self.current_step = 0
        self.score = 0

    def run(self):
        self.playing = True
        
        while self.playing:
            self.clock.tick(FPS)
            self.clicked_button = None
            self.events()
            self.draw()
            self.update()

    def update(self):
        if not self.waiting_input: # computer will give the pattern
            pygame.time.wait(500) # 0.5 seconds
            self.pattern.append(random.choice(self.colors))

            for button in self.pattern:
                self.button_flash(button)
                pygame.time.wait(200)

            self.waiting_input = True

        else: # it is the user's turn to play
            # pushed the correct button
            if self.clicked_button and self.clicked_button == self.pattern[self.current_step]: # first condition: clicked button is not null
                self.button_flash(self.clicked_button)
                self.current_step += 1

            # pushed the last button of the pattern
                if self.current_step == len(self.pattern):
                    self.score += 1
                    self.waiting_input = False
                    self.current_step = 0

            # pushed the wrong button
            elif self.clicked_button and self.clicked_button != self.pattern[self.current_step]:
                self.game_over_animation()
                self.playing = False

    def button_flash(self, color):
        for i in range(len(self.colors)):
            if self.colors[i] == color:
                sound = self.sounds[i]
                flash_color = self.clicked_colors[i]
                button = self.buttons[i]

        original_surface = self.screen.copy()
        flash_surface = pygame.Surface((BUTTON_SIZE, BUTTON_SIZE))
        flash_surface = flash_surface.convert_alpha()
        red, green, blue = flash_color
        sound.play()

        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, ANIMATION_SPEED * step):
                self.screen.blit(original_surface, (0, 0))
                flash_surface.fill((red, green, blue, alpha))
                self.screen.blit(flash_surface, (button.x, button.y))
                pygame.display.update()
                self.clock.tick(FPS)
        
        self.screen.blit(original_surface, (0, 0))

    def game_over_animation(self):
        original_surface = self.screen.copy()
        flash_surface = pygame.Surface((self.screen.get_size()))
        flash_surface = flash_surface.convert_alpha()

        for beep in self.sounds:
            beep.play()
        
        red, green, blue = WHITE

        for _ in range(3):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, ANIMATION_SPEED * step):
                    self.screen.blit(original_surface, (0, 0))
                    flash_surface.fill((red, green, blue, alpha))
                    self.screen.blit(flash_surface, (0, 0))
                    pygame.display.update()
                    self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(BGCOLOR) # background is dark grey
        UserInterface(285, 20, f"Score: {str(self.score)}").draw(self.screen)

        for button in self.buttons:
            button.draw(self.screen) # draw all buttons

        pygame.display.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0) # exit with code 0

            if event.type == pygame.MOUSEBUTTONDOWN: # clicking
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for button in self.buttons:
                    if button.clicked(mouse_x, mouse_y):
                        self.clicked_button = button.color

game = Game()
while True:
    game.new()
    game.run()