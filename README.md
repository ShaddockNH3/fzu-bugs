# fzu-bugs - 福州大学通知公告监控爬虫

一个用于自动监控福州大学教务处及各学院官网通知公告更新的 Python 爬虫工具。

> **重要提示**：本项目的所有爬虫功能都需要在福州大学**校园网**环境下，或连接**福大VPN**后才能正常运行。

## ✨ 功能特性

* ✅ **全面监控**：自动爬取教务处及多个学院的“通知公告”和“本科生教育”等页面。
* ✅ **智能去重**：内置数据库记录已爬取的文章，确保每次运行只推送新通知。
* ✅ **双模运行**：支持【单次检查】和【持续监控】两种模式，灵活应对不同需求。
* ✅ **独立线程**：在持续监控模式下，教务处和学院的监控在不同线程中独立运行，互不干扰。
* ✅ **高度可配**：

  * 可自定义不同目标的爬取频率。
  * 可限制爬虫只在特定时间段工作（例如：仅在 7:00 - 18:00 运行）。
  * 支持通过 HTTP Webhook 推送新通知（仅持续监控模式）。

## 🚀 快速开始

### 1. 准备环境

首先，请确保你的电脑上安装了 Python 3。

```bash
# 克隆项目（或者直接下载压缩包）
git clone https://github.com/ShaddockNH3/fzu-bugs.git
cd fzu-bugs

# 创建并激活 Python 虚拟环境
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

本项目依赖 `requests` 和 `lxml`。

```bash
pip install requests lxml
```

### 3. 初始化数据库

首次使用时，请先以**单次模式**运行一次脚本。这将自动为你创建并初始化 `announcements.db` 数据库文件，为后续监控做准备。

```bash
python run_crawler.py
```

> 运行后，你会在项目根目录下看到 `announcements.db` 文件。如果检查到了新通知，还会生成一个 `new_articles_*.txt` 文件。

### 4. 个性化配置

初始化完成后，打开 `bugs/config.py` 文件，根据你的需求修改配置。例如，你可以：

* 调整爬取频率（`JWC_CRAWL_INTERVAL_SECONDS` 和 `CRAWL_INTERVAL_SECONDS`）。
* 设置爬虫的工作时间段（`ENABLE_TIME_RESTRICTION`）。
* 启用并配置 Webhook 推送（`ENABLE_WEBHOOK_NOTIFICATION`）。

### 5. 启动持续监控

完成所有配置后，使用 `--loop` 参数启动**持续监控模式**。程序将在后台为你自动刷新通知。

```bash
python run_crawler.py --loop
```

按 `Ctrl+C` 可以停止监控。

## ⚙️ 配置说明

所有配置项均位于 `bugs/config.py` 文件中，你可以根据自己的需求进行修改。

#### 爬取间隔配置

可以为教务处和学院设置不同的检查频率。

```python
# bugs/config.py

# 教务处爬取间隔（秒），例如 60 * 1 表示每分钟一次
JWC_CRAWL_INTERVAL_SECONDS = 60 * 1
# 学院爬取间隔（秒），例如 60 * 60 表示每小时一次
CRAWL_INTERVAL_SECONDS = 60 * 60
```

#### 时间限制配置（仅对`--loop`模式生效）

让爬虫只在指定的时间段内活动。

```python
# bugs/config.py

# 是否启用时间限制
ENABLE_TIME_RESTRICTION = True
# 开始爬取的小时（24小时制，包含）
CRAWL_START_HOUR = 7
# 结束爬取的小时（24小时制，不包含），例如18代表运行到17:59
CRAWL_END_HOUR = 18
```

> 当 `ENABLE_TIME_RESTRICTION` 设置为 `True` 时，爬虫只会在 `CRAWL_START_HOUR` 和 `CRAWL_END_HOUR` 之间的时间段内执行爬取任务。在其他时间，程序会处于等待状态。

#### HTTP Webhook 通知配置（仅对`--loop`模式生效）

在新文章发现时，通过 HTTP POST 请求发送通知，可用于接入 Server酱、企业微信机器人等。

```python
# bugs/config.py

# 是否开启HTTP通知
ENABLE_WEBHOOK_NOTIFICATION = False
# 你的 Webhook URL
NOTIFICATION_WEBHOOK_URL = "http://your-webhook-url.com/api/notify"
```

**通知的JSON格式如下**：

```json
{
    "title": "【学院名称】这里是通知的标题",
    "content": "这里是通知的原始URL"
}
```

## 🎯 监控范围

### 教务处

* 教学通知：`https://jwch.fzu.edu.cn/jxtz.htm`

### 学院

默认配置监控以下学院的“通知公告”或“本科生教育”页面：

* 电气工程与自动化学院
* 机械工程及自动化学院
* 数学与统计学院
* 化工学院
* 土木工程学院
* 环境与安全工程学院
* 经济与管理学院
* 生物科学与工程学院
* 外国语学院
* 计算机与大数据学院
* 物理与信息工程学院
* 化学学院
* 紫金地质与矿业学院
* 材料科学与工程学院
* 法学院
* 人文社会科学学院

> 你可以通过修改 `bugs/config.py` 中的 `TARGETS_COLLEGE` 列表来添加、删除或修改监控目标。

## 📁 项目结构

```
fzu-bugs/
├── bugs/                      # 核心模块
│   ├── __init__.py
│   ├── config.py             # 配置文件（重要！）
│   ├── crawler.py            # 爬虫逻辑
│   └── database.py           # 数据库操作
├── run_crawler.py            # 主运行脚本
├── init_db.py                # 数据库初始化脚本（可选，主程序会自动调用）
├── announcements.db          # SQLite数据库（自动生成）
├── new_articles_*.txt        # 新文章记录文件（自动生成）
└── README.md                 # 本文件
```

## 📄 输出格式示例

新发现的文章将会被保存在项目根目录下的 `new_articles_YYYYMMDD_HHMMSS.txt` 文件中。

```
福州大学通知爬取结果
生成时间: 2025-11-02 14:30:00
共 2 篇新文章
============================================================

2025-11-02-14-30
教务处 - 教务通知
关于2024-2025学年第一学期期末考试安排的通知
https://jwch.fzu.edu.cn/info/1062/12345.htm
------------------------------------------------------------

2025-11-02-14-30
电气工程与自动化学院 - 通知公告
关于开展学院奖学金评选工作的通知
https://dqxy.fzu.edu.cn/info/1234/5678.htm
------------------------------------------------------------
```

## ❓ 常见问题 (FAQ)

**Q: 需要手动运行 `init_db.py` 吗？**
A: 不需要。首次运行 `run_crawler.py` 时，程序会自动检查并创建数据库和表。

**Q: 如何只在白天运行爬虫？**
A: 编辑 `bugs/config.py`，设置 `ENABLE_TIME_RESTRICTION = True`，并根据需要调整 `CRAWL_START_HOUR` 和 `CRAWL_END_HOUR`。

**Q: 单次检查模式 (`python run_crawler.py`) 会发送HTTP通知吗？**
A: 不会。HTTP Webhook 通知仅在持续监控模式 (`--loop`) 下生效。

**Q: 为什么有些学院没有被包含？**
A: 默认配置主要针对福大本部与本科生相关的学院。你可以根据 [监控范围](#🎯-监控范围) 的说明，自行在 `bugs/config.py` 中添加其他学院或页面。

## 📜 许可证

本项目采用 MIT 许可证。

---

**开发者**: ShaddockNH3
**项目地址**: [https://github.com/ShaddockNH3/fzu-bugs](https://github.com/ShaddockNH3/fzu-bugs)
