import pygame
from .brick import *

SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 600


class Paddle(Brick):
    def move_paddle(self, x_limit_l, x_limit_r, action=None, user="human"):
        if user == "human":
            key = pygame.key.get_pressed()
            if key[pygame.K_RIGHT] and self.x_cord + self.width < x_limit_r:
                self.x_cord += 1
            elif key[pygame.K_LEFT] and self.x_cord > x_limit_l:
                self.x_cord -= 1
        else:
            if action == 2 and self.x_cord + self.width < x_limit_r:
                self.x_cord += 1
            elif action == 1 and self.x_cord > x_limit_l:
                self.x_cord -= 1

        self.rect.topleft = (int(self.x_cord), int(self.y_cord))

    def reset_paddle(self):
        self.x_cord = SCREEN_WIDTH / 2 - 100
        self.y_cord = SCREEN_HEIGHT - 25
