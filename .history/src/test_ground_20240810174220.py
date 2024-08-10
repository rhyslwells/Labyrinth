from actor import Actor
from enviroment import Environment

# Example useage of the Environment class :--------------------------------------------------------------------------

def create_environment():
    # Initialize the environment
    env = Environment(10, 10)

    # Add some obstacles
    env.add_obstacle((3, 1))
    env.add_obstacle((3, 2))
    env.add_obstacle((3, 3))

    # Set the exit point
    env.set_exit((9, 8))

    # Place the hunter (represented by "A") in the environment

    return env

# Create and display the environment
env = create_environment()
env.display()

# Example of Actor in Environment :----------------------------------------------------------------------------

env = create_environment()
# Create an actor and place it in the environment
actor = Actor(position=(1, 1))  # Start the actor at the top-left corner
env.place_actor(actor.position, "A")  # Use "A" to represent the actor
env.display()
# Actors cannot start in an obstacle


# Example usage with predefined moves: -----------------------------------------------------------------------------

# Create the environment
env = create_environment()

# Create an actor and place it in the environment
actor = Actor(position=(1, 1), env)  # Pass the environment instance

# Set predefined moves
predefined_moves = "RRRRRDDDDDD"
actor.set_predefined_moves(predefined_moves)

# Display the initial position
print("Initial Position:")
env.place_actor(actor.position, "A")  # Place the actor's initial position on the grid
env.display()

# Simulate the actor's movement
for step in range(len(predefined_moves)):
    print(f"\nStep {step + 1}:")
    
    # Clear the previous actor position (for visual clarity)
    env.grid[actor.position[1], actor.position[0]] = '.'  # Reset to empty
    
    # Actor takes a step
    actor.step(env)    

    # Place the actor's new position on the grid and display it
    env.place_actor(actor.position, "A")  # Use "A" to represent the actor
    env.display()




# Can we make this dynamic?