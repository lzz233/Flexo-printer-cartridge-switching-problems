# Leon
# date:2024/6/2
from pathlib import Path
import pandas as pd
def minimize_transition_count(tasks):
    min_transitions = 0
    current_config = tasks[0]

    print(f"Initial ink configuration: {current_config}")

    for i in range(1, len(tasks)):
        prev_config = current_config
        current_config = tasks[i]

        print(f"Transition from Task {i} inks {prev_config} to Task {i + 1} inks {current_config}:")

        transitions = 0
        for slot, (prev_ink, current_ink) in enumerate(zip(prev_config, current_config), start=1):
            if prev_ink != current_ink:
                transitions += 1
                print(f"  Slot {slot}: Replace ink {prev_ink} with ink {current_ink}")

        min_transitions += transitions

        print(f"  Total transitions for this step: {transitions}")

    return min_transitions



dir_root = Path('D:\pythonProject\附件数据（B题）\附件1')
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
    time_ink = {}
    for i in range(0, num_ink):
        time_ink[f'list{i}'] = [None]
    for index, row in books1.iterrows():
        task = row['包装种类编号']
        dic_task[task] = eval(row['所需墨盒编号'])
    list_time = [i for i in time_ink.values()]
    # Task sequences, assuming each sub-list is a task with specific inks in order
    tasks = [i for i in dic_task.values()]
    total_min_cost = minimize_transition_count(tasks)
    print(f"Minimum total transition time: {total_min_cost} seconds")