import sys
import os

# Add the parent directory of `components` and `testing` to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from components.game.game import Game
from components.utils.rendering import GameWindow
FPS = 30

# Create a Game instance
game = Game(name='SimpleGridGame', world='7x7-simple', delay=10)

# Initialize GameWindow for visualization
game_window = GameWindow(game, width=800, height=800, fps=FPS)

# Run the visualization loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Render the game environment
    game_window.render()
    
    # Optional: Step through the game (e.g., move the actor around) for demonstration
    # Here we simulate a step in the game loop
    action = game.sample()  # Random action for demonstration
    game.step(action)
    
pygame.quit()

