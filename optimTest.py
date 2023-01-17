import random

# Define the number of particles in the swarm
num_particles = 100

# Define the number of iterations
num_iterations = 1000

# Define the consumption of each appliance
# The consumption of each appliance is given
consumption = [5, 10, 15, 20, 5, 10, 15, 20, 5, 10, 15, 20, 5, 10, 15, 20, 5, 10, 15, 20, 5, 10, 15, 20]

# Define the search space
# Each particle represents a schedule
# The schedule is a list of 0s and 1s, where 0 represents off and 1 represents on
search_space = [[random.randint(0, 1) for _ in range(24)] for _ in range(num_particles)]

# Initialize the velocity
velocity = [[0 for _ in range(24)] for _ in range(num_particles)]

# Define the fitness function
# In this case, the fitness function is the total consumption of the city
def fitness_function(schedule):
    total_consumption = sum(consumption[i] for i in range(24) if schedule[i] == 1)
    return total_consumption

# Initialize the swarm
swarm = search_space

# Initialize the personal best and global best particle
personal_best = search_space
global_best = min(search_space, key=fitness_function)

# Define the PSO parameters
c1 = 2
c2 = 2
w = 0.7

# Run the PSO algorithm
for _ in range(num_iterations):
    for i in range(num_particles):
        # Update the velocity
        velocity[i] = [w * velocity[i][j] + c1 * random.random() * (personal_best[i][j] - swarm[i][j]) + c2 * random.random() * (global_best[j] - swarm[i][j]) for j in range(24)]
        # Update the position
        swarm[i] = [min(max(round(swarm[i][j] + velocity[i][j]), 0), 1) for j in range(24)]
        # Update the personal best
        if fitness_function(swarm[i]) < fitness_function(personal_best[i]):
            personal_best[i] = swarm[i]
        # Update the global best
        if fitness_function(swarm[i]) < fitness_function(global_best):
            global_best = swarm[i]

# Return the best schedule
best_schedule = global_best

