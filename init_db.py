# 文件名: init_db.py
"""
数据库初始化脚本
独立运行此脚本可以手动初始化数据库
注意: run_crawler.py 会自动初始化数据库，通常不需要单独运行此脚本
"""

import os
from bugs.database import DatabaseManager


def main():
    """主函数"""
    # 确保工作目录在脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)
    
    print("正在初始化数据库...")
    db_manager = DatabaseManager()
    db_manager.init_db()
    print("数据库初始化完成！")
    print("现在你可以运行 run_crawler.py 来开始监控了。")


if __name__ == "__main__":
    main()
