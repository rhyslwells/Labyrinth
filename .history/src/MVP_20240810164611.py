from actor import Actor
from enviroment import Environment

# Example useage of the Environment class :--------------------------------------------------------------------------

def example_of_Environment():
    env = Environment(10, 10)

    # Add some obstacles
    env.add_obstacle((3, 3))
    env.add_obstacle((3, 4))
    env.add_obstacle((3, 5))

    # Set the exit point
    env.set_exit((9, 9))

    # Place the hunter (represented by "A") and prey (represented by "P")
    env.place_actor((0, 0), "A")  # Hunter starts at top-left
    env.place_actor((1, 1), "P")  # Prey starts at (1, 1)
    
    return env

env_ex = example_of_Environment()

# Display the grid
env_ex.display()
# Example usage of the Actor class:

# With random movements:

# env = Environment(5, 5)
# env.add_obstacle((3, 3))
# env.set_exit((5,5))

# print("Initial grid:")
# env.display()
# print("-----------------")

# # Create an actor
# actor = Actor(position=(0, 0))

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

# Example usage with predefined moves:

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
