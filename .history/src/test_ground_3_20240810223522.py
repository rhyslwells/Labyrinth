from game import Game
import time

def run_game(game_name, predefined_moves):
    """
    Run a game simulation with fixed environment settings and varying actor movements.

    Parameters:
        game_name (str): The name of the game.
        predefined_moves (str): A string of predefined moves (e.g., "RRUDL").
    """
    # Fixed environment parameters
    width = 10
    height = 10
    obstacles = [(3, 1), (3, 2), (3, 3)]
    exit_point = (9, 8)
    actor_start_position = (1, 1)

    # Initialize the game with fixed parameters and varying moves
    game = Game(game_name, width, height, obstacles, exit_point, actor_start_position, predefined_moves)
    
    # Save the initial state
    game.save_initial_state()
    
    # Simulate the game without saving images
    game.simulate()
    
    # Create a GIF and clean up PNG files
    game.create_gif()
    
    # Save the recorded data to a CSV file
    game.save_dataframe(f"gif_data/{game_name}_data.csv")

# Example of running multiple games with different movements
def main():
    # Define different movement sequences for each game
    game_movements = [
        {'game_name': "Game_1", 'predefined_moves': "RRRDDDD"},
        {'game_name': "Game_2", 'predefined_moves': "RLRLRUUDDUUDD"},
        {'game_name': "Game_3", 'predefined_moves': "RRDLLUUUR"},
        {'game_name': "Game_4", 'predefined_moves': "DDDDRRRRUUUU"}
    ]
    
    # Run each game scenario with the fixed environment and different moves
    for game_params in game_movements:
        run_game(**game_params)
        #pause 1 second
        time.sleep(1)

if __name__ == "__main__":
    main()
