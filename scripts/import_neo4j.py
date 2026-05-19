"""
知识图谱 Neo4j 导入脚本
- 从 movies_cleaned.jsonl 和 persons_cleaned.jsonl 读取数据
- 使用 neo4j 官方驱动导入 Neo4j
- 创建节点、关系、索引、约束
- 实现基于 douban_id 的实体对齐（知识融合）
"""
import json
import os
from neo4j import GraphDatabase

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

NEO4J_URI = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.environ.get('NEO4J_USER', 'neo4j')
NEO4J_PASS = os.environ.get('NEO4J_PASS', '12345678')


class Neo4jImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def setup_schema(self):
        """创建索引和唯一约束"""
        queries = [
            'CREATE INDEX movie_title IF NOT EXISTS FOR (m:Movie) ON (m.title)',
            'CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name)',
            'CREATE CONSTRAINT movie_douban_id IF NOT EXISTS FOR (m:Movie) REQUIRE m.douban_id IS UNIQUE',
            'CREATE CONSTRAINT person_douban_id IF NOT EXISTS FOR (p:Person) REQUIRE p.douban_id IS UNIQUE',
            'CREATE CONSTRAINT genre_name IF NOT EXISTS FOR (g:Genre) REQUIRE g.name IS UNIQUE',
            'CREATE CONSTRAINT country_name IF NOT EXISTS FOR (c:Country) REQUIRE c.name IS UNIQUE',
            'CREATE CONSTRAINT language_name IF NOT EXISTS FOR (l:Language) REQUIRE l.name IS UNIQUE',
        ]
        with self.driver.session() as session:
            for q in queries:
                try:
                    session.run(q)
                    print(f'  Schema: {q.split(" IF ")[0].strip()}... OK')
                except Exception as e:
                    print(f'  Schema warning: {e}')

    def import_movie(self, movie_data):
        """导入单个 Movie 节点及关联的 Year, Genre, Country, Language 节点和关系"""
        mid = movie_data['douban_id']
        title = movie_data['title']
        year = movie_data['year']
        rating = movie_data['rating']
        duration = movie_data['duration']
        summary = (movie_data.get('summary') or '')[:200]
        poster = movie_data.get('poster_url') or ''

        with self.driver.session() as session:
            # MERGE Movie 节点（知识融合：实体对齐）
            session.run("""
                MERGE (m:Movie {douban_id: $id})
                SET m.title = $title, m.year = $year, m.rating = $rating,
                    m.duration = $duration, m.summary = $summary, m.poster_url = $poster
            """, id=mid, title=title, year=year, rating=rating,
                 duration=duration, summary=summary, poster=poster)

            # Year 节点
            if year:
                session.run("""
                    MATCH (m:Movie {douban_id: $mid})
                    MERGE (y:Year {value: $year})
                    MERGE (m)-[:RELEASED_IN]->(y)
                """, mid=mid, year=year)

            # Genre 节点
            for g_name in (movie_data.get('genres') or []):
                session.run("""
                    MATCH (m:Movie {douban_id: $mid})
                    MERGE (g:Genre {name: $name})
                    MERGE (m)-[:BELONGS_TO]->(g)
                """, mid=mid, name=g_name)

            # Country 节点
            for c_name in (movie_data.get('countries') or []):
                session.run("""
                    MATCH (m:Movie {douban_id: $mid})
                    MERGE (c:Country {name: $name})
                    MERGE (m)-[:PRODUCED_IN]->(c)
                """, mid=mid, name=c_name)

            # Language 节点
            for l_name in (movie_data.get('languages') or []):
                session.run("""
                    MATCH (m:Movie {douban_id: $mid})
                    MERGE (l:Language {name: $name})
                    MERGE (m)-[:IN_LANGUAGE]->(l)
                """, mid=mid, name=l_name)

    def import_person(self, person_data):
        """导入单个 Person 节点（MERGE on douban_id => 知识融合: 实体对齐 + 属性合并）"""
        pid = person_data['douban_id']
        name = person_data['name']
        alias = person_data.get('alias') or ''
        gender = person_data.get('gender') or ''
        birth_year = person_data.get('birth_year')
        birthplace = person_data.get('birthplace') or ''

        with self.driver.session() as session:
            session.run("""
                MERGE (p:Person {douban_id: $id})
                SET p.name = CASE WHEN $name IS NOT NULL AND $name <> '' THEN $name ELSE p.name END,
                    p.alias = CASE WHEN $alias IS NOT NULL AND $alias <> '' THEN $alias ELSE p.alias END,
                    p.gender = CASE WHEN $gender IS NOT NULL AND $gender <> '' THEN $gender ELSE p.gender END,
                    p.birth_year = coalesce($birth_year, p.birth_year),
                    p.birthplace = CASE WHEN $birthplace IS NOT NULL AND $birthplace <> '' THEN $birthplace ELSE p.birthplace END
            """, id=pid, name=name, alias=alias, gender=gender,
                 birth_year=birth_year, birthplace=birthplace)

    def import_relationships(self, movie_data):
        """导入 Person-Movie 关系：ACTS_IN, DIRECTED, WROTE"""
        mid = movie_data['douban_id']

        with self.driver.session() as session:
            for director in (movie_data.get('directors') or []):
                if not director.get('douban_id'):
                    continue
                session.run("""
                    MATCH (p:Person {douban_id: $pid})
                    MATCH (m:Movie {douban_id: $mid})
                    MERGE (p)-[:DIRECTED]->(m)
                """, pid=director['douban_id'], mid=mid)

            for writer in (movie_data.get('writers') or []):
                if not writer.get('douban_id'):
                    continue
                session.run("""
                    MATCH (p:Person {douban_id: $pid})
                    MATCH (m:Movie {douban_id: $mid})
                    MERGE (p)-[:WROTE]->(m)
                """, pid=writer['douban_id'], mid=mid)

            for actor in (movie_data.get('actors') or []):
                if not actor.get('douban_id'):
                    continue
                role_name = actor.get('role_name') or ''
                session.run("""
                    MATCH (p:Person {douban_id: $pid})
                    MATCH (m:Movie {douban_id: $mid})
                    MERGE (p)-[r:ACTS_IN]->(m)
                    SET r.role_name = $role_name
                """, pid=actor['douban_id'], mid=mid, role_name=role_name)

    def run(self):
        print(f'Connecting to Neo4j at {NEO4J_URI}...')
        try:
            self.driver.verify_connectivity()
            print('Connected to Neo4j')
        except Exception as e:
            print(f'Failed to connect: {e}')
            return

        print('Setting up schema...')
        self.setup_schema()

        movies_path = os.path.join(DATA_DIR, 'movies_cleaned.jsonl')
        persons_path = os.path.join(DATA_DIR, 'persons_cleaned.jsonl')

        # 导入 Person 节点
        person_count = 0
        if os.path.exists(persons_path):
            print('Importing persons...')
            with open(persons_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        person_data = json.loads(line.strip())
                        self.import_person(person_data)
                        person_count += 1
                        if person_count % 100 == 0:
                            print(f'  {person_count} persons imported')
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f'  Skip invalid person record: {e}')
            print(f'Total: {person_count} persons')

        # 导入 Movie 节点及关系
        movie_count = 0
        if os.path.exists(movies_path):
            print('Importing movies...')
            with open(movies_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        movie_data = json.loads(line.strip())
                        if not movie_data.get('title'):
                            continue
                        self.import_movie(movie_data)
                        self.import_relationships(movie_data)
                        movie_count += 1
                        if movie_count % 50 == 0:
                            print(f'  {movie_count} movies imported')
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f'  Skip invalid movie record: {e}')
            print(f'Total: {movie_count} movies')

        print(f'Import complete: {movie_count} movies, {person_count} persons')
        self.close()


def main():
    importer = Neo4jImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASS)
    importer.run()


if __name__ == '__main__':
    main()
