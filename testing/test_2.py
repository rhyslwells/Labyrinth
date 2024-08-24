
import sys
import os

# Add the parent directory of `components` and `testing` to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from components.game.archive.game_everything import Game
from components.actors.actor import Actor

from components.game.rendering import GameWindow  # Assuming this is an additional class for visualization

FPS = 30


# Create a Game instance
game = Game(name='SimpleGridGame', world='environment-walled', delay=100)

# Initialize GameWindow for visualization
game_window = GameWindow(game, width=800, height=800, fps=FPS)

# Optionally: Save the initial state of the game
game.save_initial_state(save_images=True)

# Run the game loop
step = 0
max_steps = 100  # Define a maximum number of steps to prevent an infinite loop
while step < max_steps:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Step through the game (e.g., move the actor around)
    action = game.sample()  # Random action for demonstration
    state, reward, done, _ = game.step(action)
    
    # Render the game environment using GameWindow
    game_window.render()

    # Record the step
    game.record_step(step)

    if done:
        print("Actor has reached the goal!")
        break

    step += 1

# Calculate and save metrics
game.calculate_metrics(step)
game.save_metrics('game_metrics.csv')

# Optionally: Visualize the final state of the grid
game.visualize_grid()

# Optionally: Animate the game (make sure gif_data directory exists)
game.animate_game(frames=step)

# Cleanup and exit
pygame.quit()
