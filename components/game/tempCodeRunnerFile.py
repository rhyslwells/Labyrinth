# example_usage.py
import os
from components.game.game import Game

def main():
    # Set up directories for saving images and metrics
    if not os.path.exists('gif_data'):
        os.makedirs('gif_data')

    # Create a Game instance
    game = Game(name='example_game', world='environment-walled', delay=100)

    # Save the initial state of the game
    game.save_initial_state(save_images=True)

    # Run the game loop for a maximum of 100 steps
    game.game_loop(max_steps=100)

    # Save the metrics to a CSV file
    game.save_metrics('gif_data/example_game_metrics.csv')

    # Visualize the grid using matplotlib
    game.visualize_grid()

    # Create an animation of the game
    # Ensure you have the correct number of frames or steps
    game.animate_game(frames=100)

if __name__ == "__main__":
    main()
