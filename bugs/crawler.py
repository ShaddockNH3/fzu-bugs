"""网页爬虫模块，用于抓取和解析通知公告"""

import requests
from lxml import html
from urllib.parse import urljoin

from .config import HEADERS, REQUEST_TIMEOUT
from .database import DatabaseManager


class WebCrawler:
    """大学通知公告爬虫
    
    参数:
        db_manager: 数据库管理器实例
        print_lock: 线程锁，用于线程安全打印
    """
    
    def __init__(self, db_manager=None, print_lock=None):
        self.db_manager = db_manager or DatabaseManager()
        self.page_cache = {}
        self.print_lock = print_lock
    
    def _print(self, msg):
        """线程安全的打印包装器"""
        if self.print_lock:
            with self.print_lock:
                print(msg)
        else:
            print(msg)
    
    def fetch_page(self, url):
        """获取页面内容并缓存
        
        参数:
            url: 目标 URL
            
        返回:
            页面 HTML 文本，失败时返回 None
        """
        if url in self.page_cache:
            return self.page_cache[url]
        
        self._print(f"正在请求: {url}")
        
        try:
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            self.page_cache[url] = response.text
            return response.text
        except requests.RequestException as e:
            self._print(f"请求失败 {url}: {e}")
            self.page_cache[url] = None
            return None
        except Exception as e:
            self._print(f"未知错误 {url}: {e}")
            self.page_cache[url] = None
            return None
    
    def parse_section(self, page_content, target):
        """从页面内容中解析通知公告
        
        参数:
            page_content: 页面 HTML 内容
            target: 目标配置字典
            
        返回:
            新文章列表
        """
        college_name = target['college']
        category = target.get('category', '通知公告')
        
        self._print(f"检查: {college_name}")
        
        tree = html.fromstring(page_content)
        items = tree.xpath(target['list_xpath'])
        
        if not items:
            self._print(f"警告: 未找到公告列表 (XPath: {target['list_xpath']})")
            return []
        
        new_articles = []
        
        for item in reversed(items):
            try:
                title_parts = item.xpath(target['title_xpath'])
                if not title_parts:
                    continue
                
                title = title_parts[0].strip()
                if not title:
                    continue

                href_xpath = target.get('href_xpath', './a/@href')
                hrefs = item.xpath(href_xpath)
                
                if not hrefs:
                    self._print(f"警告: 未找到链接 '{title[:20]}...'")
                    continue
                
                relative_url = hrefs[0]
                full_url = urljoin(target['base_url'], relative_url)
                
                article_info = self.db_manager.check_and_add_article(
                    full_url, title, college_name, category
                )
                
                if article_info:
                    new_articles.append(article_info)
                    self._print(f"  [新] {college_name}: {title}")
                    self.send_notification(article_info)
                    
            except Exception as e:
                self._print(f"解析错误: {e}")
                continue
        
        if not new_articles:
            self._print(f"  {college_name}: 无新公告")
        
        return new_articles
    
    def send_notification(self, article_info):
        """发送新文章通知
        
        参数:
            article_info: 文章信息字典
            
        注意:
            这是一个占位符，需要替换为实际的通知逻辑
            (微信、钉钉、邮件等)
        """
        pass
    
    def crawl_target(self, target):
        """爬取单个目标
        
        参数:
            target: 目标配置字典
            
        返回:
            新文章列表，失败时返回空列表
        """
        page_content = self.fetch_page(target['url'])
        if page_content is None:
            return []
        
        return self.parse_section(page_content, target)
    
    def crawl_all_targets(self, targets):
        """爬取所有配置的目标
        
        参数:
            targets: 目标配置列表
            
        返回:
            所有新文章的合并列表
        """
        all_new_articles = []
        for target in targets:
            articles = self.crawl_target(target)
            all_new_articles.extend(articles)
        return all_new_articles
