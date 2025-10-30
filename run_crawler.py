# 文件名: run_crawler.py
# -*- coding: utf-8 -*-
"""
福州大学通知公告监控脚本
用于监控各学院网站的通知公告更新
"""

import os
import time
from datetime import datetime
from bugs.config import TARGET_ANNOUNCEMENT_PAGES, CRAWL_INTERVAL_SECONDS
from bugs.database import DatabaseManager
from bugs.crawler import WebCrawler


def save_articles_to_file(articles, filename=None):
    """
    将文章列表保存到txt文件
    articles: 文章信息列表
    filename: 文件名，如果不指定则自动生成
    """
    if not articles:
        return None
    
    # 如果没有指定文件名，使用时间戳生成
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"new_articles_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"福州大学通知爬取结果\n")
        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"共 {len(articles)} 篇新文章\n")
        f.write("=" * 60 + "\n\n")
        
        for article in articles:
            f.write(f"{article['time']}\n")
            f.write(f"{article['college']} - {article['category']}\n")
            f.write(f"{article['title']}\n")
            f.write(f"{article['url']}\n")
            f.write("-" * 60 + "\n\n")
    
    print(f"\n新文章已保存到文件: {filename}")
    return filename


def main_once():
    """执行一次爬取任务"""
    # 确保工作目录在脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)
    
    # 初始化数据库管理器
    db_manager = DatabaseManager()
    db_manager.init_db()
    
    # 初始化爬虫
    crawler = WebCrawler(db_manager)
    
    # 执行爬取，获取新文章列表
    new_articles = crawler.crawl_all_targets(TARGET_ANNOUNCEMENT_PAGES)
    
    # 保存到文件（如果有新文章）
    if new_articles:
        save_articles_to_file(new_articles)
    
    return new_articles


def main_loop():
    """持续监控模式 - 定时执行爬取"""
    print("--- 通知公告监控脚本已启动 (持续监控模式) ---")
    
    # 确保工作目录在脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)
    
    # 初始化数据库
    db_manager = DatabaseManager()
    db_manager.init_db()
    
    while True:
        print(f"\n--- {time.strftime('%Y-%m-%d %H:%M:%S')} 开始新一轮检查 ---")
        
        # 初始化爬虫（每轮重新创建以清空缓存）
        crawler = WebCrawler(db_manager)
        
        # 执行爬取
        new_articles = crawler.crawl_all_targets(TARGET_ANNOUNCEMENT_PAGES)
        
        # 保存到文件（如果有新文章）
        if new_articles:
            save_articles_to_file(new_articles)
        
        print(f"\n--- 本轮检查结束，将在 {CRAWL_INTERVAL_SECONDS / 60} 分钟后进行下一轮检查 ---")
        time.sleep(CRAWL_INTERVAL_SECONDS)


def main():
    """主函数 - 根据需要选择单次或循环模式"""
    import sys
    
    # 如果带参数 --loop 则进入循环模式
    if len(sys.argv) > 1 and sys.argv[1] == '--loop':
        main_loop()
    else:
        # 默认执行一次
        print("======== 开始执行更新检查 (单次模式) ========")
        new_articles = main_once()
        print(f"\n======== 本次检查完成，共发现 {len(new_articles)} 篇新文章 ========")
        print("\n提示: 使用 'python run_crawler.py --loop' 可以启动持续监控模式")
        return new_articles


if __name__ == "__main__":
    main()
