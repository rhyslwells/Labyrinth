# game.py
import gymnasium as gym
import numpy as np
from components.actors.actor import Actor
from components.environment_manager import EnvironmentManager
from components.renderer import Renderer
from components.data_handler import DataHandler

class Game(gym.Env):
    def __init__(self, name: str, world: str = '7x7-simple', delay: int = 0):
        super().__init__()
        self.name = name
        self.delay = delay
        self.env_manager = EnvironmentManager(world)
        self.renderer = Renderer(self.env_manager.grid, None, delay)
        self.data_handler = DataHandler()
        self.actor = Actor(position=self.env_manager.start_pos, environment=self.env_manager)
        self.renderer.actor = self.actor

        self.observation_space = gym.spaces.Discrete(len(self.env_manager.observation_table))
        self.action_space = gym.spaces.Discrete(5)
        UP = np.array([0, -1])
        RIGHT = np.array([1, 0])
        DOWN = np.array([0, 1])
        LEFT = np.array([-1, 0])
        NO_OP = np.array([0, 0])
        self.action_table = {0: NO_OP, 1: LEFT, 2: RIGHT, 3: UP, 4: DOWN}

    def reset(self):
        if self.renderer.render_mode:
            pygame.time.wait(self.delay)
        self.actor.position = self.env_manager.start_pos
        return self.env_manager.observation_table[tuple(self.actor.position)]

    def step(self, action: int) -> Tuple[int, float, bool, Dict]:
        action = self.action_table[action]
        self.actor.set_predefined_moves(action)
        self.actor.step()

        reward = -1
        done = False

        if np.array_equal(self.actor.position, self.env_manager.end_pos):
            reward = 0
            done = True

        current_state = self.env_manager.observation_table[tuple(self.actor.position)]
        if self.renderer.render_mode:
            pygame.time.wait(self.delay)
        return current_state, reward, done, {}

    def sample(self):
        return self.action_space.sample()
    
    def save_initial_state(self, save_images=True):
        self.env_manager.grid[self.env_manager.start_pos[1], self.env_manager.start_pos[0]] = 'A'
        if save_images:
            self.renderer.save_grid_to_image(f"gif_data/{self.name}_step_0.png")
        self.data_handler.record_step(self.actor.position, 0)

    def game_loop(self, max_steps: int):
        step = 0
        self.reset()
        while step < max_steps:
            action = self.sample() 
