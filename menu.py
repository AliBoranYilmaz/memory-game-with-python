import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame
pygame.init()

from settings import *

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Remember the pattern!")

font = pygame.font.SysFont("Bahnschrift", 40)
start_text = font.render("Start Game", True, YELLOW)
quit_text = font.render("Quit", True, YELLOW)

# calculate the position of the menu options
start_x = WIDTH/2 - start_text.get_width()/2
start_y = HEIGHT/2 - start_text.get_height()/2 - 50
quit_x = WIDTH/2 - quit_text.get_width()/2
quit_y = HEIGHT/2 - quit_text.get_height()/2 + 50

start_rect = start_text.get_rect(topleft=(start_x, start_y))
quit_rect = quit_text.get_rect(topleft=(quit_x, quit_y))

def display_menu():
    # display the menu options on the screen
    screen.blit(start_text, (start_x, start_y))
    screen.blit(quit_text, (quit_x, quit_y))

def handle_input():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if start_rect.collidepoint(mouse_pos):
                import main  # link to main game file
                game = main.Game()
                while True:
                    game.new()
                    game.run()
        
            elif quit_rect.collidepoint(mouse_pos):
                pygame.quit()
                quit(0)
            
running = True
while running:
    screen.fill((0, 0, 0))  # clear the screen
    display_menu()
    handle_input()
    pygame.display.update()