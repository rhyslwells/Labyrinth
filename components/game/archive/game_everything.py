import os
import pandas as pd
from PIL import Image
import numpy as np
import pygame
import gymnasium as gym
from typing import Tuple, Dict
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from components.actors.actor import Actor


WIDTH, HEIGHT = 800, 800
BLACK = (0, 0, 0)
FPS = 60

class Game(gym.Env):
    def __init__(self, name: str, world: str = '7x7-simple', delay: int = 0):
        super().__init__()
        self.name = name
        self.delay = delay
        self._load_environment(world)
        self._init_rendering()
        self.data = pd.DataFrame(columns=['Time', 'x_coord', 'y_coord'])
        self.metrics = {'success_rate': 0, 'average_time': 0}
        self.actor = None  # Initialize actor here

    def _load_environment(self, world: str):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, 'environments', f'{world}.csv')
        env = np.loadtxt(file_path, delimiter=';', dtype=object)
        base_shape = env.shape

        walls = np.array(['w'] * base_shape[0])
        env = np.c_[env, walls]
        env = np.c_[walls, env]
        walls = np.array([['w'] * (base_shape[1] + 2)])
        env = np.r_[env, walls]
        env = np.r_[walls, env]

        self.grid = env.T
        self._setup_observation_table()

        start_pos = np.where(env == 's')
        self.start_pos = np.array([int(start_pos[0]), int(start_pos[1])])
        end_pos = np.where(env == 't')
        self.end_pos = np.array([int(end_pos[0]), int(end_pos[1])])

        self.actor = Actor(position=self.start_pos, environment=self)

        self.observation_space = gym.spaces.Discrete(len(self.observation_table))
        self.action_space = gym.spaces.Discrete(5)
        # Define constants
        UP = np.array([0, -1])
        RIGHT = np.array([1, 0])
        DOWN = np.array([0, 1])
        LEFT = np.array([-1, 0])
        NO_OP = np.array([0, 0])
        self.action_table = {0: NO_OP, 1: LEFT, 2: RIGHT, 3: UP, 4: DOWN}

    def _setup_observation_table(self):
        state_counter = 0
        self.observation_table = {}
        for x, row in enumerate(self.grid):
            for y, col in enumerate(row):
                if col != 'w':
                    self.observation_table[(x, y)] = state_counter
                    state_counter += 1

    def _init_rendering(self):
        sprite_dims_x = WIDTH // self.grid.shape[0]
        sprite_dims_y = HEIGHT // self.grid.shape[1]

        self.GROUND_SPRITE = pygame.Surface((sprite_dims_x, sprite_dims_y))
        self.GROUND_SPRITE.fill((255, 255, 255))  # White

        self.WALL_SPRITE = pygame.Surface((sprite_dims_x, sprite_dims_y))
        self.WALL_SPRITE.fill((0, 0, 0))  # Black

        self.START_SPRITE = pygame.Surface((sprite_dims_x, sprite_dims_y))
        self.START_SPRITE.fill((0, 255, 0))  # Green

        self.GOAL_SPRITE = pygame.Surface((sprite_dims_x, sprite_dims_y))
        self.GOAL_SPRITE.fill((255, 0, 0))  # Red

        self.Actor_SPRITE = pygame.Surface((sprite_dims_x, sprite_dims_y))
        self.Actor_SPRITE.fill((0, 0, 255))  # Blue

        self.render_mode = False
        self.window = None
        self.clock = None
    
    def reset(self):
        if self.render_mode:
            pygame.time.wait(self.delay)
        self.actor.position = self.start_pos
        return self.observation_table[tuple(self.actor.position)]

    def render(self, mode="human"):
        self.render_mode = True
        if self.window is None:
            pygame.init()
            self.window = pygame.display.set_mode((WIDTH, HEIGHT))
            self.clock = pygame.time.Clock()

        self.window.fill(BLACK)
        for x, row in enumerate(self.grid):
            for y, col in enumerate(row):
                sprite_to_draw = self.GROUND_SPRITE
                if col == 'w':
                    sprite_to_draw = self.WALL_SPRITE
                elif col == 's':
                    sprite_to_draw = self.START_SPRITE
                elif col == 't':
                    sprite_to_draw = self.GOAL_SPRITE
                self.window.blit(sprite_to_draw, (x * (WIDTH // self.grid.shape[0]), y * (HEIGHT // self.grid.shape[1])))

        self.window.blit(self.Actor_SPRITE, (self.actor.position[0] * (WIDTH // self.grid.shape[0]), self.actor.position[1] * (HEIGHT // self.grid.shape[1])))
        self.clock.tick(FPS)
        pygame.display.flip()

    def step(self, action: int) -> Tuple[int, float, bool, Dict]:
        action = self.action_table[action]
        self.actor.set_predefined_moves(action)
        self.actor.step()

        reward = -1
        done = False

        if np.array_equal(self.actor.position, self.end_pos):
            reward = 0
            done = True

        current_state = self.observation_table[tuple(self.actor.position)]
        if self.render_mode:
            pygame.time.wait(self.delay)
        return current_state, reward, done, {}

    def sample(self):
        return self.action_space.sample()
    
    def save_initial_state(self, save_images=True):
        self.grid[self.start_pos[1], self.start_pos[0]] = 'A'
        if save_images:
            self._save_grid_to_image(f"gif_data/{self.name}_step_0.png")
        self.record_step(0)

    def record_step(self, step):
        x, y = self.actor.position
        new_data = pd.DataFrame({
            'Time': [step],
            'x_coord': [int(x)],
            'y_coord': [int(y)]
        })
        self.data = pd.concat([self.data, new_data], ignore_index=True)

    def game_loop(self, max_steps: int):
        step = 0
        self.reset()
        while step < max_steps:
            action = self.sample()  # Replace with actual policy if needed
            state, reward, done, _ = self.step(action)
            self.render()
            self.record_step(step)
            if done:
                break
            step += 1
        self.calculate_metrics(step)

    def calculate_metrics(self, steps: int):
        success = self.actor.position.tolist() == self.end_pos.tolist()
        self.metrics['success_rate'] = 1 if success else 0
        self.metrics['average_time'] = steps  # Adjust calculation as needed

    def save_metrics(self, filename: str):
        metrics_df = pd.DataFrame([self.metrics])
        metrics_df.to_csv(filename, index=False)

    def visualize_grid(self):
        fig, ax = plt.subplots()
        color_map = {'w': 'black', '.': 'white', 's': 'green', 't': 'red', 'A': 'blue'}
        c = np.vectorize(lambda x: color_map.get(x, 'white'))(self.grid)
        ax.imshow(c, interpolation='none')
        plt.title('Grid Visualization')
        plt.show()

    def animate_game(self, frames: int):
        fig, ax = plt.subplots()
        ims = []

        for step in range(frames):
            self._save_grid_to_image(f"gif_data/{self.name}_step_{step}.png")
            img = Image.open(f"gif_data/{self.name}_step_{step}.png")
            im = ax.imshow(img, animated=True)
            ims.append([im])

        ani = animation.ArtistAnimation(fig, ims, interval=500, blit=True, repeat_delay=1000)
        ani.save(f"gif_data/{self.name}.gif")

        for step in range(frames):
            os.remove(f"gif_data/{self.name}_step_{step}.png")

    def _save_grid_to_image(self, filename: str):
        color_map = {
            'w': (0, 0, 0),   # Black for walls
            '.': (255, 255, 255),  # White for empty spaces
            's': (0, 255, 0),  # Green for start
            't': (255, 0, 0),  # Red for goal
            'A': (0, 0, 255)   # Blue for actor
        }
        cell_size = 20
        image_data = np.zeros((self.grid.shape[1] * cell_size, self.grid.shape[0] * cell_size, 3), dtype=np.uint8)
        
        for y in range(self.grid.shape[1]):
            for x in range(self.grid.shape[0]):
                color = color_map.get(self.grid[y, x], (255, 255, 255))
                image_data[y * cell_size:(y + 1) * cell_size, x * cell_size:(x + 1) * cell_size] = color
        
        img = Image.fromarray(image_data)
        img.save(filename)
