from pathlib import Path
import pandas as pd
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
        print("hellow")

    print("hellow")