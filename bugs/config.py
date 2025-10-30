# 文件名: bugs/config.py
"""
配置文件 - 集中管理所有爬虫配置
"""

# 数据库配置
DB_NAME = "announcements.db"
TABLE_NAME = "seen_announcements"

# 请求配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
REQUEST_TIMEOUT = 20

# 爬虫和通知配置
CRAWL_INTERVAL_SECONDS = 60 * 10  # 每10分钟检查一次

# 目标：各学院的"通知公告"页面
TARGET_ANNOUNCEMENT_PAGES = [
    {
        'college': '电气工程与自动化学院', 
        'base_url': 'https://dqxy.fzu.edu.cn/',
        'url': 'https://dqxy.fzu.edu.cn/tzgg.htm',
        'list_xpath': "//div[@class='r-content']/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",  # 明确指定链接的xpath
        'category': '通知公告'
    },
    {
        'college': '机械工程及自动化学院',
        'base_url': 'https://jxxy.fzu.edu.cn/',
        'url': 'https://jxxy.fzu.edu.cn/fwzn/tzgg.htm',
        'list_xpath': "//div[@class='ny-list']/ul/li",
        'title_xpath': "./a/text()",
        'href_xpath': "./a/@href",  # 明确指定链接的xpath
        'category': '通知公告'
    },
    {
        'college': '数学与统计学院',
        'base_url': 'https://math.fzu.edu.cn/',
        'url': 'https://math.fzu.edu.cn/xydt/tzgg.htm',
        'list_xpath': "//div[contains(@class, 'new_list3')]/dl/dd",
        'title_xpath': "./a[2]/@title",  # 第二个a标签的title属性
        'href_xpath': "./a[2]/@href",   # 第二个a标签的href属性
        'category': '通知公告'
    },
    {
        'college': '化工学院',
        'base_url': 'https://che.fzu.edu.cn/',
        'url': 'https://che.fzu.edu.cn/xytz.htm',
        'list_xpath': "//div[span[@class='ovh']]",
        'title_xpath': ".//a/@title",
        'href_xpath': ".//a/@href",
    },
    {
        'college': '土木工程学院',
        'base_url': 'https://civil.fzu.edu.cn/',
        'url': 'https://civil.fzu.edu.cn/tzgg.htm',
        'list_xpath': "//section[contains(@class, 'n_list01')]/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
    },
     {
        'college': '环境与安全工程学院',
        'base_url': 'https://es.fzu.edu.cn/',
        'url': 'https://es.fzu.edu.cn/index/tzgg.htm',
        'list_xpath': "//div[@class='list']/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
    },
    {
    'college': '经济与管理学院',
    'base_url': 'https://jgxy.fzu.edu.cn/',
    'url': 'https://jgxy.fzu.edu.cn/tzgg.htm',
    'list_xpath': "//section[@class='TextList bgss']//ul/li", 
    'title_xpath': "./a/p/text()", 
    'href_xpath': "./a/@href",
    },

]

# 为了兼容性，保留TARGETS别名
TARGETS = TARGET_ANNOUNCEMENT_PAGES

