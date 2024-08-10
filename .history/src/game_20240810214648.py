import os
import pandas as pd
from PIL import Image
from actor import Actor
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
        self.data = pd.DataFrame(columns=['Step', 'Position', 'Time'])
    
    def save_initial_state(self):
        """Save the initial state of the environment."""
        self.environment.place_actor(self.actor.position, "A")
        self.environment.save_to_image(f"gif_data/{self.name}_step_0.png")
        
        # Record the initial state
        self.record_step(0)

    
    def record_step(self, step):
        """Record the current step, actor's position, and in-game time."""
        x, y = self.actor.position
        new_data = pd.DataFrame({
            'Time': [step],  # In-game time is the step number
            'x_coord': [x],
        '   y_coord': [y]
        })
        self.data = pd.concat([self.data, new_data], ignore_index=True)
    
    def simulate(self):
        """Simulate the actor's movement and save images for each step."""
        predefined_moves = self.actor.predefined_moves
        
        for step in range(1, len(predefined_moves) + 1):
            print(f"\nStep {step}:")
            
            # Clear the previous actor position
            self.environment.grid[self.actor.position[1], self.actor.position[0]] = '.'
            
            # Actor takes a step
            self.actor.step()
            
            # Place the actor's new position on the grid and save the image
            self.environment.place_actor(self.actor.position, "A")
            self.environment.save_to_image(f"gif_data/{self.name}_step_{step}.png")
            
            # Record the current step
            self.record_step(step)
    
    def create_gif(self):
        """Create a GIF from the saved images and remove the PNG files."""
        num_steps = len(self.actor.predefined_moves) + 1
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

# Example usage of the Game class:
def main():
    game_name = "Game_2"
    width, height = 10, 10
    obstacles = [(3, 1), (3, 2), (3, 3)]
    exit_point = (9, 8)
    actor_start_position = (1, 1)
    predefined_moves = "RRRRRDDDDDDDRRRRRRRRR"
    
    game = Game(game_name, width, height, obstacles, exit_point, actor_start_position, predefined_moves)
    
    # Save the initial state
    game.save_initial_state()
    
    # Simulate the game
    game.simulate()
    
    # Create a GIF and clean up PNG files
    game.create_gif()
    
    # Save the recorded data
    game.save_dataframe(f"gif_data/{game_name}_data.csv")

if __name__ == "__main__":
    main()
