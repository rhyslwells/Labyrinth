import numpy as np
from PIL import Image

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.full((height, width), '.', dtype=str)
        
    def add_obstacle(self, position):
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = '#'
    
    def set_exit(self, position):
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = 'E'
    
    def place_actor(self, position, actor_id):
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = actor_id
    
    def display(self):
        for row in self.grid:
            print(" ".join(row))
    
    def save_to_image(self, filename):
        color_map = {
            '.': (255, 255, 255),  # White for empty space
            '#': (0, 0, 0),       # Black for obstacles
            'E': (255, 0, 0),     # Red for exit
            'A': (0, 255, 0)      # Green for actor
        }
        image_data = np.array([[color_map[cell] for cell in row] for row in self.grid], dtype=np.uint8)
        img = Image.fromarray(image_data)
        img.save(filename)

class Actor:
    def __init__(self, position, environment, speed=1):
        self.position = position
        self.speed = speed
        self.environment = environment
        self.predefined_moves = []
        self.current_move_index = 0
        self.direction_map = {
            'U': (0, -1),
            'D': (0, 1),
            'L': (-1, 0),
            'R': (1, 0)
        }

    def scan(self):
        x, y = self.position
        directions = {}
        
        if y > 0 and self.environment.grid[y-1, x] != '#':
            directions['U'] = (0, -1)
        if y < self.environment.height - 1 and self.environment.grid[y+1, x] != '#':
            directions['D'] = (0, 1)
        if x > 0 and self.environment.grid[y, x-1] != '#':
            directions['L'] = (-1, 0)
        if x < self.environment.width - 1 and self.environment.grid[y, x+1] != '#':
            directions['R'] = (1, 0)
        
        return directions

    def make_decision(self):
        valid_directions = self.scan()
        
        if self.predefined_moves and self.current_move_index < len(self.predefined_moves):
            direction_char = self.predefined_moves[self.current_move_index]
            self.current_move_index += 1
            direction = self.direction_map.get(direction_char, (0, 0))
            
            if direction_char in valid_directions:
                return valid_directions[direction_char]
            else:
                print(f"Predefined move {direction_char} blocked or invalid. Staying at {self.position}.")
        
        return (0, 0)  # No valid move

    def move(self, direction):
        new_x = self.position[0] + direction[0] * self.speed
        new_y = self.position[1] + direction[1] * self.speed
        
        if (0 <= new_x < self.environment.width and
            0 <= new_y < self.environment.height and
            self.environment.grid[new_y, new_x] != '#'):
            self.position = (new_x, new_y)
        else:
            print(f"Move blocked by obstacle or out of bounds at {(new_x, new_y)}. Staying at {self.position}.")

    def step(self):
        direction = self.make_decision()
        self.move(direction)

    def set_predefined_moves(self, moves):
        self.predefined_moves = list(moves)
        self.current_move_index = 0

# Create the environment
env = Environment(width=10, height=10)

# Add obstacles and exit
for i in range(10):
    env.add_obstacle((i, 0))
    env.add_obstacle((i, 9))
    env.add_obstacle((0, i))
    env.add_obstacle((9, i))

env.set_exit((9, 9))

# Create an actor and place it in the environment
actor = Actor(position=(1, 1), environment=env)

# Set predefined moves
predefined_moves = "RRRRRDDDDDD"
actor.set_predefined_moves(predefined_moves)

# Capture initial state
env.place_actor(actor.position, "A")
env.save_to_image("step_0.png")

# Simulate the actor's movement
for step in range(len(predefined_moves)):
    print(f"\nStep {step + 1}:")
    
    # Clear the previous actor position (for visual clarity)
    env.grid[actor.position[1], actor.position[0]] = '.'
    
    # Actor takes a step
    actor.step()
    
    # Place the actor's new position on the grid and save the image
    env.place_actor(actor.position, "A")
    env.save_to_image(f"step_{step + 1}.png")

print("Simulation complete. Creating GIF...")

# Create GIF
images = [Image.open(f"step_{i}.png") for i in range(len(predefined_moves) + 1)]
gif_filename = "actor_simulation.gif"
images[0].save(gif_filename, save_all=True, append_images=images[1:], duration=500, loop=0)

print(f"GIF saved as {gif_filename}.")
