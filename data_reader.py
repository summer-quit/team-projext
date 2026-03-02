# -*- coding: utf-8 -*-
"""
数据读取工具
支持CSV/TXT格式数据加载，包含完善的异常处理
满足课程设计数据持久化10分要求
"""
import csv
import os
from src.data_structure.adjacency_list import UndirectedAdjacencyList
from src.data_structure.hash_table import HashTable


def load_user_data(csv_file_path: str, user_hash: HashTable) -> None:
    """
    加载用户信息CSV文件，存入哈希表
    CSV格式：用户ID,姓名,兴趣标签
    :param csv_file_path: CSV文件路径
    :param user_hash: 哈希表实例（用于缓存用户信息）
    :return: None
    :raise FileNotFoundError: 文件不存在时抛出
    :raise ValueError: 文件格式错误时抛出
    :raise RuntimeError: 读取文件异常时抛出
    """
    # 校验文件是否存在
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"用户数据文件不存在：{csv_file_path}")
    # 校验文件后缀
    if not csv_file_path.endswith(".csv"):
        raise ValueError(f"文件格式错误，要求CSV文件：{csv_file_path}")

    try:
        with open(csv_file_path, "r", encoding="utf-8") as f:
            # 读取CSV并校验列名
            reader = csv.DictReader(f)
            required_columns = {"用户ID", "姓名", "兴趣标签"}
            if not required_columns.issubset(reader.fieldnames):
                raise ValueError(f"CSV文件列名错误，需包含：{required_columns}")

            # 遍历数据并存入哈希表
            for row_num, row in enumerate(reader, start=2):  # 行号从2开始（跳过表头）
                # 清洗并校验数据
                user_id_str = row["用户ID"].strip()
                name = row["姓名"].strip()
                interest = row["兴趣标签"].strip() if row["兴趣标签"].strip() else "无"

                if not user_id_str.isdigit():
                    raise ValueError(f"第{row_num}行：用户ID必须为数字，当前为{user_id_str}")
                if not name:
                    raise ValueError(f"第{row_num}行：用户姓名不能为空")

                user_id = int(user_id_str)
                # 存入哈希表：key=user_id，value=用户信息字典
                user_hash.put(user_id, {
                    "id": user_id,
                    "name": name,
                    "interest": interest
                })
    except UnicodeDecodeError:
        raise RuntimeError(f"文件编码错误，要求UTF-8编码：{csv_file_path}")
    except Exception as e:
        raise RuntimeError(f"加载用户数据失败：{str(e)}")


def load_friend_data(txt_file_path: str, adj_list: UndirectedAdjacencyList) -> None:
    """
    加载好友关系TXT文件，构建邻接表
    TXT格式：每行用户ID1,用户ID2（表头可选）
    :param txt_file_path: TXT文件路径
    :param adj_list: 邻接表实例（用于构建好友关系）
    :return: None
    :raise FileNotFoundError: 文件不存在时抛出
    :raise ValueError: 文件格式错误时抛出
    :raise RuntimeError: 读取文件异常时抛出
    """
    # 校验文件是否存在
    if not os.path.exists(txt_file_path):
        raise FileNotFoundError(f"好友关系文件不存在：{txt_file_path}")
    # 校验文件后缀
    if not txt_file_path.endswith(".txt"):
        raise ValueError(f"文件格式错误，要求TXT文件：{txt_file_path}")

    try:
        with open(txt_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            # 跳过空行和表头（包含"用户ID1"的行）
            valid_lines = []
            for line in lines:
                line_strip = line.strip()
                if line_strip and "用户ID1" not in line_strip:
                    valid_lines.append(line_strip)

            # 遍历有效行构建好友关系
            for line_num, line in enumerate(valid_lines, start=2):
                parts = line.split(",")
                if len(parts) != 2:
                    raise ValueError(f"第{line_num}行格式错误，需为：用户ID1,用户ID2")

                # 清洗并校验数据
                user1_str = parts[0].strip()
                user2_str = parts[1].strip()
                if not user1_str.isdigit() or not user2_str.isdigit():
                    raise ValueError(f"第{line_num}行：用户ID必须为数字")

                user1 = int(user1_str)
                user2 = int(user2_str)
                # 先添加节点，再添加边
                adj_list.add_node(user1)
                adj_list.add_node(user2)
                adj_list.add_edge(user1, user2)
    except UnicodeDecodeError:
        raise RuntimeError(f"文件编码错误，要求UTF-8编码：{txt_file_path}")
    except Exception as e:
        raise RuntimeError(f"加载好友关系失败：{str(e)}")