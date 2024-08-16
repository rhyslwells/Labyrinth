### Q-Learning
- Explore Python implementation of Q-learning for reinforcement learning.

### Game Class
- Focus on creating a `Game` class to simulate an environment with actors.
- Initial focus on predefined movements, with flexibility for random or predefined actor moves.


### Actor Class
- Allows testing of specific movement patterns to ensure expected actor behavior.
- Actors are prevented from moving into obstacle positions.
- `Actor` class initialized with starting position and movement speed.
- `move` method updates position based on direction `(dx, dy)`.
- `scan` method checks adjacent cells for obstacles, exits, or other actors.
- `make_decision` method uses scan results to choose next move, defaulting to random moves if not blocked.
- `step` method simulates a time step by scanning, deciding, and moving.

### Environment Class
- `Environment` class manages a 2D grid representing the game.
- Grid initialized as a 2D numpy array with cells for empty spaces, obstacles, exits, and actors.
- Methods to add obstacles (`add_obstacle`) and set an exit (`set_exit`) on the grid.
- Obstacles marked as `#`, exits as `E`.
- `place_actor` method for placing actors (hunter/prey) on the grid.
- Unique IDs used: `H` for hunters, `P` for prey.
- `display` method visualizes the grid using symbols for elements (e.g., `.` for empty, `#` for obstacles, `E` for exit).