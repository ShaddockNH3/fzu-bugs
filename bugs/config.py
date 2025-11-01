"""福州大学通知公告爬虫配置文件"""

# 数据库配置
DB_NAME = "announcements.db"
TABLE_NAME = "seen_announcements"

# HTTP 请求配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
REQUEST_TIMEOUT = 20

# Webhook 通知配置
ENABLE_WEBHOOK_NOTIFICATION = False  # 设置为 True 开启HTTP通知
NOTIFICATION_WEBHOOK_URL = "http://example.com/webhook"

# 爬取间隔时间
JWC_CRAWL_INTERVAL_SECONDS = 60 * 1
CRAWL_INTERVAL_SECONDS = 60 * 60

# 教务处目标配置
TARGET_JWC_PAGE = [
    {
        'college': '教务处',
        'base_url': 'https://jwch.fzu.edu.cn/',
        'url': 'https://jwch.fzu.edu.cn/jxtz.htm',
        'list_xpath': "//ul[@class='list-gl']/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '教务通知'
    }
]

# 学院通知公告目标配置
TARGET_ANNOUNCEMENT_PAGES = [
    {
        'college': '电气工程与自动化学院', 
        'base_url': 'https://dqxy.fzu.edu.cn/',
        'url': 'https://dqxy.fzu.edu.cn/tzgg.htm',
        'list_xpath': "//div[@class='r-content']/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '通知公告'
    },
    {
        'college': '机械工程及自动化学院',
        'base_url': 'https://jxxy.fzu.edu.cn/',
        'url': 'https://jxxy.fzu.edu.cn/fwzn/tzgg.htm',
        'list_xpath': "//div[@class='ny-list']/ul/li",
        'title_xpath': "./a/text()",
        'href_xpath': "./a/@href",
        'category': '通知公告'
    },
    {
        'college': '数学与统计学院',
        'base_url': 'https://math.fzu.edu.cn/',
        'url': 'https://math.fzu.edu.cn/xydt/tzgg.htm',
        'list_xpath': "//div[contains(@class, 'new_list3')]/dl/dd",
        'title_xpath': "./a[2]/@title",
        'href_xpath': "./a[2]/@href",
        'category': '通知公告'
    },
    {
        'college': '化工学院',
        'base_url': 'https://che.fzu.edu.cn/',
        'url': 'https://che.fzu.edu.cn/xytz.htm',
        'list_xpath': "//div[span[@class='ovh']]",
        'title_xpath': ".//a/@title",
        'href_xpath': ".//a/@href",
        'category': '通知公告'
    },
    {
        'college': '土木工程学院',
        'base_url': 'https://civil.fzu.edu.cn/',
        'url': 'https://civil.fzu.edu.cn/tzgg.htm',
        'list_xpath': "//section[contains(@class, 'n_list01')]/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '通知公告'
    },
     {
        'college': '环境与安全工程学院',
        'base_url': 'https://es.fzu.edu.cn/',
        'url': 'https://es.fzu.edu.cn/index/tzgg.htm',
        'list_xpath': "//div[@class='list']/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '通知公告'
    },
    {
        'college': '经济与管理学院',
        'base_url': 'https://jgxy.fzu.edu.cn/',
        'url': 'https://jgxy.fzu.edu.cn/tzgg.htm',
        'list_xpath': "//section[@class='TextList bgss']//ul/li", 
        'title_xpath': "./a/p/text()", 
        'href_xpath': "./a/@href",
        'category': '通知公告'
    },
    {
        'college': '生物科学与工程学院',
        'base_url': 'https://bio.fzu.edu.cn/',
        'url': 'https://bio.fzu.edu.cn/tzgg.htm',
        'list_xpath': "//div[@class='list_main_content']/ul/li", 
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '通知公告'
    },
    {
        'college': '外国语学院',
        'base_url': 'https://sfl.fzu.edu.cn/',
        'url': 'https://sfl.fzu.edu.cn/index/tzgg.htm',
        'list_xpath': "//div[@class='notice']/ul/li",
        'title_xpath': "./a/text()",
        'href_xpath': "./a/@href",
        'category': '通知公告'
    },
    {
        'college': '外国语学院',
        'base_url': 'https://sfl.fzu.edu.cn/',
        'url': 'https://sfl.fzu.edu.cn/index/xygs.htm',
        'list_xpath': "//div[@class='notice']/ul/li",
        'title_xpath': "./a/text()",
        'href_xpath': "./a/@href",
        'category': '学院公示'
    },
    {
        'college': '计算机与大数据学院',
        'base_url': 'https://ccds.fzu.edu.cn/',
        'url': 'https://ccds.fzu.edu.cn/xwzx/xytz.htm',
        'list_xpath': "//div[contains(@class, 'new_list3')]/dl/dd",
        'title_xpath': "./a[2]/@title",
        'href_xpath': "./a[2]/@href",
        'category': '通知公告'
    },
        {
        'college': '物理与信息工程学院',
        'base_url': 'https://wx.fzu.edu.cn/',
        'url': 'https://wx.fzu.edu.cn/tzgg/xytz.htm',
        'list_xpath': "//div[@class='text-list']/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '通知公告'
    },
    {
        'college': '化学学院',
        'base_url': 'https://chem.fzu.edu.cn/',
        'url': 'https://chem.fzu.edu.cn/xwzx/tzgg.htm',
        'list_xpath': "//ul[@class='txtList']/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '通知公告'
    },
    # 建筑学院没有“通知公告”
    {
        'college': '紫金地质与矿业学院',
        'base_url': 'https://zjxy.fzu.edu.cn/',
        'url': 'https://zjxy.fzu.edu.cn/tzgg.htm',
        'list_xpath': "//div[@class='wznr']/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '通知公告'
    },
    # 厦门工艺美院不是本部，不考虑
    {
        'college': '材料科学与工程学院',
        'base_url': 'https://cl.fzu.edu.cn/',
        'url': 'https://cl.fzu.edu.cn/gsgg.htm',
        'list_xpath': "//ul[@class='rightejlst']/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '通知公告'
    },
    {
        'college': '材料科学与工程学院',
        'base_url': 'https://cl.fzu.edu.cn/',
        'url': 'https://cl.fzu.edu.cn/tzwj.htm',
        'list_xpath': "//ul[@class='rightejlst']/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '通知文件'
    },
    {
        'college': '法学院',
        'base_url': 'https://law.fzu.edu.cn/',
        'url': 'https://law.fzu.edu.cn/ggtz.htm',
        'list_xpath': "//div[@class='body1']/ul/li",
        'title_xpath': ".//a/@title",
        'href_xpath': ".//a/@href",
        'category': '通知公告'
    },
    # 至诚学院不是本部，不考虑
    # 先进制造学院不是本部，不考虑
    # 继续教育学院不知道是什么，不考虑
    # 马克思主义学院为研究生学院，不考虑
    {
        'college': '人文社会科学学院',
        'base_url': 'https://renwen.fzu.edu.cn/',
        'url': 'https://renwen.fzu.edu.cn/tzgg.htm',
        'list_xpath': "//div[@class='list-text']/ul/li",
        'title_xpath': ".//div[@class='text']/p/text()",
        'href_xpath': "./a/@href",
        'category': '通知公告'
    },
    # 梅努斯国际工程学院不是本部，不考虑
    {
        'college': '医学院',
        'base_url': 'https://med.fzu.edu.cn/',
        'url': 'https://med.fzu.edu.cn/index/xytz.htm',
        'list_xpath': "//div[@class='newlist1']/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '学院通知'
    },
    {
        'college': '医学院',
        'base_url': 'https://med.fzu.edu.cn/',
        'url': 'https://med.fzu.edu.cn/index/jxtz.htm',
        'list_xpath': "//div[@class='newlist1']/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '教学通知'
    },
    # 未来膜学院没有自己官网
    # 医工交叉研学院为研究生学院，不考虑
    # 体育教学研究部非学生，不考虑
]

# 本科教学页面
TARGET_UNDERGRAD_PAGES = [
    {
        'college': '化工学院',
        'base_url': 'https://che.fzu.edu.cn/',
        'url': 'https://che.fzu.edu.cn/jyjx/bksjy.htm',
        'list_xpath': "//div[span[@class='ovh']]",
        'title_xpath': ".//a/@title",
        'href_xpath': ".//a/@href",
        'category': '本科生教育'
    },
    {
        'college': '环境与安全工程学院',
        'base_url': 'https://es.fzu.edu.cn/',
        'url': 'https://es.fzu.edu.cn/rcpy/bksjy.htm',
        'list_xpath': "//div[@class='list']/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '本科生教育'
    },
    {
        'college': '生物科学与工程学院',
        'base_url': 'https://bio.fzu.edu.cn/',
        'url': 'https://bio.fzu.edu.cn/rcpy.htm',
        'list_xpath': "//div[@class='list_main_content']/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '本科生教育'
    },
    {
        'college': '物理与信息工程学院',
        'base_url': 'https://wx.fzu.edu.cn/',
        'url': 'https://wx.fzu.edu.cn/rcpy/bkspy/bksjx.htm',
        'list_xpath': "//div[@class='text-list']/ul/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '本科生教育'
    },
    {
        'college': '化学学院',
        'base_url': 'https://chem.fzu.edu.cn/',
        'url': 'https://chem.fzu.edu.cn/rcpy/bksjy/bksjxggl.htm',
        'list_xpath': "//ul[@class='txtList']/li",
        'title_xpath': "./a/@title",
        'href_xpath': "./a/@href",
        'category': '本科生教育'
    },
    {
        'college': '建筑与城乡规划学院',
        'base_url': 'https://jzxy.fzu.edu.cn/',
        'url': 'https://jzxy.fzu.edu.cn/rcpy1/bkspydt.htm',
        'list_xpath': "//div[@class='text-list']/ul[@class='tdate-list']/li",
        'title_xpath': "./a/text()[1]",
        'href_xpath': "./a/@href",
        'category': '本科生教育'
    },
    {
        'college': '法学院',
        'base_url': 'https://law.fzu.edu.cn/',
        'url': 'https://law.fzu.edu.cn/jx2/bks.htm',
        'list_xpath': "//div[@class='body1']/ul/li",
        'title_xpath': ".//a/@title",
        'href_xpath': ".//a/@href",
        'category': '本科生教育'
    },
    {
        'college': '人文社会科学学院',
        'base_url': 'https://renwen.fzu.edu.cn/',
        'url': 'https://renwen.fzu.edu.cn/jyjx/bksjx.htm',
        'list_xpath': "//div[@class='list-text']/ul/li",
        'title_xpath': ".//div[@class='text']/p/text()",
        'href_xpath': "./a/@href",
        'category': '本科生教育'
    },
]

TARGETS_COLLEGE = TARGET_ANNOUNCEMENT_PAGES + TARGET_UNDERGRAD_PAGES
