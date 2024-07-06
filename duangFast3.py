import numpy as np

# Updated switch times matrix
switch_times = np.array([
    [0, 3, 7, 25, 22],
    [8, 0, 12, 26, 24],
    [7, 6, 0, 28, 20],
    [8, 11, 8, 0, 26],
    [11, 10, 16, 8, 0]
])


def minimize_transition_times(tasks, switch_times):
    # Initialize the minimum cost with 0 as there's no transition before the first task
    min_cost = 0
    current_config = tasks[0]

    # Print initial configuration
    print(f"Initial ink configuration: {current_config}")

    # Iterate over tasks to calculate transitions
    for i in range(1, len(tasks)):
        prev_config = current_config
        current_config = tasks[i]
        transition_cost = 0

        print(f"Transition from Task {i} inks {prev_config} to Task {i + 1} inks {current_config}:")

        # Calculate the cost to switch from previous task inks to current task inks
        for j in range(len(prev_config)):
            if prev_config[j] != current_config[j]:
                cost = switch_times[prev_config[j] - 1][current_config[j] - 1]
                transition_cost += cost
                print(f"  Switch from ink {prev_config[j]} to ink {current_config[j]} in slot {j + 1}: {cost} seconds")

        min_cost += transition_cost
        print(f"  Total transition cost for this step: {transition_cost} seconds")

    return min_cost


# Task sequences, assuming each sub-list is a task with specific inks in order
tasks = [[3, 2], [2, 1], [1, 3], [3, 1], [2, 3]]

# Calculate the minimum transition times
total_min_cost = minimize_transition_times(tasks, switch_times)
print(f"Minimum total transition time: {total_min_cost} seconds")
