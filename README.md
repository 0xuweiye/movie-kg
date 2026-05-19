# 影视知识图谱系统

《知识图谱》课程项目 —— 豆瓣电影知识图谱的构建与应用

## 项目结构

- `crawler/` - Scrapy 爬虫模块
- `data/` - 原始数据 (JSON Lines)
- `scripts/` - 数据清洗、Neo4j 导入、知识推理
- `backend/` - Flask REST API + 前端页面
- `static/` - 前端 JS/CSS 静态资源

## 快速开始

1. 安装依赖: `pip install -r requirements.txt`
2. 启动 Neo4j 数据库
3. 运行爬虫: `cd crawler && scrapy crawl douban -o ../data/movies.jsonl`
4. 清洗数据: `python scripts/clean_data.py`
5. 导入 Neo4j: `python scripts/import_neo4j.py`
6. 知识推理: `python scripts/inference.py`
7. 启动后端: `python backend/app.py`
8. 访问 http://localhost:5000
