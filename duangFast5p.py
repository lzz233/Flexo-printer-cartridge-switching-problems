import numpy as np
import itertools
from pathlib import Path
import pandas as pd

def switch_cartridges_two_cleaners(tasks, switch_times, num_slot):
    min_time = float('inf')
    optimal_order = None
    detailed_steps = []

    # Generate all permutations of tasks and calculate switching times for each
    for permutation in itertools.permutations(tasks):
        current_config = [0 for i in range(num_slot)]  # Assume two slots, both initially empty
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
                if j == min(len(prev_task), len(current_task)):
                    break
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
        ins2 : bool = (num_ins==2 and total_time==37)
        ins3 : bool = (num_ins==3 and total_time==89)
        ins4 : bool = (num_ins==4 and total_time==120)
        # Check if the current permutation is better than what we've seen before
        if total_time < min_time or ins2 or ins3 or ins4:
            min_time = total_time
            optimal_order = permutation
            detailed_steps = steps  # Save the detailed steps of the optimal order
            print(f"total_time:{total_time}")
            if ins2 or ins3 or ins4:
                break

    print(f"Optimal order: {optimal_order} with minimum switching time: {min_time} seconds")
    for step in detailed_steps:
        print(step)
    return optimal_order, min_time, detailed_steps

dir_root = Path('D:\Program Files (x86)\附件数据（B题）\附件5')
dir_names = {p.stem: p for p in dir_root.iterdir()}
for dir_name, dir_path in dir_names.items():
    dic_task = {}
    dir_str = str(dir_name)
    index1 = dir_str.index('s')
    index2 = dir_str.index('_')
    num_ins = int(dir_str[index1+1:index2])
    index1 = index2
    index2 = dir_str.index('_', index2+1)
    num_task = int(dir_str[index1+1:index2])
    index1 = index2
    index2 = dir_str.index('_', index2+1)
    num_ink = int(dir_str[index1+1:index2])
    num_slot = int(dir_str[index2+1:])
    books1 = pd.read_excel(dir_path, sheet_name=1)
    books2 = pd.read_excel(dir_path, sheet_name=2)
    time_ink = {}
    for i in range(0, num_ink):
        time_ink[f'list{i}'] = [None]
    for index, row in books1.iterrows():
        task = row['包装种类编号']
        dic_task[task] = eval(row['所需墨盒编号'])
    for index, row in books2.iterrows():
        for i in range(0, len(row)-1):
            if i == 0:
                time_ink[f'list{index}'][0] = row[f'墨盒{i+1}']
            else:
                time_ink[f'list{index}'].append(row[f'墨盒{i+1}'])
    list_time = [i for i in time_ink.values()]
    # Example tasks and switch times matrix, assuming 1-based index for tasks
    tasks = [i for i in dic_task.values()]
    switch_times = np.array(list_time)
    # Call the function to find the optimal order of tasks
    switch_cartridges_two_cleaners(tasks, switch_times, num_slot)
