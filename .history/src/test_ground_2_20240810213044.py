import os
from PIL import Image
from actor import Actor
from game import Game
from environment import Environment

# Example usage of the Game class:
def main():
    game_name = "Game_1"
    width, height = 10, 10
    obstacles = [(3, 1), (3, 2), (3, 3)]
    exit_point = (9, 8)
    actor_start_position = (1, 1)
    predefined_moves = "RRRDDDDDDDRRRRRRRRR"
    
    game = Game(game_name, width, height, obstacles, exit_point, actor_start_position, predefined_moves)
    
    # Save the initial state
    game.save_initial_state()
    
    # Simulate the game
    game.simulate()
    
    # Create a GIF and clean up PNG files
    game.create_gif()

if __name__ == "__main__":
    main()


