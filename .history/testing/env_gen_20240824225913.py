import numpy as np
import pandas as pd
import Tuple

def generate_environment(rows: int, cols: int, start_pos: Tuple[int, int], end_pos: Tuple[int, int], walls: List[Tuple[int, int]]) -> np.ndarray:
    """
    Generates a grid environment with start and end positions and optional walls.

    Args:
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        start_pos (Tuple[int, int]): Starting position (row, col).
        end_pos (Tuple[int, int]): Ending position (row, col).
        walls (List[Tuple[int, int]]): List of wall positions (row, col).

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

# Example usage
rows, cols = 8, 8
start_pos = (0, 0)
end_pos = (7, 7)
walls = [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2)]  # Example wall positions

env = generate_environment(rows, cols, start_pos, end_pos, walls)
print(env)
