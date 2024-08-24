import os
import pandas as pd
from PIL import Image
import numpy as np
import pygame
import gym
from typing import Tuple, Optional, Union

# Define constants for directions and other configurations
UP = np.array([0, -1])
RIGHT = np.array([1, 0])
DOWN = np.array([0, 1])
LEFT = np.array([-1, 0])
NO_OP = np.array([0, 0])

WIDTH, HEIGHT = 800, 800
BLACK = (0, 0, 0)
FPS = 60


# Game class integrating environment, actor, and gameplay logic
class Game:
    (self, name, width, height, obstacles, exit_point, actor_start_position, predefined_moves)
    def __init__(self, name, world='7x7-simple', delay=0):
        self.name = name
        self.delay = delay
        self._load_environment(world)
        self._init_rendering()

        # Initialize the DataFrame to record actor's position and in-game time at each step
        self.data = pd.DataFrame(columns=['Time', 'x_coord', 'y_coord'])

    def _load_environment(self, world):
        file = open(f"Actorworld_assets/Actorworld_maps/{world}.csv")
        env = np.loadtxt(file, delimiter=';', dtype=object)
        base_shape = env.shape

        walls = np.array(['w' for _ in range(base_shape[0])])
        env = np.c_[env, walls]
        env = np.c_[walls, env]
        walls = np.array([['w' for _ in range(base_shape[1] + 2)]])
        env = np.r_[env, walls]
        env = np.r_[walls, env]

        self.env = env.T
        self._setup_observation_table()

        start_pos = np.where(env == 's')
        self.start_pos = np.array([int(start_pos[0]), int(start_pos[1])])
        end_pos = np.where(env == 't')
        self.end_pos = np.array([int(end_pos[0]), int(end_pos[1])])

        self.actor = Actor(position=self.start_pos, environment=self.env)
        self.current_pos = self.start_pos

        self.observation_space = gym.spaces.Discrete(len(self.observation_table))
        self.action_space = gym.spaces.Discrete(5)
        self.action_table = {0: NO_OP, 1: LEFT, 2: RIGHT, 3: UP, 4: DOWN}

    def _setup_observation_table(self):
        state_counter = 0
        self.observation_table = {}
        for x, row in enumerate(self.env):
            for y, col in enumerate(row):
                if col != 'w':
                    self.observation_table[(x, y)] = state_counter
                    state_counter += 1

    def _init_rendering(self):
        sprite_dims_x = int(WIDTH / self.env.shape[0])
        sprite_dims_y = int(HEIGHT / self.env.shape[1])

        # Define sprites as solid colors instead of image paths for simplicity
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

        self.sprite_dims_x = sprite_dims_x
        self.sprite_dims_y = sprite_dims_y

        self.render_mode = False
        self.window = None
        self.clock = None

    def reset(self):
        if self.render_mode:
            pygame.time.wait(self.delay)
        self.current_pos = self.start_pos
        return self.observation_table[tuple(self.current_pos)]

    def render(self, mode="human"):
        self.render_mode = True
        if self.window is None:
            pygame.init()
            self.window = pygame.display.set_mode((WIDTH, HEIGHT))
            self.clock = pygame.time.Clock()

        self.window.fill(BLACK)
        for x, row in enumerate(self.env):
            for y, col in enumerate(row):
                sprite_to_draw = self.GROUND_SPRITE
                if col == 'w':
                    sprite_to_draw = self.WALL_SPRITE
                elif col == 's':
                    sprite_to_draw = self.START_SPRITE
                elif col == 't':
                    sprite_to_draw = self.GOAL_SPRITE
                self.window.blit(sprite_to_draw, (x * self.sprite_dims_x, y * self.sprite_dims_y))

        self.window.blit(self.Actor_SPRITE, (self.current_pos[0] * self.sprite_dims_x, self.current_pos[1] * self.sprite_dims_y))
        self.clock.tick(FPS)
        pygame.display.flip()

    def step(self, action: int) -> Tuple[int, float, bool, dict]:
        action = self.action_table[action]
        next_pos = self.current_pos + action

        if self.env[tuple(next_pos)] != 'w':
            self.current_pos = next_pos

        reward = -1
        done = False

        if (self.current_pos == self.end_pos).all():
            reward = 0
            done = True

        current_state = self.observation_table[tuple(self.current_pos)]
        if self.render_mode:
            pygame.time.wait(self.delay)
        return current_state, reward, done, {}

    def sample(self):
        return self.action_space.sample()

    def save_initial_state(self, save_images=True):
        self.env[self.start_pos[1], self.start_pos[0]] = 'A'
        if save_images:
            self._save_grid_to_image(f"gif_data/{self.name}_step_0.png")
        self.record_step(0)

    def record_step(self, step):
        x, y = self.current_pos
        new_data = pd.DataFrame({
            'Time': [step],
            'x_coord': [int(x)],
            'y_coord': [int(y)]
        })
        self.data = pd.concat([self.data, new_data], ignore_index=True)

    def simulate(self, save_images=True):
        for step in range(1, len(self.actor.predefined_moves) + 1):
            self.env[self.actor.position[1], self.actor.position[0]] = '.'
            self.actor.step()
            self.env[self.actor.position[1], self.actor.position[0]] = 'A'
            if save_images:
                self._save_grid_to_image(f"gif_data/{self.name}_step_{step}.png")
            self.record_step(step)

    def create_gif(self):
        num_steps = len(self.actor.predefined_moves) + 1
        images = [Image.open(f"gif_data/{self.name}_step_{i}.png") for i in range(num_steps)]
        gif_filename = f"gif_data/{self.name}.gif"
        images[0].save(gif_filename, save_all=True, append_images=images[1:], duration=500, loop=0)

        for i in range(num_steps):
            os.remove(f"gif_data/{self.name}_step_{i}.png")

    def save_dataframe(self, filename):
        self.data.to_csv(filename, index=False)

    def _save_grid_to_image(self, filename):
        color_map = {
            'w': (0, 0, 0),   # Black for walls
            '.': (255, 255, 255),  # White for empty spaces
            's': (0, 255, 0),  # Green for start
            't': (255, 0, 0),  # Red for goal
            'A': (0, 0, 255)   # Blue for actor
        }
        cell_size = 20
        image_data = np.zeros((self.env.shape[1] * cell_size, self.env.shape[0] * cell_size, 3), dtype=np.uint8)
        
        for y in range(self.env.shape[1]):
            for x in range(self.env.shape[0]):
                color = color_map.get(self.env[y, x], (255, 255, 255))
                image_data[y * cell_size:(y + 1) * cell_size, x * cell_size:(x + 1) * cell_size] = color
        
        img = Image.fromarray(image_data)
