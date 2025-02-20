import pygame


class Brick:
    def __init__(self, width, height, x_cord, y_cord, color):
        self.width = width
        self.height = height
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.color = color
        self.rect = pygame.Rect((self.x_cord, self.y_cord, self.width, self.height))

    def destroy(self):
        pass
