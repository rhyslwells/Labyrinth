


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

# A Game Instance

A Game will consist of Actors within an Environment. 

A Game ends if an Actor reaches their objective, and a loss for all other Actors.

A Game can be visualised. In particular the Environment and Actors.

For each time step of a Game we record the position of Actors within the Environment in a Table.

Game statistics such as success rate, which actor wins, average time to catch, and escape rates, will be recorded for future analysis.

# Entities

As the movement dynamics and characteristics of both hunter and prey are similar. They will inherit from a parent class called Actor.

The Actor class:

- Focuses movement characteristics such as position and speed,
- Size and shape of actor.
- Actors will explore towards their objective.
- Actors can change speeds dynamically during the game. There is a fixed maximum speed they can attain.
- To navigate the actors will scan, make a decision, then travel in the direction of the decision. They will do this in discrete steps (aim to do this continuously).

## Hunter 
The **Hunter** subclass:
- Moves towards the **Prey**
- The hunter’s objective is to get to the **Prey**.
- If the hunter sees the prey (during a scan), the **Hunter** will want to minimize the distance from **Prey**.

Hunter's Goal: Learn a policy that maximizes the probability of capturing the prey in the shortest possible time.

## Prey 
The **Prey** subclass:
- The prey's objective is to get to the exit.
- If seen (during a scan) by the **Hunter** the **Prey** will want to maximize the distance from hunter
- The prey may approach the **Hunter** if it increases the total distance in the long run.

Prey's Goal: Learn a policy that maximizes the likelihood of evading the hunter for the longest possible time.

# Environment of a Game

Each Game will take place within an Environment. The Actor’s will navigate within the Environment 

The Environment will have boundaries and obstacles that the Actor’s interact with and can not pass through.


#  Game Class
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
