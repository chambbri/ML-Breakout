import pygame
from .brick import *
from .paddle import *
from .ball import *
from .stats import *

SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 600


def play_game(screen, bricks, paddle, ball, stats):
    """Play game will use brick, paddle, ball, and stats objects to play breakout. The function
    is responsible for updating objects, calling functions for interactions, and keeping score via an
    infinite loop"""

    pygame.init()
    game_started = False
    run = True

    while run:
        # draw black background
        screen.fill((0, 0, 0))

        # draw paddle, ball, and brick objects to screen
        pygame.draw.rect(screen, paddle.color, paddle.rect)
        pygame.draw.circle(screen, ball.color, (ball.x_cord, ball.y_cord), ball.radius)
        for b in bricks:
            pygame.draw.rect(screen, b.color, b.rect)

        # user presses SPACE to start game and move ball
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not game_started:
            game_started = True

        # handle paddle and ball movements
        paddle.move_paddle(0, SCREEN_WIDTH)
        if game_started:
            ball.move_ball(SCREEN_HEIGHT)

        # handle ball collision with paddle, wall, and bricks
        if game_started:
            paddle_collision(paddle, ball)
            wall_collision(ball)
            brick_collision(ball, bricks, stats)

        # update scores and lives as needed
        display_score(stats.score, screen)
        display_lives(stats.lives, screen)

        # determine if life was lost and "pause" game if so
        lost = life_lost(ball, stats)
        if lost:
            game_started = False

        # if the user clears all bricks, reset them for next level and increase y speed to make the game harder
        if len(bricks) == 0:
            game_started = False
            stats.update_level()
            ball.reset_ball()
            ball.y_speed = abs(ball.y_speed) + 0.2
            bricks = create_bricks()
            pygame.display.update()
            pygame.time.delay(500)

        # game over, break out of loop
        if stats.lives == 0:
            run = False

        # listen for event to quit game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # update the display
        pygame.display.update()

    # call the game over function in case user wants to play again
    game_over(screen)


def setup_game():
    """Setup game creates the necessary objects to play breakout and calls play_game"""
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    bricks = create_bricks()
    paddle = create_paddle()
    ball = create_ball()
    stats = Stats()
    play_game(screen, bricks, paddle, ball, stats)


def create_bricks():
    """Creates the bricks to be broken. 7 rows of bricks are created with a different color for each row.
    Each row has 11 bricks"""

    # initial brick starting poiints
    x_cord = 2
    y_cord = 100

    colors = ["red", "orange", "yellow", "green",
              "aqua", "blue", "blueviolet"]
    row = 0

    # brick specs and list to hold all bricks
    brick_width = 100
    brick_height = 15
    bricks = []

    # create brick objects and add to bricks list
    while row < 7:
        while x_cord + brick_width < SCREEN_WIDTH:
            b = Brick(brick_width, brick_height, x_cord, y_cord, colors[row])
            x_cord += brick_width + 5
            bricks.append(b)
        x_cord = 2
        y_cord += brick_height + 5
        row += 1

    return bricks


def create_paddle():
    """Create the padel object that the user plays the game with"""
    x_cord = SCREEN_WIDTH / 2 - 100
    y_cord = SCREEN_HEIGHT - 25
    paddle_width = 200
    paddle_height = 10
    color = "cadetblue"
    paddle = Paddle(paddle_width, paddle_height, x_cord, y_cord, color)

    return paddle


def create_ball():
    """Create ball object"""
    radius = 10
    x_cord = SCREEN_WIDTH / 2 - 5
    y_cord = SCREEN_HEIGHT / 2 - 5
    color = "azure"
    ball = Ball(radius, x_cord, y_cord, color)

    return ball


def paddle_collision(paddle, ball):
    """Determine if the ball and paddle have collided"""
    if paddle.rect.colliderect(ball.rect):
        ball.y_speed *= -1  # reverse y-direction

        # determine x-direction and angle based on where it hit on paddle
        paddle_center = paddle.x_cord + (paddle.width / 2)
        ball_center = ball.x_cord + (ball.radius / 2)
        offset = (ball_center - paddle_center) / (paddle.width / 2)
        ball.x_speed = offset * ball.max_speed
        return True
    else:
        return False


def wall_collision(ball):
    """Reverse course of x or y direction depending on which wall the ball hit"""
    if ball.x_cord <= 0:
        ball.x_speed *= -1
    elif ball.x_cord >= SCREEN_WIDTH:
        ball.x_speed *= -1
    if ball.y_cord <= 0:
        ball.y_speed *= -1


def brick_collision(ball, bricks, stats):
    """Loop through bricks to determine if there have been any collisions, update score, and
    remove the brick from the bricks list"""
    for brick in bricks:
        if ball.rect.colliderect(brick.rect):
            ball.y_speed *= -1
            stats.update_score(brick.color)
            bricks.remove(brick)


def display_score(score, screen):
    """Add score to top right of screen"""
    font = pygame.font.SysFont("Arial", 30)
    img = font.render(f"{score}", True, "white")
    screen.blit(img, (SCREEN_WIDTH - 50, 10))


def display_lives(lives, screen):
    """Add lives to top left of screen"""
    font = pygame.font.SysFont("Arial", 30)
    img = font.render(f"{lives}", True, "white")
    screen.blit(img, (10, 10))


def life_lost(ball, stats):
    """Updates number of user lives if the ball has gone below the paddle and resets the ball to starting position"""
    if ball.y_cord >= SCREEN_HEIGHT:
        stats.update_lives()
        if stats.lives > 0:
            ball.reset_ball()
        return True
    return False


def game_over(screen):
    """Display new screen to user when their game is over and ask if they want to play again"""
    quit_game = False
    font = pygame.font.SysFont("Arial", 30)
    message = "GAME OVER: PRESS SPACE TO REPLAY, ESCAPE TO QUIT"
    img = font.render(message, True, "white")

    # if user closed window, do not go through game over loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

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
