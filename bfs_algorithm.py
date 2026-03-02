# -*- coding: utf-8 -*-
"""
BFS算法自主实现
实现一度/二度人脉查询、社交距离计算+路径回溯
满足课程设计二度人脉发现15分、社交距离计算15分要求
"""
from collections import deque
from src.data_structure.adjacency_list import UndirectedAdjacencyList


def first_degree_friends(adj_list: UndirectedAdjacencyList, user_id: int) -> list:
    """
    一度人脉查询：获取用户直接好友
    :param adj_list: 邻接表实例
    :param user_id: 用户ID
    :return: 直接好友ID列表
    :raise ValueError: 用户ID不存在时抛出
    """
    if not adj_list.is_node_exist(user_id):
        raise ValueError(f"用户ID{user_id}不存在，无法查询一度人脉")
    return adj_list.get_neighbors(user_id)


def second_degree_friends(adj_list: UndirectedAdjacencyList, user_id: int) -> (list, dict):
    """
    二度人脉查询：好友的好友，排除自身和一度人脉
    :param adj_list: 邻接表实例
    :param user_id: 用户ID
    :return: 二度人脉ID列表、连接路径字典{二度人脉ID: 路径字符串}
    :raise ValueError: 用户ID不存在时抛出
    """
    if not adj_list.is_node_exist(user_id):
        raise ValueError(f"用户ID{user_id}不存在，无法查询二度人脉")

    first_degree = set(first_degree_friends(adj_list, user_id))
    second_degree = set()
    path_dict = dict()

    # 遍历一度人脉的好友，筛选二度人脉
    for friend_id in first_degree:
        friend_of_friend = adj_list.get_neighbors(friend_id)
        for fof_id in friend_of_friend:
            # 排除自身、一度人脉
            if fof_id != user_id and fof_id not in first_degree:
                second_degree.add(fof_id)
                # 记录连接路径
                path_dict[fof_id] = f"{user_id}→{friend_id}→{fof_id}"

    return list(second_degree), path_dict


def social_distance(adj_list: UndirectedAdjacencyList, user1: int, user2: int) -> (int, str):
    """
    计算两个用户的最短社交距离，BFS实现+路径回溯
    :param adj_list: 邻接表实例
    :param user1: 第一个用户ID
    :param user2: 第二个用户ID
    :return: 最短距离（整型）、路径字符串
             无关联返回-1和"无社交关联"，同一用户返回0和"用户ID（同一用户）"
    :raise ValueError: 用户ID不存在时抛出
    """
    # 校验用户是否存在
    if not adj_list.is_node_exist(user1):
        raise ValueError(f"用户ID{user1}不存在")
    if not adj_list.is_node_exist(user2):
        raise ValueError(f"用户ID{user2}不存在")
    # 处理同一用户情况
    if user1 == user2:
        return 0, f"{user1}（同一用户）"

    # BFS初始化：队列存储(当前节点, 距离, 路径)，已访问集合避免重复
    visited = set()
    queue = deque()
    queue.append((user1, 0, [user1]))
    visited.add(user1)

    # BFS核心逻辑
    while queue:
        current_node, current_dist, current_path = queue.popleft()
        # 遍历当前节点的所有邻居
        for neighbor in adj_list.get_neighbors(current_node):
            if neighbor not in visited:
                new_path = current_path + [neighbor]
                # 找到目标节点，返回结果
                if neighbor == user2:
                    path_str = "→".join(map(str, new_path))
                    return current_dist + 1, path_str
                visited.add(neighbor)
                queue.append((neighbor, current_dist + 1, new_path))

    # 无社交关联
    return -1, "无社交关联"