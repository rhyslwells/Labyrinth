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