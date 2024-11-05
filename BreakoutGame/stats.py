import pygame

class Stats:
    def __init__(self):
        self.score = 0;
        self.lives = 20;
        self.level = 1;

    def update_score(self, color):
        if color == "red":
            self.score += 12
        elif color == "orange":
            self.score += 10
        elif color == "yellow":
            self.score += 8
        elif color == "green":
            self.score += 6
        elif color == "aqua":
            self.score += 4
        elif color == "blue":
            self.score += 2
        elif color == "blueviolet":
            self.score += 1

    def update_lives(self):
        self.lives -= 1

    def update_level(self):
        self.level += 1
