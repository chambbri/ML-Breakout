import pygame
from brick import *


class Paddle(Brick):
    def move_paddle(self, x_limit_l, x_limit_r):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT] and self.x_cord + self.width < x_limit_r:
            self.x_cord += 1
        elif key[pygame.K_LEFT] and self.x_cord > x_limit_l:
            self.x_cord -= 1

        self.rect.topleft = (int(self.x_cord), int(self.y_cord))
