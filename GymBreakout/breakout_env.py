import gym
import numpy as np
import pygame

from BreakoutGame.stats import Stats
from BreakoutGame.game import create_paddle, create_ball, create_bricks, paddle_collision, wall_collision, \
    brick_collision, life_lost, display_score, display_lives

SCREEN_WIDTH = 1260
SCREEN_HEIGHT = 600


class BreakoutEnv(gym.Env):

    def __init__(self):
        super(BreakoutEnv, self).__init__()
        pygame.init()

        # initialize game objects
        self.screen = None
        self.bricks = create_bricks()
        self.paddle = create_paddle()
        self.ball = create_ball()
        self.stats = Stats()

        num_bricks = len(self.bricks)
        self.observation_space = gym.spaces.Box(
            low=0, high=SCREEN_WIDTH, shape=(1 + 2 + 2 + num_bricks,), dtype=np.float32
        )

        # Actions: 0 = stay still, 1 = move left, 2 = move right
        self.action_space = gym.spaces.Discrete(3)

    def reset(self):
        # Reset game state
        self.paddle = create_paddle()
        self.ball = create_ball()
        self.bricks = create_bricks()
        self.stats = Stats()

        # Return the initial observation (game state)
        return self.get_obs()

    def step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        done = False
        reward = 0
        prev_score = self.stats.score

        self.ball.move_ball(SCREEN_HEIGHT)
        self.paddle.move_paddle(0, SCREEN_WIDTH, action, "agent")
        paddle_col = paddle_collision(self.paddle, self.ball)
        brick_col = brick_collision(self.ball, self.bricks, self.stats)
        wall_collision(self.ball)
        # display_score(self.stats.score, self.screen)
        # display_lives(self.stats.lives, self.screen)
        # print("Score: ", self.stats.score)
        if paddle_col:
            reward += 3
        if brick_col:
            reward += 0
        new_score = self.stats.score
        # reward += new_score - prev_score
        # proximity_reward = max(0, 1 - abs(self.paddle.x_cord - self.ball.x_cord) / (SCREEN_WIDTH / 2))
        # reward += 0.005 * proximity_reward  # Small reward at each step
        lost = life_lost(self.ball, self.paddle, self.stats)

        if lost:
            # penalty = -5 * (1 - proximity_reward)  # Scaled based on proximity at time of loss
            reward -= 3

        if len(self.bricks) == 0:
            # reward += 10
            done = True

        if self.stats.lives == 0:
            # reward -= 3
            done = True

        observation = self.get_obs()

        return observation, reward, done

    def get_obs(self):
        paddle_location = self.paddle.x_cord
        ball_location = [self.ball.x_cord, self.ball.y_cord]
        ball_velocity = list(self.ball.get_normalized_speed())
        relative_x = self.ball.x_cord - self.paddle.x_cord
        relative_y = self.ball.y_cord - self.paddle.y_cord
        # brick_layout = [1 if brick.rect is not None else 0 for brick in self.bricks]
        # brick_layout = len(self.bricks)
        # ball_reset_flag = 1 if self.ball.x_cord == self.ball.x_start and self.ball.y_cord == self.ball.y_start else 0

        obs = np.array([paddle_location] + ball_location + ball_velocity + [relative_x, relative_y], dtype=np.float32)

        return obs

    def render(self, mode='human'):
        if self.screen is None:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # draw black background
        self.screen.fill((0, 0, 0))

        # draw paddle, ball, and brick objects to screen
        pygame.draw.rect(self.screen, self.paddle.color, self.paddle.rect)
        pygame.draw.circle(self.screen, self.ball.color, (self.ball.x_cord, self.ball.y_cord), self.ball.radius)
        for brick in self.bricks:
            pygame.draw.rect(self.screen, brick.color, brick.rect)

        # update the display
        pygame.display.update()

    def get_score(self):
        return self.stats.score
