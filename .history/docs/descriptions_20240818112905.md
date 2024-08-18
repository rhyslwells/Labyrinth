# Class Summaries

- The `Game` class handles the overall simulation, tracking movements, managing time steps, and collecting game statistics. It also creates and maintains the grid, allowing for visualization and strategic placement of obstacles and exits.
- The `Actor` class defines common behaviors for both hunters and prey, with specialized subclasses for their unique goals. It now includes a sightline ability that has replaced the previous scanning mechanism.
- Learning strategies classes: `QLearning` and `Sarsa`.

## 1. Game Class

The `Game` class serves as the main controller for the simulation. It manages the interaction between actors (hunters and prey) within an environment. Each game starts with the hunter and prey at fixed positions within the environment. The primary responsibilities of this class include:

- **Environment Simulation**: The game runs within a 2D grid where actors (hunters and prey) move and interact.
  - Each actor gets a turn to move based on their decision-making process.
- **Time Steps and Statistics Tracking**: For each time step, the positions of the actors are recorded in a table. Key statistics like success rates, average time to capture, and escape frequencies are tracked for future analysis.
- **Game Termination**: The game ends when an actor reaches their objective (e.g., hunter captures prey or prey escapes), leading to a win/loss scenario for all involved actors.
- **Visualization**: The environment and actors can be visualized, allowing for easy tracking of the simulation.
  - Use a simple matplotlib or seaborn heatmap to represent the environment, showing the positions of the hunter, prey, obstacles, and the exit.
  - Animate the game by updating the plot at each time step.
- **Grid Setup**: Initializes a 2D numpy array representing the grid, with cells for empty spaces, obstacles, exits, and actors (starting positions). The grid should be finite, with defined boundaries that actors cannot cross. Use a 2D numpy array to represent obstacles as `1`, exits as `2`, prey as `3`, and the hunter as `4`.

## 2. Actor Class

The `Actor` class is the base class for all entities (hunters and prey) in the environment. Both types of actors inherit common behaviors and movement dynamics from this class. The class now uses a **sightline** mechanism, replacing the previous scanning feature, to gather information about the environment. Key attributes and methods include:

- **Position and Speed**: Each actor has a position on the grid and a defined movement speed. Actors can change speeds dynamically during the game, with a fixed maximum speed.
- **Movement (`move`)**: Updates the actor’s position based on direction `(dx, dy)`.
- **Sightline (`sightline`)**: Detects cells in a straight line from the actor's position in multiple directions until the view is blocked by an obstacle. This allows the actor to perceive its surroundings more effectively and plan its moves accordingly.
- **Decision-Making (`make_decision`)**: Uses the sightline results to determine the next move. The actor can then decide to move towards its objective, avoid an obstacle, or make a random move based on what it "sees".
- **Stepping (`step`)**: Simulates a time step where the actor uses its sightline, makes a decision, and moves.
- Actors cannot pass through obstacles, which are represented as blocked cells on the grid.

### Actor: Reward and Penalty System for Learning Strategies

Each actor will have its own **learning strategy**. The reward and penalties for these strategies include:

- Each move for an actor from one state to the next is rewarded or penalized:
  - Each move from one cell to an adjacent cell costs `-0.04` points, discouraging unnecessary wandering.
  - An attempt to enter a blocked cell ("red" cell) costs `-0.75` points. Although the move is invalid, the severe penalty teaches the actor to avoid such cells.
  - A move to a previously visited cell incurs a `-0.25` point penalty, discouraging counterproductive behavior.

### Hunter Subclass

The `Hunter` subclass inherits from the `Actor` class and represents an agent that chases the prey. Key characteristics include:

- **Objective**: The hunter’s goal is to minimize the distance to the prey and eventually capture it.
- **Behavior**: The hunter actively uses sightlines to detect the prey and adjusts its movements to optimize capture.
- **Learning Goal**: The hunter aims to learn a policy that maximizes the probability of capturing the prey in the shortest possible time.

**Behavior:**

- If the prey is within the scan range, the hunter moves directly towards it.
- If the prey is not visible, the hunter moves in a search direction or towards the last known position of the prey.

### Prey Subclass

The `Prey` subclass also inherits from the `Actor` class and represents an agent trying to evade the hunter and reach the exit. Key characteristics include:

- **Objective**: The prey’s goal is to reach the exit while avoiding capture by the hunter.
- **Behavior**: The prey uses its sightline ability to detect obstacles and avoid the hunter. It may also alter its path to maximize the distance from the hunter or, in certain cases, approach the hunter if it benefits its overall escape strategy.
- **Learning Goal**: The prey seeks to learn a policy that maximizes the likelihood of evading the hunter for as long as possible.

## QLearning Class

The `QLearning` class implements the Q-learning algorithm, a model-free reinforcement learning technique. This class is designed to enable an agent (hunter or prey) to learn optimal policies based on trial and error. Q-learning uses a Q-table to store the estimated utility (expected future reward) for taking a specific action in a given state.

### Key Components

- **Learning Rate (`learning_rate`)**: Determines how much the newly acquired information overrides the old information. It controls the update step when adjusting the Q-value.
- **Discount Factor (`discount_factor`)**: Represents the importance of future rewards versus immediate rewards. A value closer to 1 places more emphasis on long-term rewards.
- **Exploration Rate (`epsilon`)**: Balances exploration and exploitation by determining whether the agent explores random actions or exploits known information from the Q-table.
- **Q-Table (`q_table`)**: A table (implemented as a tensor) that stores Q-values, which represent the expected rewards for state-action pairs. The Q-table is initialized to zeros and is updated iteratively as the agent interacts with the environment.

### Methods

- **`update(s_t, a_t, reward, s_next)`**: Updates the Q-value for a given state-action pair using the temporal difference (TD) update rule. The update is based on the observed reward and the estimated future rewards.
- **`_get_temporal_difference(s_t, a_t, reward, s_next)`**: Computes the temporal difference, which measures the discrepancy between the predicted and observed Q-values.
- **`_get_temporal_target(reward, s_next)`**: Calculates the temporal target, which represents the immediate reward plus the discounted future reward for the next state.
- **`get_best_action(s_t)`**: Returns the action with the highest Q-value for the current state. This method is used when the agent decides to exploit its learned knowledge.
- **`get_action(s_t)`**: Determines the next action to take based on the exploration-exploitation tradeoff controlled by epsilon. The agent either chooses the best-known action or explores a random action.

### Usage

- **State Representation**: The state is represented as a tuple, mapping to the Q-table’s indices. The state is typically defined by the actor's position and environment features.
- **Training Process**: The agent iteratively interacts with the environment, observing the state, taking an action, receiving a reward, and updating the Q-table. Over time, the Q-values converge toward the optimal policy.

### Example Workflow

1. The agent starts in a particular state `s_t`.
2. The `get_action(s_t)` method decides whether to explore or exploit.
3. The agent takes the chosen action `a_t`, receives a reward, and transitions to a new state `s_next`.
4. The `update(s_t, a_t, reward, s_next)` method updates the Q-table based on the observed reward and the predicted future reward.

This process repeats, allowing the agent to learn an optimal policy through experience.

## Sarsa Class

The `Sarsa` class implements the Sarsa (State-Action-Reward-State-Action) algorithm, a model-free reinforcement learning method that, unlike Q-learning, updates its Q-values based on the action chosen by the policy in the next state. This makes Sarsa an on-policy learning method, where updates are made using the actual actions that the agent follows.

### Key Components

- **Learning Rate (`learning_rate`)**: Controls how quickly the Q-values are updated in response to new information. It governs how much weight is given to the new estimate versus the existing estimate.
- **Discount Factor (`discount_factor`)**: Balances the importance of immediate rewards versus long-term rewards. A higher value places more emphasis on future rewards.
- **Exploration Rate (`epsilon`)**: Regulates the exploration-exploitation tradeoff by determining whether the agent should explore new actions or exploit known information from the Q-table.
- **Q-Table (`q_table`)**: A table (implemented as a tensor) storing Q-values, which represent the expected utility of performing an action in a specific state. The table is initialized to zeros and is updated as the agent interacts with the environment.

### Methods

- **`update(s_t, a_t, reward, s_next, a_next)`**: Updates the Q-value for the current state-action pair using the Sarsa update rule, which considers both the current and the next action taken by the agent.
- **`_get_temporal_difference(s_t, a_t, reward, s_next, a_next)`**: Computes the temporal difference, which measures the error between the current Q-value and the temporal target.
- **`_get_temporal_target(reward, s_next, a_next)`**: Calculates the temporal target, which is the sum of the immediate reward and the discounted future reward for the next state-action pair.
- **`get_best_action(s_t)`**: Returns the action with the highest Q-value for the given state. This method is used when the agent decides to exploit its learned knowledge.
- **`get_action(s_t)`**: Determines the next action based on epsilon-greedy exploration. The agent either selects a random action (exploration) or the best-known action (exploitation) based on the current Q-table.

### Workflow

- **State and Action Representation**: The state is represented as a tuple, and the action is selected from the action space. The Q-table uses these indices to store and retrieve Q-values.
- **Training Process**: The agent observes a state `s_t`, selects an action `a_t`, receives a reward, and transitions to a new state `s_next` while selecting the next action `a_next`. The Q-table is updated based on the Sarsa update rule.
- **Update Rule**: The Q-value is updated using the actual next action `a_next`, unlike Q-learning, which updates based on the greedy action. This leads to a more conservative learning approach, especially in stochastic environments.

### Example Workflow

1. The agent begins in a state `s_t` and selects an action `a_t` using the `get_action(s_t)` method.
2. The agent takes the action, receives a reward, and transitions to a new state `s_next`.
3. In the new state, the agent selects the next action `a_next`.
4. The `update(s_t, a_t, reward, s_next, a_next)` method updates the Q-table based on the Sarsa update rule.

The process repeats, allowing the agent to improve its policy over time.

# Analysis

Analysis can be done within the learning classes of a given actor. Each actor will have its own learning strategy (e.g., `QLearning`). The comparison of learning strategies across multiple actors can be performed in the `Game` class.

- At each time step, record the positions of both actors (see `Actor` class).
- The `Actor` class will note the position in the game grid.
- General actor statistics are tracked within the `Actor` class.
- Specific prey and hunter statistics can be found in their respective subclasses.
- The `Game` class consolidates these statistics from the actors and subclasses, tracking game metrics such as the number of steps taken, whether the prey escaped, or if the hunter caught the prey. Data on outcomes, such as success rates, average time to catch/escape, and path distributions, are collected for further analysis.
