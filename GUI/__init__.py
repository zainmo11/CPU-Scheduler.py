import pygame


pygame.init()

WIDTH = 1280
HEIGHT = 720

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (211, 211, 211)

# limit FPS to 30 fps
FPS = 30
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

from .menu import * 
from .gui import GUIInterface
