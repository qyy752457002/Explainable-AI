import pygame
import sys
sys.path.append('D:\XAI Process Mining Research\Python-Checkers-AI\checkers')

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('D:/XAI Process Mining Research/Python-Checkers-AI/assets/crown.png'), (44, 25))
