import pygame


class Paddle:
    def __init__(self, width, height, x_cord, y_cord, color):
        self.width = width
        self.height = height
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.color = color
        self.rect = pygame.Rect((self.x_cord, self.y_cord, self.width, self.height))

    def move_paddle(self, x_limit_l, x_limit_r):
        key = pygame.key.get_pressed()

        if key[pygame.K_RIGHT] and self.x_cord + self.width < x_limit_r:
            self.rect.move_ip(1, 0)
            self.x_cord += 1
        elif key[pygame.K_LEFT] and self.x_cord > x_limit_l:
            self.rect.move_ip(-1, 0)
            self.x_cord -= 1
