import numpy as np
import itertools

# Switch times matrix based on your input
switch_times = np.array([
    [0, 6, 7, 10, 4, 2, 5, 2, 8, 1],
    [5, 0, 4, 14, 4, 7, 5, 6, 2, 6],
    [1, 7, 0, 11, 5, 3, 6, 3, 9, 2],
    [6, 6, 5, 0, 4, 7, 3, 4, 8, 7],
    [4, 4, 3, 12, 0, 6, 1, 6, 6, 5],
    [12, 12, 11, 13, 11, 0, 9, 14, 11, 13],
    [3, 3, 2, 11, 7, 5, 0, 5, 5, 4],
    [11, 11, 10, 8, 7, 3, 8, 0, 8, 4],
    [3, 9, 2, 12, 7, 5, 6, 4, 0, 4],
    [7, 7, 6, 9, 3, 1, 4, 9, 9, 0]
])

tasks = [
    [7, 5], [2, 5], [4, 2], [8], [7, 3]
]

def calculate_total_switch_time(tasks, switch_times):
    min_time = float('inf')
    min_order = None
    best_steps = []

    # Assume two slots are available, starting empty
    current_config = [0, 0]  # Only two slots available, start empty

    # Generate all possible permutations of tasks
    for order in itertools.permutations(tasks):
        total_time = 0
        steps = []
        current_config = [0, 0]  # Reset for each permutation

        # Initial setup for the first task
        for i, ink in enumerate(order[0]):
            current_config[i] = ink
        steps.append(f"Initial setup: {current_config}")

        # Calculate switching times between tasks
        for i in range(1, len(order)):
            prev_config = current_config[:]
            next_config = [0, 0]
            for j, ink in enumerate(order[i]):
                next_config[j] = ink

            steps.append(f"Switch from task {prev_config} to {next_config}:")
            # Apply the cartridge switch
            for j in range(2):  # Only two slots
                if prev_config[j] != next_config[j]:
                    if next_config[j] == 0:
                        # No replacement, maintain the previous cartridge if removal not allowed
                        next_config[j] = prev_config[j]
                    else:
                        switch_time = switch_times[prev_config[j]-1][next_config[j]-1]
                        total_time += switch_time
                        steps.append(f"  Switch from cartridge {prev_config[j]} to {next_config[j]} in slot {j+1}, time cost: {switch_time} seconds")

            current_config = next_config[:]

        # Check if this order is better
        if total_time < min_time:
            min_time = total_time
            min_order = order
            best_steps = steps

    return min_time, min_order, best_steps

# Find the minimum switching time and the optimal task order
min_time, min_order, best_steps = calculate_total_switch_time(tasks, switch_times)
print("Minimum Total Switching Time:", min_time)
print("Optimal Task Order:", min_order)
for step in best_steps:
    print(step)
