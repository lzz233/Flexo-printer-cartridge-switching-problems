import numpy as np
import itertools

def switch_cartridges_two_cleaners(tasks, switch_times):
    min_time = float('inf')
    optimal_order = None
    detailed_steps = []

    # Generate all permutations of tasks and calculate switching times for each
    for permutation in itertools.permutations(tasks):
        current_config = [0, 0]  # Assume two slots, both initially empty
        total_time = 0
        steps = []

        steps.append(f"Initial cartridge setup: {permutation[0]}")
        current_config = list(permutation[0])  # Start with the first task's cartridges

        # Iterate over task transitions
        for i in range(1, len(permutation)):
            prev_task = permutation[i - 1]
            current_task = permutation[i]
            times = []

            steps.append(f"State before switching from {prev_task} to {current_task}: {current_config}")
            # Assuming two slots, calculate the necessary changes
            for j in range(2):
                if prev_task[j] != current_task[j]:
                    time = switch_times[prev_task[j]-1][current_task[j]-1]
                    times.append(time)
                    steps.append(f"  Switch from cartridge {prev_task[j]} to {current_task[j]} in slot {j+1}, time cost: {time} seconds")

            # Take the maximum time as the step time for parallel execution
            if times:
                max_time = max(times)
                total_time += max_time

            current_config = list(current_task)  # Update current configuration after the switch
            steps.append(f"State after switching to {current_task}: {current_config}")

        # Check if the current permutation is better than what we've seen before
        if total_time < min_time:
            min_time = total_time
            optimal_order = permutation
            detailed_steps = steps  # Save the detailed steps of the optimal order

    print(f"Optimal order: {optimal_order} with minimum switching time: {min_time} seconds")
    for step in detailed_steps:
        print(step)
    return optimal_order, min_time, detailed_steps

# Example tasks and switch times matrix, assuming 1-based index for tasks
tasks = [[4, 1], [2, 1], [4, 3], [3, 2], [2, 4]]
switch_times = np.array([
    [0, 1, 6, 1, 10],
    [9, 0, 5, 10, 9],
    [9, 10, 0, 6, 4],
    [3, 4, 9, 0, 13],
    [5, 6, 11, 2, 0]
])

# Call the function to find the optimal order of tasks
switch_cartridges_two_cleaners(tasks, switch_times)
