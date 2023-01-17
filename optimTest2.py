import random
import numpy as np
import matplotlib.pyplot as plt

# Define the power of each appliance
power = [1.3,2,1,0.1,0.1,2.2,0.1,1.6,1.2,0.3,3]  # power of each appliance

# Define the power limit of the residence
L = 9000

# Define the minimum allowed consumption
D = 9

# Define the number of particles in the swarm
num_particles = 100

# Define the number of iterations
num_iterations = 1000

# Define the search space
# Each particle represents a schedule
# The schedule is a list of 0s and 1s, where 0 represents off and 1 represents on
search_space = [[random.randint(0, 1) for _ in range(11)] for _ in range(num_particles)]

# Initialize the velocity
velocity = [[0 for _ in range(11)] for _ in range(num_particles)]

# Define a list to store the fitness values
fitness_values = []

counter = 0

# Define the fitness function
def fitness_function(schedule):
    global counter
    if counter >= num_iterations:
        return None
    total_consumption = sum(power[i] * schedule[i] for i in range(11))
    if total_consumption > L or total_consumption < D:
        return float('inf')
    fitness_values.append(total_consumption)
    counter += 1
    return total_consumption
# Initialize the swarm
swarm = search_space    

# Initialize the personal best and global best particle
personal_best = search_space
global_best = min(search_space, key=fitness_function)

# Initialize the personal best and global best fitness to a large number
personal_best_fitness = float('inf')
global_best_fitness = float('inf')

# Define the PSO parameters
c1 = 2
c2 = 2
w = 0.7

# Run the PSO algorithm
for _ in range(num_iterations):
    for i in range(num_particles):
        particle = swarm[i]
        fitness = fitness_function(particle)
        if fitness is None:
            break
        if fitness < personal_best_fitness:
            personal_best[i] = particle
            personal_best_fitness = fitness
        if fitness < global_best_fitness:
            global_best = particle
            global_best_fitness = fitness
        # Update the velocity and position
        for j in range(11):
            velocity[i][j] = w * velocity[i][j] + c1 * random.random() * (personal_best[i][j] - particle[j]) + c2 * random.random() * (global_best[j] - particle[j])
            particle[j] += velocity[i][j]
            

# The global best particle is the optimal schedule
schedule = global_best

# Display the schedule
hour_map = {i: f'{i % 24}:00' for i in range(24)}
for i in range(11):
    print(f'Appliance {i+1}: {"On" if schedule[i] else "Off"} at {hour_map[i]}')

# Create a list of hours
hours = [hour_map[i] for i in range(24)]

# Create a list of status for each appliance
status = [1 if schedule[i] else 0 for i in range(11)]


power = np.resize(power, (264,))
new_status = np.repeat(status, 24) * power
new_status = np.resize(new_status, (24,))

# Create the bar chart
# fig, ax = plt.subplots()
# colors = ["green" if s else "red" for s in status]
# for i in range(11):
#     ax.barh(i, new_status[i], color=colors[i])
# ax.set_yticklabels(hours)
# ax.set_xlabel('Appliance Status')
# ax.set_title('Appliance schedule')
# plt.show()

# Plot the results
plt.plot(range(num_iterations), fitness_values)
plt.xlabel('Iterations')
plt.ylabel('Total consumption')
plt.title('PSO optimization results')
plt.show()
