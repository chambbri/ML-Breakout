from GymBreakout.breakout_env import BreakoutEnv
from collections import deque
import torch
import matplotlib.pyplot as plt
import random
import numpy as np
from MLAgent.model import NN, QTrainer

MAX_MEMORY = 10000
BATCH_SIZE = 32
LR = 0.001


class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.99
        self.env = BreakoutEnv()
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = NN(9, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.state_mean = 0
        self.state_std = 1e-5  # Small value to avoid division by zero

    def normalize_state(self, state):
        paddle_x, ball_x, ball_y, ball_x_speed, ball_y_speed, brick_layout, \
            relative_x, relative_y, ball_reset_flag = state
        max_screen_width = 1260
        max_screen_height = 600

        paddle_x /= max_screen_width
        ball_x /= max_screen_width
        ball_y /= max_screen_height

        relative_x = max_screen_width
        relative_y = max_screen_height

        max_bricks = 77
        brick_layout /= max_bricks
        return np.array([paddle_x, ball_x, ball_y, ball_x_speed, ball_y_speed, relative_x, relative_y,
                         brick_layout, ball_reset_flag], dtype=np.float32)

    def get_state(self):
        state = self.env.get_obs()
        return self.normalize_state(state)

    def add_to_memory(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        if len(mini_sample) > 1:
            states, actions, rewards, next_states, dones = zip(*mini_sample)
            self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: exploration vs exploitation
        self.epsilon = max(0.01, 0.995 ** self.n_games)
        if random.random() < self.epsilon:
            final_move = random.randint(0, 2)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            final_move = torch.argmax(prediction).item()

        return final_move


def train():
    scores = []
    mean_scores = []
    total_score = 0
    record = 0
    total_reward = 0
    agent = Agent()
    env = agent.env
    env.reset()

    # plt.ion()
    # fig, ax = plt.subplots()

    max_games = 2000

    with open("game_scores.txt", "w") as file:
        file.write("Game, Score, Total Reward, Record")
        while agent.n_games < max_games:
            # if agent.n_games > 500:
            #    env.render()
            state = agent.get_state()
            action = agent.get_action(state)
            new_state, reward, done = env.step(action)
            total_reward += reward

            agent.train_short_memory(state, action, reward, new_state, done)
            agent.add_to_memory(state, action, reward, new_state, done)

            if done:
                score = env.stats.score
                env.reset()
                agent.n_games += 1
                agent.train_long_memory()

                if score > record:
                    record = score
                    agent.model.save()

                file.write(f"{agent.n_games}, {score}, {total_reward}, {record}\n")
                print('Game', agent.n_games, 'Score', score, 'Record', record, 'Reward', total_reward)

                total_reward = 0
                scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                mean_scores.append(mean_score)
            """
                ax.clear()
                ax.plot(scores, label="Score")
                ax.plot(mean_scores, label="Mean Score")
                ax.set_xlabel("Episode")
                ax.set_ylabel("Score")
                ax.set_title("Agent Score and Mean Score Over Time")
                ax.legend()
    
                plt.pause(0.001)
            """

    print(f"Training completed after {max_games} games.")
    print(f"Final Record: {record}")
    print(f"Mean score after {max_games} games: {mean_score}")


if __name__ == '__main__':
    train()