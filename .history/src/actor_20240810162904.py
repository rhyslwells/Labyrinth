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
