import numpy as np

class Environment:
    def __init__(self, width, height):
        # Initialize a grid of given width and height filled with '.' (empty cells)
        self.width = width
        self.height = height
        self.grid = np.full((height, width), '.', dtype=str)
        
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