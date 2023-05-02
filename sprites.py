import pygame
from settings import *
import math
import numpy

pygame.mixer.init() # initialize mixer for the sound that will play when clicked to a button

class Button():
    def __init__(self, x, y, color): # x and y are for coordinates of the button
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, BUTTON_SIZE, BUTTON_SIZE))

    def clicked(self, mouse_x, mouse_y):
        # if the mouse_x and mouse_y are both inside the button then it is clicked, return true
        return self.x <= mouse_x <= self.x + BUTTON_SIZE and self.y <= mouse_y <= self.y + BUTTON_SIZE
    
class Sound():
    def __init__(self, frequency):
        duration = 0.5 # beep duration
        bits = 16 # number of bits of data each sample will use
        sample_rate = 44100 # number of sample rates that will be generated in one second of audio
        total_samples = int(round(duration * sample_rate)) # total number of samples required by the sample rates and the duration of the sound (in seconds)
        data = numpy.zeros((total_samples, 2), dtype=numpy.int16) # data that will contain all the samples 
        max_sample = 2 ** (bits - 1) - 1 # largest possible value of a single sample that will be used

        for sample in range(total_samples):
            sample_time = float(sample) / sample_rate

            for channel in range(2): # we have two channels, left and right. it generates the data for the left and right side of the sound
                data[sample][channel] = int(round(max_sample * math.sin(2 * math.pi * frequency * sample_time)))
                # data is a sinus wave

        self.sound = pygame.sndarray.make_sound(data) # generate the sound
        self.current_channel = None

    def play(self):
        self.current_channel = pygame.mixer.find_channel(True)
        self.current_channel.play(self.sound)

class UserInterface():
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont("Bahnschrift", 16)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))        