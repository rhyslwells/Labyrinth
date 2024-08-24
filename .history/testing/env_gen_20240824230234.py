import numpy as np
import pandas as pd

def generate_environment(rows: int, cols: int, start_pos: tuple[int, int], end_pos: tuple[int, int], walls: list[tuple[int, int]]) -> np.ndarray:
    """
    Generates a grid environment with start and end positions and optional walls.

    Args:
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        start_pos (tuple[int, int]): Starting position (row, col).
        end_pos (tuple[int, int]): Ending position (row, col).
        walls (list[tuple[int, int]]): List of wall positions (row, col).

    Returns:
        np.ndarray: Generated environment grid.
    """
    # Initialize environment with empty spaces
    env = np.full((rows, cols), '', dtype=str)

    # Place start and end positions
    env[start_pos] = 's'
    env[end_pos] = 't'

    # Place walls
    for wall in walls:
        env[wall] = 'w'

    return env

def save_environment_to_csv(env: np.ndarray, file_path: str):
    """
    Saves the environment grid to a CSV file.

    Args:
        env (np.ndarray): The environment grid.
        file_path (str): Path to the CSV file to save.
    """
    # Convert the numpy array to a pandas DataFrame
    df = pd.DataFrame(env)
    
    # Save the DataFrame to a CSV file
    df.to_csv(file_path, index=False, header=False, sep=';')

# Example usage
rows, cols = 8, 8
start_pos = (0, 0)
end_pos = (7, 7)
walls = [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2)]  # Example wall positions

env = generate_environment(rows, cols, start_pos, end_pos, walls)
print(env)

# Save the environment to a CSV file
save_environment_to_csv(env, 'environment-walled.csv')
