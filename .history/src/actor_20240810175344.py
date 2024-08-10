import random

class Actor:
    def __init__(self, position, environment, speed=1):
        """
        Initialize the actor with a starting position, environment, and speed.
        
        :param position: Tuple (x, y) representing the actor's position.
        :param environment: The Environment instance this actor interacts with.
        :param speed: Maximum number of cells the actor can move in one time step.
        """
        self.position = position
        self.speed = speed
        self.environment = environment
        self.predefined_moves = []
        self.current_move_index = 0

        # Define the mapping for the directions
        self.direction_map = {
            'U': (0, -1),  # Up
            'D': (0, 1),   # Down
            'L': (-1, 0),  # Left
            'R': (1, 0)    # Right
        }

    def scan(self):
        """
        Scan the environment to determine which directions are valid for movement.
        
        :return: A dictionary with valid directions and their respective coordinates.
        """
        x, y = self.position
        directions = {}
        
        # Check Up
        if y > 0 and self.environment.grid[y-1, x] != '#':
            directions['U'] = (0, -1)
        # Check Down
        if y < self.environment.height - 1 and self.environment.grid[y+1, x] != '#':
            directions['D'] = (0, 1)
        # Check Left
        if x > 0 and self.environment.grid[y, x-1] != '#':
            directions['L'] = (-1, 0)
        # Check Right
        if x < self.environment.width - 1 and self.environment.grid[y, x+1] != '#':
            directions['R'] = (1, 0)
        
        return directions

    def make_decision(self):
        """
        Decide on the next move based on predefined moves and check for valid directions.
        
        :return: The chosen direction as a tuple (dx, dy).
        """
        valid_directions = self.scan()  # Get valid directions based on surroundings
        
        if self.predefined_moves and self.current_move_index < len(self.predefined_moves):
            direction_char = self.predefined_moves[self.current_move_index]
            self.current_move_index += 1
            direction = self.direction_map.get(direction_char, (0, 0))
            
            # Check if the predefined move is in the valid directions
            if direction_char in valid_directions:
                return valid_directions[direction_char]
            else:
                print(f"Predefined move {direction_char} blocked or invalid. Staying at {self.position}.")
        
        return (0, 0)  # No valid move

    def move(self, direction):
        """
        Move the actor in the specified direction if not blocked by an obstacle.
        
        :param direction: Tuple (dx, dy) representing the direction to move.
        """
        new_x = self.position[0] + direction[0] * self.speed
        new_y = self.position[1] + direction[1] * self.speed
        
        # Update position if within bounds
        if (0 <= new_x < self.environment.width and
            0 <= new_y < self.environment.height):
            self.position = (new_x, new_y)
        else:
            print(f"Move blocked by obstacle or out of bounds at {(new_x, new_y)}. Staying at {self.position}.")

    def step(self):
        """
        Perform one time step in the environment, scanning, deciding, and moving.
        """
        direction = self.make_decision()
        self.move(direction)

    def set_predefined_moves(self, moves):
        """
        Set a sequence of predefined moves for the actor.
        
        :param moves: String of moves (e.g., "UULLRDU").
        """
        self.predefined_moves = list(moves)
        self.current_move_index = 0  # Reset the index when setting new moves
