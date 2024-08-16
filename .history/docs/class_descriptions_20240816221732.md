# Class Descriptions for the Hunter-Prey Game

## Summary

- The `Game` class handles the overall simulation, tracking movements, managing time steps, and collecting game statistics.
- The `Actor` class defines common behaviors for both hunters and prey, with specialized subclasses for their unique goals, and now includes a sightline ability that has replaced the previous scanning mechanism.
- The `Environment` class creates and maintains the grid, allowing for visualization and strategic placement of obstacles and exits.

## 1. Game Class

The `Game` class serves as the main controller for the simulation. It manages the interaction between actors (hunters and prey) within an environment. The primary responsibilities of this class include:

- **Environment Simulation**: The game runs within a 2D grid where actors (hunters and prey) move and interact.
- **Movement Flexibility**: Allows for predefined movements or random moves for the actors, supporting both deterministic and stochastic simulations.
- **Time Steps and Statistics Tracking**: For each time step, the positions of the actors are recorded in a table. Key statistics like success rates, average time to capture, and escape frequencies are tracked for future analysis.
- **Game Termination**: The game ends when an actor reaches their objective (e.g., hunter captures prey or prey escapes), leading to a win/loss scenario for all involved actors.
- **Visualization**: The environment and actors can be visualized, allowing for easy tracking of the simulation.

## 2. Actor Class

The `Actor` class is the base class for all entities (hunters and prey) in the environment. Both types of actors inherit common behaviors and movement dynamics from this class. The class now uses a **sightline** mechanism, replacing the previous scanning feature, to gather information about the environment. Key attributes and methods include:

- **Position and Speed**: Each actor has a position on the grid and a defined movement speed. Actors can change speeds dynamically during the game, with a fixed maximum speed.
- **Movement (`move`)**: Updates the actor’s position based on direction `(dx, dy)`.
- **Sightline (`sightline`)**: Detects cells in a straight line from the actor's position in multiple directions until the view is blocked by an obstacle. This allows the actor to perceive its surroundings more effectively and plan its moves accordingly.
- **Decision-Making (`make_decision`)**: Uses the sightline results to determine the next move. The actor can then decide to move towards its objective, avoid an obstacle, or make a random move based on what it "sees".
- **Stepping (`step`)**: Simulates a time step where the actor uses its sightline, makes a decision, and moves.

### Hunter Subclass

The `Hunter` subclass inherits from the `Actor` class and represents an agent that chases the prey. Key characteristics include:

- **Objective**: The hunter’s goal is to minimize the distance to the prey and eventually capture it.
- **Behavior**: The hunter actively uses sightlines to detect the prey and adjusts its movements to optimize capture.
- **Learning Goal**: The hunter aims to learn a policy that maximizes the probability of capturing the prey in the shortest possible time.

### Prey Subclass

The `Prey` subclass also inherits from the `Actor` class and represents an agent trying to evade the hunter and reach the exit. Key characteristics include:

- **Objective**: The prey’s goal is to reach the exit while avoiding capture by the hunter.
- **Behavior**: The prey uses its sightline ability to detect obstacles and avoid the hunter. It may also alter its path to maximize the distance from the hunter or, in certain cases, approach the hunter if it benefits its overall escape strategy.
- **Learning Goal**: The prey seeks to learn a policy that maximizes the likelihood of evading the hunter for as long as possible.

## 3. Environment Class

The `Environment` class is responsible for managing the 2D grid where the game takes place. It handles:

- **Grid Setup**: Initializes a 2D numpy array representing the grid, with cells for empty spaces, obstacles, exits, and actors.
- **Obstacles and Exits**: Obstacles can be added with the `add_obstacle` method and are marked as `#`. Exits are set with the `set_exit` method and are represented by `E`.
- **Actor Placement (`place_actor`)**: Places hunters (`H`) and prey (`P`) on the grid at specified positions.
- **Display (`display`)**: Visualizes the grid using symbols like `.` for empty spaces, `#` for obstacles, `E` for exits, and `H`/`P` for hunters and prey.
