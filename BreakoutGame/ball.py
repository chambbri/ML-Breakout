import pygame


class Ball:
    def __init__(self, radius, x_cord, y_cord, color):
        self.radius = radius
        self.x_start = x_cord
        self.y_start = y_cord
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.color = color
        self.y_speed = 0.6
        self.x_speed = 0.1
        self.max_speed = 0.5
        self.rect = pygame.Rect(int(self.x_cord - self.radius), int(self.y_cord - self.radius), self.radius * 2,
                                self.radius * 2)

    def move_ball(self, screen_h):
        if self.y_cord < screen_h:
            self.y_cord += self.y_speed
            self.x_cord += self.x_speed
            self.rect.topleft = (int(self.x_cord - self.radius), int(self.y_cord - self.radius))

    def reset_ball(self):
        self.x_cord = self.x_start
        self.y_cord = self.y_start
        self.x_speed = 0.1
