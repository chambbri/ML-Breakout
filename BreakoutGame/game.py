import pygame
from brick import *
from paddle import *
from ball import *
from stats import *

SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 600


def play_game(screen, bricks, paddle, ball, stats):
    pygame.init()

    game_started = False
    run = True
    while run:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, paddle.color, paddle.rect)
        pygame.draw.circle(screen, ball.color, (ball.x_cord, ball.y_cord), ball.radius)

        for brick in bricks:
            pygame.draw.rect(screen, brick.color, brick.rect)

        paddle.move_paddle(0, SCREEN_WIDTH)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not game_started:
            game_started = True
        if game_started:
            ball.move_ball(SCREEN_HEIGHT)

        paddle_collision(paddle, ball)
        wall_collision(ball)
        brick_collision(ball, bricks, stats)
        display_score(stats.score, screen)
        display_lives(stats.lives, screen)
        lost = life_lost(ball, stats)
        if lost:
            game_started = False

        if stats.lives == 0:
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        pygame.display.update()

    game_over(screen)


def setup_game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    bricks = create_bricks()
    paddle = create_paddle()
    ball = create_ball()
    stats = Stats()
    play_game(screen, bricks, paddle, ball, stats)


def create_bricks():
    x_cord = 2
    y_cord = 100
    colors = ["red", "orange", "yellow", "green",
              "aqua", "blue", "blueviolet"]
    row = 0

    brick_width = 100
    brick_height = 15
    bricks = []

    while row < 7:
        while x_cord + brick_width < SCREEN_WIDTH:
            brick = Brick(brick_width, brick_height, x_cord, y_cord, colors[row])
            x_cord += brick_width + 5
            bricks.append(brick)
        x_cord = 2
        y_cord += brick_height + 5
        row += 1

    return bricks


def create_paddle():
    x_cord = SCREEN_WIDTH / 2 - 100
    y_cord = SCREEN_HEIGHT - 25
    paddle_width = 200
    paddle_height = 10
    color = "cadetblue"
    paddle = Paddle(paddle_width, paddle_height, x_cord, y_cord, color)

    return paddle


def create_ball():
    radius = 10
    x_cord = SCREEN_WIDTH / 2 - 5
    y_cord = SCREEN_HEIGHT / 2 - 5
    color = "azure"
    ball = Ball(radius, x_cord, y_cord, color)

    return ball


def paddle_collision(paddle, ball):
    if paddle.rect.colliderect(ball.rect):
        ball.y_speed *= -1
        paddle_center = paddle.x_cord + (paddle.width / 2)
        ball_center = ball.x_cord + (ball.radius / 2)
        offset = (ball_center - paddle_center) / (paddle.width / 2)
        ball.x_speed = offset * ball.max_speed


def wall_collision(ball):
    if ball.x_cord <= 0:
        ball.x_speed *= -1
    elif ball.x_cord >= SCREEN_WIDTH:
        ball.x_speed *= -1
    if ball.y_cord <= 0:
        ball.y_speed *= -1


def brick_collision(ball, bricks, stats):
    for brick in bricks:
        if ball.rect.colliderect(brick.rect):
            ball.y_speed *= -1
            stats.update_score(brick.color)
            bricks.remove(brick)


def display_score(score, screen):
    font = pygame.font.SysFont("Arial", 30)
    img = font.render(f"{score}", True, "white")
    screen.blit(img, (SCREEN_WIDTH - 50, 10))


def display_lives(lives, screen):
    font = pygame.font.SysFont("Arial", 30)
    img = font.render(f"{lives}", True, "white")
    screen.blit(img, (10, 10))


def life_lost(ball, stats):
    if ball.y_cord >= SCREEN_HEIGHT:
        stats.update_lives()
        if stats.lives > 0:
            ball.reset_ball()
        return True
    return False


def game_over(screen):
    quit_game = False
    font = pygame.font.SysFont("Arial", 30)
    message = "GAME OVER: PRESS SPACE TO REPLAY, ESCAPE TO QUIT"
    img = font.render(message, True, "white")
    while not quit_game:
        screen.fill((0, 0, 0))
        text_rect = img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(img, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    setup_game()
                    return
                elif event.key == pygame.K_ESCAPE:
                    quit_game = True

        pygame.display.update()

    pygame.quit()
