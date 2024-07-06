import itertools


def dp_ink_management(tasks, max_slots):
    max_ink_id = 10  # 假设墨盒编号从1到10
    all_inks = range(1, max_ink_id + 1)

    # 初始化DP表，dp[i][config]表示前i个任务执行后的墨盒配置为config时的最小更换次数
    dp = [{} for _ in range(len(tasks) + 1)]
    initial_config = tuple([0] * max_slots)
    dp[0][initial_config] = 0

    # 动态规划过程
    for i in range(1, len(tasks) + 1):
        required_inks = set(tasks[i - 1])
        for prev_config, prev_cost in dp[i - 1].items():
            for new_config in itertools.product([0] + list(all_inks), repeat=max_slots):
                new_config_set = set(new_config) - {0}
                if required_inks.issubset(new_config_set):
                    # 确保单次操作不拔出墨盒（只允许添加或替换）
                    if all(y != 0 or x == 0 for x, y in zip(prev_config, new_config)):
                        # 计算切换成本
                        transition_cost = sum(
                            1 for x, y in zip(prev_config, new_config) if x != y and x != 0 and y != 0)
                        new_cost = prev_cost + transition_cost
                        new_config_tuple = tuple(new_config)
                        if new_config_tuple not in dp[i] or new_cost < dp[i][new_config_tuple]:
                            dp[i][new_config_tuple] = new_cost

    # 找到最后一个任务完成时的最小成本
    final_cost = float('inf')
    final_config = None
    for config, cost in dp[len(tasks)].items():
        if cost < final_cost:
            final_cost = cost
            final_config = config

    return final_cost, reconstruct_path(dp, final_config, tasks, max_slots)


def reconstruct_path(dp, final_config, tasks, max_slots):
    path = [final_config]
    current_config = final_config

    for i in range(len(tasks), 0, -1):
        required_inks = set(tasks[i - 1])
        for prev_config, prev_cost in dp[i - 1].items():
            if required_inks.issubset(set(current_config) - {0}):
                # 确保单次操作不拔出墨盒（只允许添加或替换）
                if all(y != 0 or x == 0 for x, y in zip(prev_config, current_config)):
                    transition_cost = sum(
                        1 for x, y in zip(prev_config, current_config) if x != y and x != 0 and y != 0)
                    if dp[i][current_config] == prev_cost + transition_cost:
                        path.append(prev_config)
                        current_config = prev_config
                        break

    return path[::-1]


def print_best_path(best_path):
    if not best_path:
        print("No solution found.")
        return

    print("Optimal path to solution with detailed ink changes:")
    for i in range(1, len(best_path)):
        prev_config, curr_config = best_path[i - 1], best_path[i]
        changes = []
        for j, (prev_ink, curr_ink) in enumerate(zip(prev_config, curr_config)):
            if prev_ink != curr_ink:
                if prev_ink == 0 and curr_ink != 0:
                    changes.append(f"Add ink {curr_ink} to slot {j + 1}")
                elif prev_ink != 0 and curr_ink != 0:
                    changes.append(f"Change from ink {prev_ink} to {curr_ink} in slot {j + 1}")
        print(f"Step {i}: From {prev_config} to {curr_config}")
        for change in changes:
            print(f"  {change}")


# 示例使用
tasks = [[7, 5], [2, 5], [4, 2], [8], [7, 3]]
max_slots = 2
# tasks = [[2, 7], [3, 8, 6], [7, 9], [6, 9], [4], [2, 6], [7, 3, 1]]
# max_slots = 3
best_cost, best_path = dp_ink_management(tasks, max_slots)
print("Minimum changes with Dynamic Programming:", best_cost)
print_best_path(best_path)
