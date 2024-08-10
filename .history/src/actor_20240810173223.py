import random

class Actor:
    def __init__(self, position, speed=1):
        """
        Initialize the actor with a starting position and speed.
        
        :param position: Tuple (x, y) representing the actor's position.
        :param speed: Maximum number of cells the actor can move per time step.
        """
        self.position = position
        self.speed = speed
        self.predefined_moves = []  # Store predefined moves here
        self.current_move_index = 0

        # Define the mapping for the directions
        self.direction_map = {
            'U': (0, -1),  # Up
            'D': (0, 1),   # Down
            'L': (-1, 0),  # Left
            'R': (1, 0)    # Right
        }

    def scan(self, environment):
        """
        Scan the environment to determine nearby obstacles, exit, or other actors.
        
        :param environment: The 2D grid representing the environment.
        :return: A dictionary with details about the surroundings.
        """
        x, y = self.position
        surroundings = {
            'U': environment.grid[y-1][x] if y > 0 else None,       # Up
            'D': environment.grid[y+1][x] if y < environment.height - 1 else None,  # Down
            'L': environment.grid[y][x-1] if x > 0 else None,       # Left
            'R': environment.grid[y][x+1] if x < environment.width - 1 else None   # Right
        }
        return surroundings

    def make_decision(self, environment):
        """
        Decide on the next move based on predefined moves and check for obstacles.
        
        :param environment: The 2D grid representing the environment.
        :return: The chosen direction as a tuple (dx, dy).
        """
        if self.predefined_moves and self.current_move_index < len(self.predefined_moves):
            direction_char = self.predefined_moves[self.current_move_index]
            self.current_move_index += 1
            direction = self.direction_map.get(direction_char, (0, 0))
            
            # Calculate the new position if the move is executed
            new_x = self.position[0] + direction[0] * self.speed
            new_y = self.position[1] + direction[1] * self.speed
            
            # Check if the new position is blocked by an obstacle
            if (0 <= new_x < environment.width and
                0 <= new_y < environment.height and
                environment.grid[new_y, new_x] != '#'):
                return direction
            
            print(f"Move {direction_char} blocked by obstacle or out of bounds. Staying at {self.position}.")
        
        return (0, 0)  # No valid move

    def move(self, direction, environment):
        """Move the actor in the specified direction if not blocked by an obstacle."""
        new_x = self.position[0] + direction[0] * self.speed
        new_y = self.position[1] + direction[1] * self.speed
        
        # Ensure the new position is within bounds and not blocked
        if (0 <= new_x < environment.width and
            0 <= new_y < environment.height and
            environment.grid[new_y, new_x] != '#'):
            self.position = (new_x, new_y)
        else:
            print(f"Blocked by obstacle or out of bounds at {(new_x, new_y)}. Staying at {self.position}.")

    def step(self, environment):
        """
        Perform one time step in the environment, scanning, deciding, and moving.
        
        :param environment: The 2D grid representing the environment.
        """
        direction = self.make_decision(environment)
        self.move(direction, environment)

    def set_predefined_moves(self, moves):
        """
        Set a sequence of predefined moves for the actor.
        
        :param moves: String of moves (e.g., "UULLRDU").
        """
        self.predefined_moves = list(moves)
        self.current_move_index = 0  # Reset the index when setting new moves
