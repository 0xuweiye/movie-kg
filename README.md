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

1. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```

2. 启动 Neo4j 数据库，设置你的密码

3. 生成样本数据（或运行爬虫获取 Top250 列表数据）:
   ```bash
   # 先爬取 Top250 列表（列表页可以直接爬取）
   cd crawler && PYTHONPATH=.. python -m scrapy crawl douban
   # 生成包含详情数据的完整数据集
   cd .. && python scripts/generate_sample_data.py
   ```

4. 清洗数据:
   ```bash
   python scripts/clean_data.py
   ```

5. 导入 Neo4j:
   ```bash
   NEO4J_PASS=你的密码 python scripts/import_neo4j.py
   ```

6. 知识推理:
   ```bash
   NEO4J_PASS=你的密码 python scripts/inference.py
   ```

7. 启动后端:
   ```bash
   NEO4J_PASS=你的密码 PYTHONPATH=. python backend/app.py
   ```

8. 访问 http://localhost:5000

## 知识图谱规模

- 电影: 125 部
- 人物: 53 位
- 类型: 17 种
- 关系: 约 280 条（含推理生成的合作关系和相似电影关系）
