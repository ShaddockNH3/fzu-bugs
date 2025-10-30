# 文件名: bugs/crawler.py
"""
爬虫模块 - 处理网页抓取和解析
"""

import requests
from lxml import html
from urllib.parse import urljoin
from .config import HEADERS, REQUEST_TIMEOUT
from .database import DatabaseManager


class WebCrawler:
    """网页爬虫类"""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()
        self.page_cache = {}  # 缓存页面内容，避免重复请求
    
    def fetch_page(self, url):
        """
        获取页面内容
        返回: 页面HTML文本，失败返回None
        """
        # 检查缓存
        if url in self.page_cache:
            return self.page_cache[url]
        
        print(f"\n--- 正在请求新页面: {url} ---")
        try:
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            self.page_cache[url] = response.text
            return response.text
        except requests.RequestException as e:
            print(f"错误: 请求页面 {url} 失败: {e}")
            self.page_cache[url] = None
            return None
        except Exception as e:
            print(f"错误: 处理页面 {url} 时发生未知错误: {e}")
            self.page_cache[url] = None
            return None
    
    def parse_section(self, page_content, target):
        """
        解析页面中的特定板块
        page_content: 页面HTML内容
        target: 目标配置字典
        返回: 新文章列表
        """
        college_name = target['college']
        category = target.get('category', '通知公告')
        
        print(f"\n>>> 正在检查学院: {college_name} ({target['url']})")
        
        tree = html.fromstring(page_content)
        items = tree.xpath(target['list_xpath'])
        
        if not items:
            print(f"警告: 在页面上未找到公告列表，请检查XPath: {target['list_xpath']}")
            return []
        
        new_articles = []
        # 从后往前遍历，符合时间顺序
        for item in reversed(items):
            try:
                # 使用配置中指定的正确标题XPath
                title_parts = item.xpath(target['title_xpath'])
                if not title_parts:
                    continue
                
                # .strip() 用于去除首尾空白
                title = title_parts[0].strip()
                if not title:  # 跳过空标题
                    continue

                # **【核心升级】**
                # 智能获取href：如果配置了href_xpath则使用，否则默认使用第一个<a>标签的href
                href_xpath = target.get('href_xpath', './a/@href')
                hrefs = item.xpath(href_xpath)
                
                if not hrefs:
                    print(f"  - 警告: 在公告 '{title[:20]}...' 中未找到链接，请检查 href_xpath: {href_xpath}")
                    continue
                
                relative_url = hrefs[0]
                # 使用配置中指定的 base_url 来拼接链接
                full_url = urljoin(target['base_url'], relative_url)
                
                # 检查并添加文章
                article_info = self.db_manager.check_and_add_article(
                    full_url, title, college_name, category
                )
                if article_info:
                    new_articles.append(article_info)
                    print(f"  [新公告] {college_name} - {title}")
                    # 发送通知
                    self.send_notification(article_info)
                    
            except Exception as e:
                print(f"  解析列表项时出错: {e}")
                continue
        
        if len(new_articles) == 0:
            print("  没有发现新公告。")
        
        return new_articles
    
    def send_notification(self, article_info):
        """
        发送通知的函数。
        【请注意】: 这里只是一个打印示例，你需要替换成你自己的微信/钉钉/邮件等通知实现。
        """
        print("  └── 发送通知...")
        # --- 在下方替换成你的通知代码 ---
        # 示例: send_wechat_message(f"【{article_info['college']}通知】\n标题: {article_info['title']}\n链接: {article_info['url']}")
        pass
        # --- 替换代码结束 ---
    
    def crawl_target(self, target):
        """
        爬取单个目标
        target: 目标配置字典
        返回: 新文章列表，失败返回空列表
        """
        page_content = self.fetch_page(target['url'])
        if page_content is None:
            return []
        
        return self.parse_section(page_content, target)
    
    def crawl_all_targets(self, targets):
        """
        爬取所有目标
        targets: 目标配置列表
        返回: 所有新文章列表
        """
        all_new_articles = []
        for target in targets:
            articles = self.crawl_target(target)
            all_new_articles.extend(articles)
        return all_new_articles
