import pygame
from brick import *
from paddle import *

SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 600


def play_game():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    bricks = create_bricks(screen)
    paddle = create_paddle(screen)

    run = True
    while run:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, paddle.color, paddle.rect)
        for brick in bricks:
            pygame.draw.rect(screen, brick.color, brick.rect)

        paddle.move_paddle(0, SCREEN_WIDTH)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


def create_bricks(screen):
    x_cord = 2
    y_cord = 50
    colors = [(209, 23, 23), (209, 97, 23), (235, 225, 45), (133, 235, 45),
              (45, 235, 174), (45, 159, 235), (45, 51, 235)]
    row = 0

    brick_width = 100
    brick_height = 15
    bricks = []

    while row < 7:
        while x_cord + brick_width < SCREEN_WIDTH:
            brick = Brick(brick_width, brick_height, x_cord, y_cord, colors[row])
            # pygame.draw.rect(screen, brick.color, brick.rect)
            x_cord += brick_width + 5
            bricks.append(brick)
        x_cord = 2
        y_cord += brick_height + 5
        row += 1

    return bricks


def create_paddle(screen):
    x_cord = SCREEN_WIDTH / 2 - 100
    y_cord = SCREEN_HEIGHT - 25
    paddle_width = 200
    paddle_height = 10
    color = (7, 245, 245)
    paddle = Paddle(paddle_width, paddle_height, x_cord, y_cord, color)
    return paddle
