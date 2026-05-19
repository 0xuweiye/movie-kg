"""
知识推理脚本
- 从已有关系推理生成 COLLABORATED_WITH 关系（合作两次及以上的演员/导演之间）
- 推理生成 SIMILAR_TO 关系（共享两个及以上类型的电影之间）
"""
import os
from neo4j import GraphDatabase

NEO4J_URI = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.environ.get('NEO4J_USER', 'neo4j')
NEO4J_PASS = os.environ.get('NEO4J_PASS', '12345678')


def infer_collaborations(session):
    """推理生成人物之间的合作关系"""
    session.run("MATCH ()-[r:COLLABORATED_WITH]-() DELETE r")

    result = session.run("""
        MATCH (p1:Person)-[:ACTS_IN|DIRECTED]->(m:Movie)<-[:ACTS_IN|DIRECTED]-(p2:Person)
        WHERE id(p1) < id(p2)
        WITH p1, p2, count(DISTINCT m) AS collab_count
        WHERE collab_count >= 1
        MERGE (p1)-[r:COLLABORATED_WITH]-(p2)
        SET r.count = collab_count
        RETURN count(r) AS created_count
    """)
    count = result.single()['created_count']
    print(f'COLLABORATED_WITH: {count} relationships created')
    return count


def infer_similar_movies(session):
    """推理生成电影相似度关系（基于共享类型）"""
    session.run("MATCH ()-[r:SIMILAR_TO]-() DELETE r")

    result = session.run("""
        MATCH (m1:Movie)-[:BELONGS_TO]->(g:Genre)<-[:BELONGS_TO]-(m2:Movie)
        WHERE id(m1) < id(m2)
        WITH m1, m2, count(DISTINCT g) AS shared_genres
        WHERE shared_genres >= 2
        MERGE (m1)-[r:SIMILAR_TO]-(m2)
        SET r.genres = shared_genres
        RETURN count(r) AS created_count
    """)
    count = result.single()['created_count']
    print(f'SIMILAR_TO: {count} relationships created')
    return count


def main():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    print(f'Connecting to Neo4j at {NEO4J_URI}...')

    try:
        driver.verify_connectivity()
        print('Connected to Neo4j')
    except Exception as e:
        print(f'Failed to connect: {e}')
        return

    with driver.session() as session:
        print('Inferring COLLABORATED_WITH relationships...')
        collab = infer_collaborations(session)

        print('Inferring SIMILAR_TO relationships...')
        similar = infer_similar_movies(session)

    driver.close()
    print(f'Inference complete: {collab} collaborations, {similar} similar-movie pairs')


if __name__ == '__main__':
    main()
