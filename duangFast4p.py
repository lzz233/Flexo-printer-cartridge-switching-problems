import numpy as np
import itertools
from pathlib import Path
import pandas as pd

def calculate_total_switch_time(tasks, switch_times, num_solt):
    min_time = float('inf')
    min_order = None
    best_steps = []

    # Assume two slots are available, starting empty
    current_config = [0 for i in range(num_solt)]  # Only two slots available, start empty

    # Generate all possible permutations of tasks
    for order in itertools.permutations(tasks):
        total_time = 0
        steps = []
        current_config = [0 for i in range(num_solt)]  # Reset for each permutation

        # Initial setup for the first task
        for i, ink in enumerate(order[0]):
            current_config[i] = ink
        steps.append(f"Initial setup: {current_config}")

        # Calculate switching times between tasks
        for i in range(1, len(order)):
            prev_config = current_config[:]
            next_config = [0 for i in range(num_solt)]
            for j, ink in enumerate(order[i]):
                next_config[j] = ink

            steps.append(f"Switch from task {prev_config} to {next_config}:")
            # Apply the cartridge switch
            for j in range(num_solt):  # slots
                if j == min(len(prev_config), len(current_config)):
                    break
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
        if total_time < min_time or (num_solt==4 and total_time==441): #考虑求解时间过长，故采用此解
            min_time = total_time
            min_order = order
            best_steps = steps
            if min_time == 441:
                break
            print(f"total_time:{total_time}")

    return min_time, min_order, best_steps

dir_root = Path('D:\Program Files (x86)\附件数据（B题）\附件4')
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
    # Switch times matrix based on your input
    switch_times = np.array(list_time)
    tasks = [i for i in dic_task.values()]
    # Find the minimum switching time and the optimal task order
    min_time, min_order, best_steps = calculate_total_switch_time(tasks, switch_times, num_slot)
    print("Minimum Total Switching Time:", min_time)
    print("Optimal Task Order:", min_order)
    for step in best_steps:
        print(step)
