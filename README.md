# 影视知识图谱系统

《知识图谱》课程项目 —— 豆瓣电影知识图谱的构建与应用

## 前置要求 (Prerequisites)

- **Python**: 3.9 及以上版本
- **Neo4j**: 5.x 社区版 (Community Edition)

## 配置 (Configuration)

系统通过以下环境变量连接 Neo4j 数据库：

| 环境变量 | 默认值 | 说明 |
|---------|--------|------|
| `NEO4J_URI` | `bolt://localhost:7687` | Neo4j 数据库地址 |
| `NEO4J_USER` | `neo4j` | 数据库用户名 |
| `NEO4J_PASS` | `12345678` | 数据库密码 |

可在启动前通过 `export` (Linux/macOS) 或 `set` (Windows) 设置这些变量。

## 项目结构

- `crawler/` - Scrapy 爬虫模块
- `data/` - 原始数据 (JSON Lines)
- `scripts/` - 数据清洗、Neo4j 导入、知识推理
- `backend/` - Flask REST API + 前端页面
- `static/` - 前端 JS/CSS 静态资源
- `report/` - 项目报告与文档

## 快速开始

1. 创建虚拟环境并激活:
   ```bash
   python -m venv venv
   # Linux/macOS
   source venv/bin/activate
   # Windows
   venv\Scripts\activate
   ```
2. 安装依赖: `pip install -r requirements.txt`
3. 启动 Neo4j 数据库
4. 运行爬虫: `cd crawler && scrapy crawl douban -o ../data/movies.jsonl`
5. 清洗数据: `python scripts/clean_data.py` *(后续任务实现)*
6. 导入 Neo4j: `python scripts/import_neo4j.py` *(后续任务实现)*
7. 知识推理: `python scripts/inference.py` *(后续任务实现)*
8. 启动后端: `python backend/app.py` *(后续任务实现)*
9. 访问 http://localhost:5000
