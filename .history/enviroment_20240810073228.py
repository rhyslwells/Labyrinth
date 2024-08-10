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

# Example usage:
env = Environment(10, 10)

# Add some obstacles
env.add_obstacle((3, 3))
env.add_obstacle((3, 4))
env.add_obstacle((3, 5))

# Set the exit point
env.set_exit((9, 9))

# Place the hunter (represented by 3) and prey (represented by 4)
env.place_actor((0, 0), 3)  # Hunter starts at top-left
env.place_actor((1, 1), 4)  # Prey starts at (1, 1)

# Display the grid
print("ttt")
env.display()
