import gym
import numpy as np
import pygame

from ..BreakoutGame.stats import Stats
from ..BreakoutGame.game import create_paddle, create_ball, create_bricks, paddle_collision, wall_collision, \
    brick_collision, life_lost

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
        return self._get_obs()

    def step(self, action):
        done = False
        reward = 0
        prev_score = self.stats.score

        self.ball.move_ball(SCREEN_HEIGHT)
        self.paddle.move_paddle(0, SCREEN_WIDTH, action, "agent")
        paddle_col = paddle_collision(self.paddle, self.ball)
        brick_collision(self.ball, self.bricks, self.stats)
        wall_collision(self.ball)
        if paddle_col:
            reward += 1
        new_score = self.stats.score
        reward += new_score - prev_score

        lost = life_lost(self.ball, self.stats)

        if lost:
            reward -= 10

        if len(self.bricks) == 0:
            reward += 20
            done = True

        if self.stats.lives == 0:
            reward -= 20
            done = True

        observation = self._get_obs()

        return observation, reward, done

    def _get_obs(self):
        paddle_location = self.paddle.x_cord
        ball_location = [self.ball.x_cord, self.ball.y_cord]
        ball_velocity = [self.ball.x_speed, self.ball.y_speed]
        brick_layout = [1 if brick.rect is not None else 0 for brick in self.bricks]

        obs = np.array([paddle_location] + ball_location + ball_velocity + brick_layout, dtype=np.float32)

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


env = BreakoutEnv()
obs = env.reset()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            env.close()
            exit()
    action = env.action_space.sample()
    obs, rward, finished = env.step(action)

    env.render()

    if finished:
        break

env.close()
