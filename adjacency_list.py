# -*- coding: utf-8 -*-
"""
无向图邻接表自主实现
支持节点/边的增删查，满足课程设计图结构建模15分要求
禁止调用第三方图相关库，仅使用Python基础类型
"""


class UndirectedAdjacencyList:
    def __init__(self):
        # 邻接表核心存储：{user_id(int): [friend_id1, friend_id2, ...]}
        self.adj_list = dict()

    def add_node(self, user_id: int) -> None:
        """
        添加用户节点
        :param user_id: 用户ID（整型）
        :return: None
        """
        if not isinstance(user_id, int):
            raise TypeError("用户ID必须为整数类型")
        if user_id not in self.adj_list:
            self.adj_list[user_id] = []

    def remove_node(self, user_id: int) -> None:
        """
        删除用户节点，同时删除所有与该节点关联的好友边
        :param user_id: 用户ID（整型）
        :return: None
        :raise ValueError: 用户ID不存在时抛出
        """
        if user_id not in self.adj_list:
            raise ValueError(f"用户ID{user_id}不存在，无法执行删除操作")
        # 删除自身节点
        del self.adj_list[user_id]
        # 遍历所有节点，删除与该节点的关联边
        for key in self.adj_list:
            if user_id in self.adj_list[key]:
                self.adj_list[key].remove(user_id)

    def add_edge(self, user1: int, user2: int) -> None:
        """
        添加好友边（无向），需确保两个节点均已存在
        :param user1: 第一个用户ID
        :param user2: 第二个用户ID
        :return: None
        :raise ValueError: 节点不存在时抛出
        """
        if user1 not in self.adj_list or user2 not in self.adj_list:
            raise ValueError(f"节点{user1}或{user2}不存在，无法添加好友边")
        if user1 == user2:
            raise ValueError("无法为同一用户添加好友边")
        # 避免重复添加边
        if user2 not in self.adj_list[user1]:
            self.adj_list[user1].append(user2)
            self.adj_list[user2].append(user1)

    def remove_edge(self, user1: int, user2: int) -> None:
        """
        删除好友边（无向）
        :param user1: 第一个用户ID
        :param user2: 第二个用户ID
        :return: None
        :raise ValueError: 节点/边不存在时抛出
        """
        if user1 not in self.adj_list or user2 not in self.adj_list:
            raise ValueError(f"节点{user1}或{user2}不存在，无法删除好友边")
        if user2 not in self.adj_list[user1]:
            raise ValueError(f"用户{user1}与{user2}并非好友，无法删除边")
        self.adj_list[user1].remove(user2)
        self.adj_list[user2].remove(user1)

    def get_neighbors(self, user_id: int) -> list:
        """
        获取用户的直接好友（一度人脉）
        :param user_id: 用户ID
        :return: 好友ID列表
        :raise ValueError: 用户ID不存在时抛出
        """
        if user_id not in self.adj_list:
            raise ValueError(f"用户ID{user_id}不存在")
        return self.adj_list[user_id]

    def is_node_exist(self, user_id: int) -> bool:
        """
        判断用户节点是否存在
        :param user_id: 用户ID
        :return: 存在返回True，否则False
        """
        return user_id in self.adj_list

    def get_all_nodes(self) -> list:
        """
        获取所有用户节点ID
        :return: 所有用户ID列表
        """
        return list(self.adj_list.keys())

    def query_edge(self, user1: int, user2: int) -> bool:
        """
        查询两个用户是否为好友（边是否存在）
        :param user1: 第一个用户ID
        :param user2: 第二个用户ID
        :return: 是好友返回True，否则False
        """
        if user1 not in self.adj_list or user2 not in self.adj_list:
            return False
        return user2 in self.adj_list[user1]