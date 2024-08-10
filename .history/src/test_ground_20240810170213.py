from actor import Actor
from enviroment import Environment

# Example useage of the Environment class :--------------------------------------------------------------------------

def create_environment():
    # Initialize the environment
    env = Environment(10, 10)

    # Add some obstacles
    env.add_obstacle((3, 3))
    env.add_obstacle((3, 4))
    env.add_obstacle((3, 5))

    # Set the exit point
    env.set_exit((9, 9))

    # Place the hunter (represented by "A") in the environment

    return env

# Create and display the environment
env = create_environment()
env.display()

# Example usage of the Actor class :----------------------------------------------------------------------------

env = create_environment()

# Create an actor and place it in the environment
actor = Actor(position=(0, 0))  # Start the actor at the top-left corner


# Simulate the actor's movement
for step in range(2):
    print(f"\nStep {step}:")

    # Clear the previous actor position (for visual clarity)
    env.grid[actor.position[1], actor.position[0]] = '.'  # Reset to empty
    
    if step != 0:
        # Actor takes a step
        actor.step(env)    

    # Place the actor's new position on the grid and display it
    env.place_actor(actor.position, "A")  # Use "A" to represent the actor
    env.display()


# Example usage with predefined moves: -----------------------------------------------------------------------------

# env = Environment(10, 10)
# env.add_obstacle((3, 3))
# env.set_exit((9, 9))

# print("Initial grid:")
# env.display()

# # Create an actor
# actor = Actor(position=(0, 0))

# # Set predefined moves: right, down, right, down
# actor.set_predefined_moves([(1, 0), (1,0), (1, 0), (0, 1)])

# # Run a few steps and display the grid
# for step in range(5):
#     print(f"Step {step + 1}:")
    
#     # Clear the previous actor position (for visual clarity)
#     env.grid[actor.position[1], actor.position[0]] = 0
    
#     # Actor takes a step
#     actor.step(env)
    
#     # Place the actor's new position on the grid and display it
#     env.place_actor(actor.position, 3)  # Use 3 to represent the actor
#     env.display()
