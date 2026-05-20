# 影视知识图谱系统

《知识图谱》课程项目 —— 豆瓣电影知识图谱的构建与应用

## 项目概述

本项目构建了一个覆盖 **知识表示、图谱构建、知识融合、知识存储、智能应用** 五个环节的完整影视领域知识图谱系统。数据来源于豆瓣电影 Top250，使用 Neo4j 图数据库存储，提供基于 D3.js 的力导向图可视化和多维搜索、筛选、推荐、路径分析等智能应用。

## 前置要求

- **Python**: 3.9 及以上版本
- **Neo4j**: 5.x 社区版 (Community Edition)

## 配置

系统通过以下环境变量连接 Neo4j 数据库：

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `NEO4J_URI` | `bolt://localhost:7687` | Neo4j 数据库地址 |
| `NEO4J_USER` | `neo4j` | 数据库用户名 |
| `NEO4J_PASS` | — | 数据库密码（必填） |

## 项目结构

```
movie-kg/
├── crawler/                     # Scrapy 爬虫模块
│   ├── spiders/douban_spider.py # 豆瓣 Top250 爬虫
│   ├── items.py                 # MovieItem + PersonItem 定义
│   ├── settings.py              # 爬虫配置
│   └── middlewares.py           # UA轮换 + Cookie轮换
├── data/                        # 原始数据 (JSON Lines)
├── scripts/                     # 数据处理脚本
│   ├── generate_sample_data.py  # 生成样本数据
│   ├── clean_data.py            # 数据清洗与去重
│   ├── import_neo4j.py          # Neo4j 导入与实体对齐
│   └── inference.py             # 知识推理
├── backend/                     # Flask 后端
│   ├── app.py                   # 应用入口
│   ├── routes/search.py         # 搜索 + 筛选 API
│   ├── routes/graph.py          # 图谱子图 + 路径 API
│   ├── routes/recommend.py      # 推荐 API
│   └── templates/index.html     # 前端单页
├── static/                      # 前端静态资源
│   ├── css/style.css
│   └── js/
│       ├── graph.js             # D3.js 力导向图
│       ├── search.js            # 搜索交互
│       ├── recommend.js         # 推荐交互
│       └── app.js               # 主入口
├── report/                      # 课程报告
├── requirements.txt
└── README.md
```

## 知识图谱本体

### 实体类型 (6 种)

| 实体 | 标签 | 核心属性 |
|------|------|---------|
| 电影 | Movie | title, year, rating, duration, summary, douban_id |
| 人物 | Person | name, gender, birth_year, birthplace, douban_id |
| 类型 | Genre | name |
| 国家/地区 | Country | name |
| 语言 | Language | name |
| 年份 | Year | value |

### 关系类型 (8 种)

| 关系 | 方向 | 说明 |
|------|------|------|
| ACTS_IN | Person → Movie | 演员出演 |
| DIRECTED | Person → Movie | 导演执导 |
| WROTE | Person → Movie | 编剧创作 |
| BELONGS_TO | Movie → Genre | 电影类型 |
| PRODUCED_IN | Movie → Country | 制片国家 |
| IN_LANGUAGE | Movie → Language | 电影语言 |
| RELEASED_IN | Movie → Year | 上映年份 |
| COLLABORATED_WITH | Person ↔ Person | 合作关系（推理生成） |
| SIMILAR_TO | Movie ↔ Movie | 电影相似度（推理生成） |

## 知识图谱规模

| 指标 | 数量 |
|------|------|
| 电影节点 | 157 |
| 人物节点 | 128 |
| 类型节点 | 21 |
| 总关系数 | 896 |
| 其中 COLLABORATED_WITH | 172 |
| 其中 SIMILAR_TO | 208 |

## 智能应用功能

- **力导向图可视化**：D3.js 实现，支持缩放/拖拽/点击展开，实体类型颜色区分与分区布局
- **关系筛选**：支持切换"人物关系 / 属性关系 / 全部关系"三种视图
- **多维搜索**：电影名/人名关键词搜索，按类型/年份/国家分面筛选
- **电影推荐**：基于类型的相似推荐 + 基于合作网络的推荐
- **关系路径分析**：任意两实体间最短路径查询，图谱上高亮显示

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 Neo4j 数据库

# 3. 爬取 Top250 列表 + 生成详情数据
cd crawler && PYTHONPATH=.. python -m scrapy crawl douban
cd .. && python scripts/generate_sample_data.py

# 4. 清洗数据
python scripts/clean_data.py

# 5. 导入 Neo4j（含实体对齐与属性融合）
NEO4J_PASS=你的密码 python scripts/import_neo4j.py

# 6. 知识推理（生成合作关系与电影相似度）
NEO4J_PASS=你的密码 python scripts/inference.py

# 7. 启动 Web 应用
NEO4J_PASS=你的密码 PYTHONPATH=. python backend/app.py

# 8. 浏览器访问
# http://localhost:5000
```

## 技术栈

| 层次 | 技术 |
|------|------|
| 爬虫 | Scrapy, BeautifulSoup, fake-useragent |
| 数据库 | Neo4j 5.x Community Edition |
| 数据库驱动 | neo4j (official Python driver) |
| 后端 | Flask, Flask-CORS |
| 可视化 | D3.js v7, ECharts |
