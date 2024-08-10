from game import Game

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
    
    # Simulate the game without saving images
    game.simulate(save_images=False)
    
    # Create a GIF and clean up PNG files
    # game.create_gif()
    
    # Save the recorded data
    game.save_dataframe(f"gif_data/{game_name}_data.csv")

if __name__ == "__main__":
    main()
