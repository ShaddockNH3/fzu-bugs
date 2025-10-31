"""福州大学通知公告监控脚本

用于监控各学院和教务处网站的通知公告更新。
支持单次执行和持续监控两种模式。
"""

import os
import sys
import time
import threading
from datetime import datetime

from bugs.config import (
    TARGETS_COLLEGE,
    CRAWL_INTERVAL_SECONDS,
    TARGET_JWC_PAGE,
    JWC_CRAWL_INTERVAL_SECONDS
)
from bugs.database import DatabaseManager
from bugs.crawler import WebCrawler

# 全局锁，用于线程安全的打印和文件操作
_print_lock = threading.Lock()


def save_articles_to_file(articles, filename=None):
    """将文章列表保存到文本文件
    
    参数:
        articles: 文章信息字典列表
        filename: 输出文件名，未指定时自动生成
        
    返回:
        保存的文件名，如果没有文章则返回 None
    """
    if not articles:
        return None
    
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"new_articles_{timestamp}.txt"
    
    with _print_lock:
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
        
        print(f"新文章已保存: {filename}")
    
    return filename


def main_once():
    """执行一次爬取任务"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)
    
    db_manager = DatabaseManager()
    db_manager.init_db()
    
    crawler = WebCrawler(db_manager)
    new_articles = crawler.crawl_all_targets(TARGETS_COLLEGE)
    
    if new_articles:
        save_articles_to_file(new_articles)
    
    return new_articles


def _run_college_monitor():
    """学院通知持续监控"""
    with _print_lock:
        print("[学院监控] 已启动")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)
    
    db_manager = DatabaseManager()
    db_manager.init_db()
    
    while True:
        with _print_lock:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[学院监控 {timestamp}] 开始检查")
        
        crawler = WebCrawler(db_manager, _print_lock)
        new_articles = crawler.crawl_all_targets(TARGETS_COLLEGE)
        
        if new_articles:
            save_articles_to_file(new_articles)
        
        with _print_lock:
            interval_min = CRAWL_INTERVAL_SECONDS / 60
            print(f"[学院监控] 检查完成，{interval_min:.0f}分钟后进行下一轮")
        
        time.sleep(CRAWL_INTERVAL_SECONDS)


def _run_jwc_monitor():
    """教务处通知持续监控"""
    with _print_lock:
        print("[教务处监控] 已启动")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir:
        os.chdir(script_dir)
        
    db_manager = DatabaseManager()
    db_manager.init_db()
    
    while True:
        with _print_lock:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"\n[教务处监控 {timestamp}] 开始检查")
        
        crawler = WebCrawler(db_manager, _print_lock)
        new_articles = crawler.crawl_all_targets(TARGET_JWC_PAGE)
        
        if new_articles:
            save_articles_to_file(new_articles)
        
        with _print_lock:
            interval_min = JWC_CRAWL_INTERVAL_SECONDS / 60
            print(f"[教务处监控] 检查完成，{interval_min:.0f}分钟后进行下一轮")
        
        time.sleep(JWC_CRAWL_INTERVAL_SECONDS)


def main():
    """主入口函数 - 单次或持续监控模式
    
    使用方法:
        python run_crawler.py           # 单次运行模式
        python run_crawler.py --loop    # 持续监控模式
    """
    if len(sys.argv) > 1 and sys.argv[1] == '--loop':
        college_thread = threading.Thread(
            target=_run_college_monitor,
            name="CollegeMonitor",
            daemon=True
        )
        jwc_thread = threading.Thread(
            target=_run_jwc_monitor,
            name="JWCMonitor",
            daemon=True
        )
        
        college_thread.start()
        jwc_thread.start()
        
        try:
            college_thread.join()
            jwc_thread.join()
        except KeyboardInterrupt:
            print("\n程序已中断")
            sys.exit(0)
    else:
        print("开始单次检查...")
        all_targets = TARGETS_COLLEGE + TARGET_JWC_PAGE
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir:
            os.chdir(script_dir)
        
        db_manager = DatabaseManager()
        db_manager.init_db()
        crawler = WebCrawler(db_manager)
        
        new_articles = crawler.crawl_all_targets(all_targets)
        
        if new_articles:
            save_articles_to_file(new_articles)
        
        print(f"检查完成，发现 {len(new_articles)} 篇新文章")
        print("提示: 使用 'python run_crawler.py --loop' 启动持续监控模式")
        
        return new_articles


if __name__ == "__main__":
    main()
