import numpy as np
from pathlib import Path
import pandas as pd

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
            if j == min(len(prev_config), len(current_config)):
                break
            prev_ink = prev_config[j]
            current_ink = current_config[j]
            if prev_ink != current_ink:
                cost = switch_times[prev_ink - 1][current_ink - 1]
                transition_cost += cost
                print(f"  Switch from ink {prev_ink} to ink {current_ink} in slot {j + 1}: {cost} seconds")

        min_cost += transition_cost
        print(f"  Total transition cost for this step: {transition_cost} seconds")

    return min_cost



dir_root = Path('D:\pythonProject\附件数据（B题）\附件2')
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
    # Updated switch times matrix
    switch_times = np.array(list_time)
    # Task sequences, assuming each sub-list is a task with specific inks in order
    tasks = [i for i in dic_task.values()]
    # Calculate the minimum transition times
    total_min_cost = 0
    total_min_cost = minimize_transition_times(tasks, switch_times)
    print(f"Minimum total transition time: {total_min_cost} seconds")

