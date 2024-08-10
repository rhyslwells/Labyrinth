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

# Example useage of the Environment class

# # Example usage:
# env = Environment(10, 10)

# # Add some obstacles
# env.add_obstacle((3, 3))
# env.add_obstacle((3, 4))
# env.add_obstacle((3, 5))

# # Set the exit point
# env.set_exit((9, 9))

# # Place the hunter (represented by 3) and prey (represented by 4)
# env.place_actor((0, 0), 3)  # Hunter starts at top-left
# env.place_actor((1, 1), 4)  # Prey starts at (1, 1)

# # Display the grid
# env.display()


import random

import random

class Actor:
    def __init__(self, position, speed=1):
        """
        Initialize the actor with a starting position and speed.
        
        :param position: Tuple (x, y) representing the actor's position.
        :param speed: Maximum speed the actor can move per time step.
        """
        self.position = position
        self.speed = speed  # Maximum number of cells the actor can move in one time step
        self.predefined_moves = []  # Store predefined moves here
        self.current_move_index = 0

    def move(self, direction):
        """
        Move the actor in the specified direction.
        
        :param direction: Tuple (dx, dy) representing the direction to move.
        """
        new_x = self.position[0] + direction[0] * self.speed
        new_y = self.position[1] + direction[1] * self.speed
        self.position = (new_x, new_y)

    def scan(self, environment):
        """
        Scan the environment to determine nearby obstacles, exit, or other actors.
        
        :param environment: The 2D grid representing the environment.
        :return: A dictionary with details about the surroundings.
        """
        x, y = self.position
        surroundings = {
            'up': environment.grid[y-1][x] if y > 0 else None,
            'down': environment.grid[y+1][x] if y < environment.height - 1 else None,
            'left': environment.grid[y][x-1] if x > 0 else None,
            'right': environment.grid[y][x+1] if x < environment.width - 1 else None,
        }
        return surroundings

    def make_decision(self, environment):
        """
        Decide on the next move based on the surroundings or predefined moves.
        
        :param environment: The 2D grid representing the environment.
        :return: The chosen direction as a tuple (dx, dy).
        """
        if self.predefined_moves and self.current_move_index < len(self.predefined_moves):
            # Use the predefined move if available
            direction = self.predefined_moves[self.current_move_index]
            self.current_move_index += 1
            return direction
        
        # If no predefined moves, fall back to random movement
        directions = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }
        possible_directions = [dir for dir, pos in self.scan(environment).items() if pos is not None and pos != 1]
        
        if not possible_directions:
            return (0, 0)  # No valid move, stay in place
        
        chosen_direction = random.choice(possible_directions)
        return directions[chosen_direction]

    def step(self, environment):
        """
        Perform one time step in the environment, scanning, deciding, and moving.
        
        :param environment: The 2D grid representing the environment.
        """
        direction = self.make_decision(environment)
        self.move(direction)

    def set_predefined_moves(self, moves):
        """
        Set a sequence of predefined moves for the actor.
        
        :param moves: List of tuples representing the moves (e.g., [(1, 0), (0, 1), (-1, 0)]).
        """
        self.predefined_moves = moves
        self.current_move_index = 0  # Reset the index when setting new moves


# Example usage of the Actor class:

# With random movements:

# env = Environment(5, 5)
# env.add_obstacle((3, 3))
# env.set_exit((5,5))

# print("Initial grid:")
# env.display()
# print("-----------------")

# # Create an actor
# actor = Actor(position=(0, 0))

# # Run a few steps and display the grid
# for step in range(5):
#     print(f"Step {step + 1}:")
    
#     # Clear the previous actor position (for visual clarity)
#     env.grid[actor.position[1], actor.position[0]] = 0
    
#     # Actor takes a step
#     actor.step(env)
    
#     # Place the actor's new position on the grid and display it
#     env.place_actor(actor.position, 3)  # Use 3 to represent the actor
#     env.display()

# Example usage with predefined moves:

env = Environment(10, 10)
env.add_obstacle((3, 3))
env.set_exit((9, 9))

print("Initial grid:")
env.display()

# Create an actor
actor = Actor(position=(0, 0))

# Set predefined moves: right, down, right, down
actor.set_predefined_moves([(1, 0), (1,0, (1, 0), (0, 1)])

# Run a few steps and display the grid
for step in range(5):
    print(f"Step {step + 1}:")
    
    # Clear the previous actor position (for visual clarity)
    env.grid[actor.position[1], actor.position[0]] = 0
    
    # Actor takes a step
    actor.step(env)
    
    # Place the actor's new position on the grid and display it
    env.place_actor(actor.position, 3)  # Use 3 to represent the actor
    env.display()
