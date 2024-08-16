# Objective

Create a simplified version of the hunter-prey dynamic within a 2D environment. The MVP should allow for basic simulations and visualizations, focusing on the core mechanics of movement, pursuit, and escape.

## Tasks: Implementation Steps

### 1. Setup the Environment
- Implement a 2D grid with obstacles and an exit point.

### 2. Create the Actor Base Class
- Implement movement and decision-making processes.

### 3. Subclass Hunter and Prey
- Implement specific behaviors for both actors.

### 4. Develop Game Logic
- Create a loop that progresses the game, handles actor movement, and checks for win conditions.

### 5. Add Visualization
- Implement basic grid visualization to display actor positions over time.

### 6. Run Simulations
- Automate running multiple games and collecting data for analysis.

### 7. Analysis and Insights
- Generate basic plots and statistical insights from the collected data.

## Implementation Details

### 1. Environment Setup

#### 2D Grid World
- The environment will be a simple 2D grid where each cell represents a possible position for the actors (hunter and prey). The grid should be finite, with defined boundaries that actors cannot cross.

#### Obstacles
- Start with a simple environment containing a few static obstacles (e.g., walls or barriers) that actors cannot pass through. These obstacles can be represented as blocked cells on the grid.

#### Exit Point
- Define a single exit point for the prey within the environment. This is the prey's objective.

### 2. Actor Classes

#### Actor Base Class
**Attributes:** Position, speed, size, shape.  
**Methods:**
- **Move:** Updates the actor's position based on the decision-making process.
- **Scan:** Allows the actor to "see" nearby cells (within a certain range) and detect obstacles, other actors, or the exit.
- **Decision-Making:** Based on the scan, the actor decides on the next move. For the MVP, use a simple rule-based approach (e.g., always move towards the nearest target).

#### Hunter Subclass
**Objective:** Move towards the prey.  
**Behavior:**
- If the prey is within the scan range, the hunter moves directly towards it.
- If the prey is not visible, the hunter moves in a random direction or towards the last known position of the prey.

#### Prey Subclass
**Objective:** Reach the exit while avoiding the hunter.  
**Behavior:**
- If the hunter is within the scan range, the prey moves away from it.
- If not, the prey moves towards the exit.

### 3. Game Mechanics

#### Initialization
- Start each game with the hunter and prey at fixed positions within the environment.
- The prey knows the location of the exit, and the hunter knows the location of the prey.

#### Movement and Turns
- The game progresses in discrete time steps.
- Each actor gets a turn to move based on their decision-making process.
- The game ends when either the hunter catches the prey or the prey reaches the exit.

#### Reward and Penalty System
- Each move from one state to the next will be rewarded (e.g., the rat gains points) by a positive or negative (penalty) amount.
- Each move from one cell to an adjacent cell will cost -0.04 points, discouraging unnecessary wandering.
- An attempt to enter a blocked cell ("red" cell) will cost -0.75 points. Although the move is invalid and not executed, the severe penalty teaches the actor to avoid such cells.
- A move to a previously visited cell incurs a -0.25 point penalty, discouraging counterproductive behavior.

#### Recording Data
- At each time step, record the positions of both actors.
- Track game statistics such as the number of steps taken, whether the prey escaped, or if the hunter caught the prey.

### 4. Visualization

#### Grid Visualization
- Use a simple matplotlib or seaborn heatmap to represent the environment, showing the positions of the hunter, prey, obstacles, and the exit.
- Animate the game by updating the plot at each time step.

### 5. Simulation and Analysis

#### Multiple Simulations
- Run multiple games with slight variations in starting positions, obstacle placements, or actor speeds.
- Collect data on the outcomes for analysis, such as success rates for the hunter and prey, average time to catch/escape, and distribution of paths taken.

#### Basic Analysis
- Plot the success rates of the hunter and prey over many games.
- Analyze the average number of steps taken for different scenarios.
