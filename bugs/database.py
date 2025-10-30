# 文件名: bugs/database.py
"""
数据库模块 - 处理所有数据库相关操作
"""

import sqlite3
from datetime import datetime
from .config import DB_NAME, TABLE_NAME


class DatabaseManager:
    """数据库管理类"""
    
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.table_name = TABLE_NAME
    
    def init_db(self):
        """初始化数据库，创建表（如果不存在）"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            college TEXT NOT NULL,
            category TEXT NOT NULL,
            first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()
        conn.close()
        print(f"数据库 '{self.db_name}' 初始化成功")
    
    def is_article_seen(self, url):
        """检查URL是否已在数据库中"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT url FROM {self.table_name} WHERE url = ?", (url,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def add_article(self, url, title, college, category):
        """添加新文章到数据库"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"INSERT INTO {self.table_name} (url, title, college, category) VALUES (?, ?, ?, ?)", 
                (url, title, college, category)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # URL已存在
            return False
        finally:
            conn.close()
    
    def check_and_add_article(self, url, title, college, category):
        """
        检查URL是否已存在，如果不存在则添加到数据库并返回文章信息
        返回: 新文章信息字典，如果已存在则返回None
        """
        if self.is_article_seen(url):
            return None
        
        # 添加到数据库
        self.add_article(url, title, college, category)
        
        # 返回文章信息
        now_str = datetime.now().strftime('%Y-%m-%d-%H-%M')
        return {
            'time': now_str,
            'college': college,
            'category': category,
            'title': title,
            'url': url
        }

