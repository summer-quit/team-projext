# -*- coding: utf-8 -*-
"""
哈希表自主实现（链地址法处理哈希冲突）
用于缓存用户信息，以用户ID为键，查询时间复杂度接近O(1)
满足课程设计用户信息管理10分要求
"""


class HashNode:
    """哈希表链表节点"""
    def __init__(self, key: int, value: dict):
        self.key = key  # 键：用户ID（整型）
        self.value = value  # 值：用户信息字典{id, name, interest}
        self.next = None  # 下一个节点指针


class HashTable:
    def __init__(self, capacity: int = 1000):
        """
        初始化哈希表
        :param capacity: 哈希表桶容量，默认1000（支持大数据量）
        """
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("哈希表容量必须为正整数")
        self.capacity = capacity
        # 桶数组：每个元素为链表头节点，初始化为None
        self.buckets = [None] * self.capacity

    def _hash(self, key: int) -> int:
        """
        哈希函数：除留余数法，将用户ID映射到桶索引
        :param key: 用户ID
        :return: 桶索引（整型）
        """
        return int(key) % self.capacity

    def put(self, key: int, value: dict) -> None:
        """
        插入/更新用户信息
        :param key: 用户ID
        :param value: 用户信息字典
        :return: None
        """
        if not isinstance(key, int):
            raise TypeError("用户ID必须为整数类型")
        index = self._hash(key)
        current = self.buckets[index]

        # 若key已存在，更新对应value
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next

        # 若key不存在，头插法添加新节点
        new_node = HashNode(key, value)
        new_node.next = self.buckets[index]
        self.buckets[index] = new_node

    def get(self, key: int) -> dict or None:
        """
        查询用户信息
        :param key: 用户ID
        :return: 用户信息字典，不存在返回None
        """
        if not isinstance(key, int):
            return None
        index = self._hash(key)
        current = self.buckets[index]

        # 遍历链表查询key
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def remove(self, key: int) -> None:
        """
        删除用户信息
        :param key: 用户ID
        :return: None
        """
        if not isinstance(key, int) or key not in self:
            return
        index = self._hash(key)
        current = self.buckets[index]
        prev = None

        # 遍历链表找到目标节点并删除
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.buckets[index] = current.next
                return
            prev = current
            current = current.next

    def __contains__(self, key: int) -> bool:
        """
        重写in运算符，判断key是否存在
        :param key: 用户ID
        :return: 存在返回True，否则False
        """
        return self.get(key) is not None

    def get_all_keys(self) -> list:
        """
        获取哈希表中所有用户ID
        :return: 用户ID列表
        """
        keys = []
        for bucket in self.buckets:
            current = bucket
            while current:
                keys.append(current.key)
                current = current.next
        return keys