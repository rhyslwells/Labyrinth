import os
import pandas as pd
from PIL import Image
from src.actors.actor import Actor
from environment import Environment

class Game:
    def __init__(self, name, width, height, obstacles, exit_point, actor_start_position, predefined_moves):
        self.name = name
        self.environment = Environment(width, height)
        
        # Add obstacles
        for obstacle in obstacles:
            self.environment.add_obstacle(obstacle)
        
        # Set exit point
        self.environment.set_exit(exit_point)
        
        # Create an actor
        self.actor = Actor(position=actor_start_position, environment=self.environment)
        
        # Set predefined moves for the actor
        self.actor.set_predefined_moves(predefined_moves)
        
        # Ensure gif_data directory exists
        os.makedirs('gif_data', exist_ok=True)
        
        # Initialize the DataFrame to record actor's position and in-game time at each step
        self.data = pd.DataFrame(columns=['Time', 'x_coord', 'y_coord'])
    
    def save_initial_state(self,save_images=True):
        """Save the initial state of the environment."""
        self.environment.place_actor(self.actor.position, "A")
        if save_images:
            self.environment.save_to_image(f"gif_data/{self.name}_step_0.png")
        
        # Record the initial state
        self.record_step(0)

    
    def record_step(self, step):
        """Record the current step, actor's position, and in-game time."""
        x, y = self.actor.position
        new_data = pd.DataFrame({
            'Time': [step],  # In-game time is the step number
            'x_coord': [int(x)],
            'y_coord': [int(y)]
        })
        self.data = pd.concat([self.data, new_data], ignore_index=True)
    
    def simulate(self, save_images=True):
        """Simulate the actor's movement and optionally save images for each step."""
        predefined_moves = self.actor.predefined_moves
        
        for step in range(1, len(predefined_moves) + 1):
            # print(f"\nStep {step}:")
            
            # Clear the previous actor position
            self.environment.grid[self.actor.position[1], self.actor.position[0]] = '.'
            
            # Actor takes a step
            self.actor.step()
            
            # Place the actor's new position on the grid
            self.environment.place_actor(self.actor.position, "A")
            
            # Save the image only if save_images is True
            if save_images:
                self.environment.save_to_image(f"gif_data/{self.name}_step_{step}.png")
            
            # Record the current step
            self.record_step(step)
    
    def create_gif(self):
        """Create a GIF from the saved images and remove the PNG files."""
        # First, simulate the game with image saving enabled
        # self.simulate(save_images=True)
        
        num_steps = len(self.actor.predefined_moves) + 1
        print(f"Creating GIF with {num_steps} steps...")
        images = [Image.open(f"gif_data/{self.name}_step_{i}.png") for i in range(num_steps)]
        gif_filename = f"gif_data/{self.name}.gif"
        
        # Save the GIF
        images[0].save(gif_filename, save_all=True, append_images=images[1:], duration=500, loop=0)
        print(f"GIF saved as {gif_filename}.")
        
        # Remove the PNG files
        for i in range(num_steps):
            os.remove(f"gif_data/{self.name}_step_{i}.png")
        print("PNG files removed.")
    
    def save_dataframe(self, filename):
        """Save the recorded DataFrame to a CSV file."""
        self.data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")


Enviorment class will be incorporated in the game class.

import numpy as np
from PIL import Image

class Environment:
    def __init__(self, width, height):
        # Initialize a grid of given width and height filled with '.' (empty cells)
        self.width = width
        self.height = height
        self.grid = np.full((height, width), '.', dtype=str)

        # Add obstacles around the perimeter
        self.add_perimeter_obstacles()

    def add_perimeter_obstacles(self):
        """Add obstacles around the perimeter of the grid."""
        for x in range(self.width):
            self.grid[0, x] = '#'  # Top row
            self.grid[self.height - 1, x] = '#'  # Bottom row

        for y in range(self.height):
            self.grid[y, 0] = '#'  # Left column
            self.grid[y, self.width - 1] = '#'  # Right column

    def add_obstacle(self, position):
        """Add an obstacle to the grid at the specified position."""
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = '#'  # Use # to represent an obstacle

    def set_exit(self, position):
        """Set the exit point at the specified position."""
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = 'E'  # Use E to represent the exit

    def place_actor(self, position, actor_id):
        """Place an actor on the grid (e.g., hunter, prey)."""
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = actor_id  # Use a character to represent the actor

    def display(self):
        """Display the grid in a human-readable format."""
        for row in self.grid:
            print(" ".join(row))

    def save_to_image(self, filename):
        color_map = {
            '.': (255, 255, 255),  # White for empty space
            '#': (0, 0, 0),       # Black for obstacles
            'E': (255, 0, 0),     # Red for exit
            'A': (0, 255, 0)      # Green for actor
        }
        cell_size = 20  # Size of each cell in pixels
        image_data = np.zeros((self.height * cell_size, self.width * cell_size, 3), dtype=np.uint8)
        
        for y in range(self.height):
            for x in range(self.width):
                color = color_map.get(self.grid[y, x], (255, 255, 255))  # Default to white if color not found
                image_data[y * cell_size:(y + 1) * cell_size, x * cell_size:(x + 1) * cell_size] = color
        
        img = Image.fromarray(image_data)
        img.save(filename)
        print(f"Saved image to {filename}")


import numpy as np
import pygame
from typing import Tuple, Optional, Union
import pathlib
import gym
from gym.core import ActType, ObsType

UP = np.array([0, -1])
RIGHT = np.array([1, 0])
DOWN = np.array([0, 1])
LEFT = np.array([-1, 0])
NO_OP = np.array([0, 0])

WIDTH, HEIGHT = 800, 800
BLACK = (0, 0, 0)
FPS = 60
CURRENT_PATH = pathlib.Path(__file__).parent.absolute()
ground_tile_path = CURRENT_PATH/"gregworld_assets/sprites/ground_tile.png"
wall_tile_path = CURRENT_PATH/"gregworld_assets/sprites/wall_tile.png"
start_tile_path = CURRENT_PATH/"gregworld_assets/sprites/start_tile.png"
goal_tile_path = CURRENT_PATH/"gregworld_assets/sprites/goal_tile.png"
greg_tile_path = CURRENT_PATH/"gregworld_assets/sprites/greg.png"


class GregWorld(gym.Env):

    def __init__(self, world='7x7-simple', delay=0):

        file = open(CURRENT_PATH/f"gregworld_assets/gregworld_maps/{world}.csv")
        env = np.loadtxt(file, delimiter=';', dtype=object)
        base_shape = env.shape

        walls = np.array(['w' for _ in range(base_shape[0])])

        env = np.c_[env, walls]
        env = np.c_[walls, env]

        walls = np.array([['w' for _ in range(base_shape[1] + 2)]])

        env = np.r_[env, walls]
        env = np.r_[walls, env]

        self.env = env.T

        state_counter = 0
        self.observation_table = dict()

        for x, row in enumerate(env):
            for y, col in enumerate(row):
                if col != 'w':
                    self.observation_table[(x, y)] = state_counter
                    state_counter += 1

        start_pos = np.where(env == 's')
        start_pos = int(start_pos[0]), int(start_pos[1])
        end_pos = np.where(env == 't')
        end_pos = int(end_pos[0]), int(end_pos[1])

        self.start_pos = np.array(start_pos)
        self.end_pos = np.array(end_pos)

        self.current_pos = start_pos

        self.observation_space = gym.spaces.Discrete(len(self.observation_table))
        self.action_space = gym.spaces.Discrete(5)

        self.action_table = {
            0: NO_OP,
            1: LEFT,
            2: RIGHT,
            3: UP,
            4: DOWN
        }

        # Rendering configuration
        self.delay = delay
        sprite_dims_x = int(WIDTH / self.env.shape[0])
        sprite_dims_y = int(HEIGHT / self.env.shape[1])

        self.GROUND_SPRITE = pygame.transform.scale(pygame.image.load(ground_tile_path), (sprite_dims_x, sprite_dims_y))
        self.WALL_SPRITE = pygame.transform.scale(pygame.image.load(wall_tile_path), (sprite_dims_x, sprite_dims_y))
        self.START_SPRITE = pygame.transform.scale(pygame.image.load(start_tile_path), (sprite_dims_x, sprite_dims_y))
        self.GOAL_SPRITE = pygame.transform.scale(pygame.image.load(goal_tile_path), (sprite_dims_x, sprite_dims_y))
        self.GREG = pygame.transform.scale(pygame.image.load(greg_tile_path), (sprite_dims_x, sprite_dims_y))

        self.sprite_dims_x = sprite_dims_x
        self.sprite_dims_y = sprite_dims_y

        self.render_mode = False
        self.window = None
        self.clock = None

    def reset(self, *, seed: Optional[int] = None, return_info: bool = False, options: Optional[dict] = None) -> Union[ObsType, tuple[ObsType, dict]]:
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
        events = pygame.event.get()

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

        self.window.blit(self.GREG, (self.current_pos[0] * self.sprite_dims_x, self.current_pos[1] * self.sprite_dims_y))
        self.clock.tick(FPS)

        pygame.display.flip()
        return events

    def step(self, action: ActType) -> Tuple[ObsType, float, bool, dict]:

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