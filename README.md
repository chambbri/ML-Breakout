# ML-Breakout
This project creates a replica of Atari's Breakout with a reinforcement learning agent designed to play the game.

## About this project
Breakout was created using Pygame and classes to represent all objects necessary to play Breakout.
The reinforcement learning environment was set up using OpenAI's Gym, providing the RL agent information about environment variables such as paddle/ball position and ball velocity.
Iterative training is performed using a model created with Pytorch.

## Still to do
The current focus on this project is to get the RL agent to consistently create paddle/ball collisions as it transitions from exploration to exploitation. Parameter tuning, environment feedback, and model adjustments are still being performed to accomplish this. Once this is completed, focus will transition to adding bricks into the environment variables so the agent can focus on eliminating bricks to win the game.

Once the agent is performing satisfactorly, a function will be added for a human player to compete against the RL agent.
