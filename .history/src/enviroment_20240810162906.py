import numpy as np

class Environment:
    def __init__(self, width, height):
        # Initialize a grid of given width and height filled with 0 (empty cells)
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        
    def add_obstacle(self, position):
        """Add an obstacle to the grid at the specified position."""
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = 1  # Use 1 to represent an obstacle

    def set_exit(self, position):
        """Set the exit point at the specified position."""
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = 2  # Use 2 to represent the exit

    def place_actor(self, position, actor_id):
        """Place an actor on the grid (e.g., hunter, prey)."""
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = actor_id  # Use a unique number for each actor

    def display(self):
        """Display the grid in a human-readable format."""
        symbols = {0: '.', 1: '#', 2: 'E'}  # . for empty, # for obstacle, E for exit
        for row in self.grid:
            print(" ".join(symbols.get(cell, str(cell)) for cell in row))
        print()