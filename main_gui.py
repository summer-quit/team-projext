# -*- coding: utf-8 -*-
"""
Tkinter GUI主界面实现
...
"""
import sys
import os
current_file_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_file_dir, "..", ".."))
sys.path.insert(0, project_root)

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
# 确保这一行存在，导入邻接表类
from src.data_structure.adjacency_list import UndirectedAdjacencyList
from src.data_structure.hash_table import HashTable
from src.algorithm.bfs_algorithm import first_degree_friends, second_degree_friends, social_distance
from src.utils.data_reader import load_user_data, load_friend_data


class SocialNetworkGUI:
    def __init__(self, root: tk.Tk):
        """初始化GUI"""
        self.root = root
        self.root.title("社交网络图谱分析及智能推荐系统")
        self.root.geometry("950x650")
        self.root.resizable(True, True)  # 支持窗口大小调整

        # 初始化核心数据结构
        self.adj_list = UndirectedAdjacencyList()
        self.user_hash = HashTable(capacity=1000)  # 支持1000+用户大数据量

        # 构建界面组件
        self._build_widgets()

    def _build_widgets(self) -> None:
        """构建界面组件，分模块布局"""
        # 整体主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. 数据加载模块
        load_frame = ttk.LabelFrame(main_frame, text="数据加载", padding="10")
        load_frame.pack(fill=tk.X, pady=5)
        ttk.Button(load_frame, text="加载用户CSV", command=self._load_user_csv, width=15).grid(row=0, column=0, padx=5)
        ttk.Button(load_frame, text="加载好友TXT", command=self._load_friend_txt, width=15).grid(row=0, column=1, padx=5)
        ttk.Label(load_frame, text="提示：请先加载用户数据，再加载好友数据").grid(row=0, column=2, padx=10, sticky=tk.W)

        # 2. 一度人脉查询模块
        first_frame = ttk.LabelFrame(main_frame, text="一度人脉查询", padding="10")
        first_frame.pack(fill=tk.X, pady=5)
        ttk.Label(first_frame, text="输入用户ID：").grid(row=0, column=0, padx=5)
        self.first_user_entry = ttk.Entry(first_frame, width=20)
        self.first_user_entry.grid(row=0, column=1, padx=5)
        ttk.Button(first_frame, text="立即查询", command=self._query_first_degree, width=10).grid(row=0, column=2)

        # 3. 二度人脉查询模块
        second_frame = ttk.LabelFrame(main_frame, text="二度人脉查询", padding="10")
        second_frame.pack(fill=tk.X, pady=5)
        ttk.Label(second_frame, text="输入用户ID：").grid(row=0, column=0, padx=5)
        self.second_user_entry = ttk.Entry(second_frame, width=20)
        self.second_user_entry.grid(row=0, column=1, padx=5)
        ttk.Button(second_frame, text="立即查询", command=self._query_second_degree, width=10).grid(row=0, column=2)

        # 4. 社交距离计算模块
        distance_frame = ttk.LabelFrame(main_frame, text="社交距离计算", padding="10")
        distance_frame.pack(fill=tk.X, pady=5)
        ttk.Label(distance_frame, text="用户ID1：").grid(row=0, column=0, padx=5)
        self.dist_user1_entry = ttk.Entry(distance_frame, width=15)
        self.dist_user1_entry.grid(row=0, column=1, padx=5)
        ttk.Label(distance_frame, text="用户ID2：").grid(row=0, column=2, padx=5)
        self.dist_user2_entry = ttk.Entry(distance_frame, width=15)
        self.dist_user2_entry.grid(row=0, column=3, padx=5)
        ttk.Button(distance_frame, text="计算距离", command=self._calc_social_distance, width=10).grid(row=0, column=4)

        # 5. 结果展示模块（带滚动条，占满剩余空间）
        result_frame = ttk.LabelFrame(main_frame, text="结果展示", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # 滚动条
        scroll_y = ttk.Scrollbar(result_frame, orient=tk.VERTICAL)
        scroll_x = ttk.Scrollbar(result_frame, orient=tk.HORIZONTAL)
        # 结果文本框
        self.result_text = tk.Text(
            result_frame,
            font=("宋体", 12),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            wrap=tk.NONE
        )
        # 布局滚动条和文本框
        scroll_y.config(command=self.result_text.yview)
        scroll_x.config(command=self.result_text.xview)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # 6. 清空结果按钮
        ttk.Button(main_frame, text="清空结果", command=self._clear_result, width=15).pack(anchor=tk.E, pady=5)

    def _clear_result(self) -> None:
        """清空结果展示区"""
        self.result_text.delete(1.0, tk.END)

    def _load_user_csv(self) -> None:
        """加载用户CSV文件，带异常提示"""
        try:
            file_path = filedialog.askopenfilename(
                title="选择用户信息CSV文件",
                filetypes=[("CSV文件", "*.csv")]
            )
            if not file_path:
                return
            # 加载数据到哈希表
            load_user_data(file_path, self.user_hash)
            self.result_text.insert(tk.END, f"✅ 成功加载用户数据：{file_path}\n")
            messagebox.showinfo("成功", "用户数据加载完成！")
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.result_text.insert(tk.END, f"❌ 加载用户数据失败：{str(e)}\n")

    def _load_friend_txt(self) -> None:
        """加载好友TXT文件，带异常提示"""
        try:
            file_path = filedialog.askopenfilename(
                title="选择好友关系TXT文件",
                filetypes=[("TXT文件", "*.txt")]
            )
            if not file_path:
                return
            # 加载数据到邻接表
            load_friend_data(file_path, self.adj_list)
            self.result_text.insert(tk.END, f"✅ 成功加载好友数据：{file_path}\n")
            messagebox.showinfo("成功", "好友关系数据加载完成！")
        except Exception as e:
            messagebox.showerror("错误", str(e))
            self.result_text.insert(tk.END, f"❌ 加载好友数据失败：{str(e)}\n")

    def _get_int_id(self, entry: ttk.Entry) -> int or None:
        """输入校验：将输入框内容转为整型ID，失败则提示并返回None"""
        input_str = entry.get().strip()
        if not input_str:
            messagebox.showwarning("警告", "用户ID不能为空！")
            return None
        if not input_str.isdigit():
            messagebox.showwarning("警告", "用户ID必须为正整数！")
            return None
        return int(input_str)

    def _query_first_degree(self) -> None:
        """一度人脉查询逻辑"""
        self._clear_result()
        user_id = self._get_int_id(self.first_user_entry)
        if user_id is None:
            return

        try:
            # 获取一度人脉ID
            friend_ids = first_degree_friends(self.adj_list, user_id)
            # 获取当前用户姓名
            user_info = self.user_hash.get(user_id)
            user_name = user_info["name"] if user_info else "未知姓名"

            # 展示结果
            self.result_text.insert(tk.END, f"===== 一度人脉查询结果（ID：{user_id} | 姓名：{user_name}）=====\n")
            if not friend_ids:
                self.result_text.insert(tk.END, "📌 该用户暂无直接好友\n")
                return
            for fid in friend_ids:
                f_info = self.user_hash.get(fid)
                f_name = f_info["name"] if f_info else "未知姓名"
                self.result_text.insert(tk.END, f"好友ID：{fid} | 姓名：{f_name}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"❌ 查询失败：{str(e)}\n")

    def _query_second_degree(self) -> None:
        """二度人脉查询逻辑"""
        self._clear_result()
        user_id = self._get_int_id(self.second_user_entry)
        if user_id is None:
            return

        try:
            # 获取二度人脉ID和路径
            second_ids, path_dict = second_degree_friends(self.adj_list, user_id)
            # 获取当前用户姓名
            user_info = self.user_hash.get(user_id)
            user_name = user_info["name"] if user_info else "未知姓名"

            # 展示结果
            self.result_text.insert(tk.END, f"===== 二度人脉查询结果（ID：{user_id} | 姓名：{user_name}）=====\n")
            if not second_ids:
                self.result_text.insert(tk.END, "📌 该用户暂无二度人脉\n")
                return
            for sid in second_ids:
                s_info = self.user_hash.get(sid)
                s_name = s_info["name"] if s_info else "未知姓名"
                path = path_dict[sid]
                self.result_text.insert(tk.END, f"二度人脉ID：{sid} | 姓名：{s_name} | 连接路径：{path}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"❌ 查询失败：{str(e)}\n")

    def _calc_social_distance(self) -> None:
        """社交距离计算逻辑"""
        self._clear_result()
        # 获取并校验两个用户ID
        user1 = self._get_int_id(self.dist_user1_entry)
        user2 = self._get_int_id(self.dist_user2_entry)
        if user1 is None or user2 is None:
            return

        try:
            # 计算最短距离和路径
            dist, path = social_distance(self.adj_list, user1, user2)
            # 获取用户姓名
            u1_info = self.user_hash.get(user1)
            u2_info = self.user_hash.get(user2)
            u1_name = u1_info["name"] if u1_info else "未知姓名"
            u2_name = u2_info["name"] if u2_info else "未知姓名"

            # 展示结果
            self.result_text.insert(tk.END, f"===== 社交距离计算结果（{user1}({u1_name}) ↔ {user2}({u2_name})）=====\n")
            self.result_text.insert(tk.END, f"最短社交距离：{dist if dist != -1 else '无'}\n")
            self.result_text.insert(tk.END, f"连接路径：{path}\n")
        except Exception as e:
            self.result_text.insert(tk.END, f"❌ 计算失败：{str(e)}\n")