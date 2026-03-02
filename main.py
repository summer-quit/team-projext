"""
程序入口
启动社交网络图谱分析及智能推荐系统GUI
Python 3.7+ 可直接运行，无第三方依赖
"""
import sys
import os

# 获取当前文件所在目录（即 src 目录）
current_file_dir = os.path.dirname(os.path.abspath(__file__))
# 项目根目录是 src 的上级目录
project_root = os.path.abspath(os.path.join(current_file_dir, ".."))
# 把项目根目录加到 sys.path 最前面，让 Python 能找到 src 模块
sys.path.insert(0, project_root)

import tkinter as tk
from src.gui.main_gui import SocialNetworkGUI

if __name__ == "__main__":
    # 初始化Tk根窗口
    root = tk.Tk()
    # 启动GUI应用
    app = SocialNetworkGUI(root)
    # 主事件循环
    root.mainloop()