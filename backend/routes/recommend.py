from flask import Blueprint, request, jsonify, current_app

recommend_bp = Blueprint('recommend', __name__)


def get_driver():
    return current_app.config['get_db']()


@recommend_bp.route('/recommend/similar/<douban_id>')
def similar_movies(douban_id):
    """推荐同类电影（基于 SIMILAR_TO 推理关系，回退到类型相似度）"""
    driver = get_driver()
    movies = []

    with driver.session() as session:
        result = session.run("""
            MATCH (m:Movie {douban_id: $id})-[:SIMILAR_TO]-(other:Movie)
            RETURN other
            ORDER BY other.rating DESC
            LIMIT 10
        """, id=douban_id)
        for record in result:
            m = record['other']
            movies.append({
                'douban_id': m['douban_id'],
                'title': m['title'],
                'year': m['year'],
                'rating': m['rating'],
                'poster_url': m.get('poster_url', ''),
            })

        # 如果推理关系不够，回退到类型相似度
        if len(movies) < 5:
            fallback = session.run("""
                MATCH (m:Movie {douban_id: $id})-[:BELONGS_TO]->(g:Genre)
                WITH m, collect(g) AS my_genres
                MATCH (other:Movie)-[:BELONGS_TO]->(g2:Genre)
                WHERE other <> m AND g2 IN my_genres
                WITH other, count(g2) AS shared
                WHERE shared >= 2
                RETURN other, shared
                ORDER BY shared DESC, other.rating DESC
                LIMIT 10
            """, id=douban_id)
            for record in fallback:
                m = record['other']
                exists = any(x['douban_id'] == m['douban_id'] for x in movies)
                if not exists:
                    movies.append({
                        'douban_id': m['douban_id'],
                        'title': m['title'],
                        'year': m['year'],
                        'rating': m['rating'],
                        'poster_url': m.get('poster_url', ''),
                    })

    return jsonify({'movies': movies, 'source': 'similar_genre'})


@recommend_bp.route('/recommend/collaboration/<douban_id>')
def collaboration_recommend(douban_id):
    """基于合作网络推荐电影"""
    driver = get_driver()
    movies = []

    with driver.session() as session:
        result = session.run("""
            MATCH (p:Person {douban_id: $id})-[:COLLABORATED_WITH]-(partner:Person)
            WITH partner ORDER BY partner.name
            LIMIT 5
            MATCH (partner)-[:ACTS_IN|DIRECTED]->(m:Movie)
            WHERE m.rating IS NOT NULL
            RETURN DISTINCT m, partner.name AS via
            ORDER BY m.rating DESC
            LIMIT 10
        """, id=douban_id)
        for record in result:
            m = record['m']
            movies.append({
                'douban_id': m['douban_id'],
                'title': m['title'],
                'year': m['year'],
                'rating': m['rating'],
                'poster_url': m.get('poster_url', ''),
                'reason': f"通过 {record['via']} 推荐",
            })

    return jsonify({'movies': movies, 'source': 'collaboration'})


@recommend_bp.route('/recommend/popular')
def popular_movies():
    """热门推荐：高评分电影"""
    driver = get_driver()
    movies = []

    with driver.session() as session:
        result = session.run("""
            MATCH (m:Movie)
            WHERE m.rating IS NOT NULL AND m.rating >= 8.5
            RETURN m
            ORDER BY m.rating DESC
            LIMIT 12
        """)
        for record in result:
            m = record['m']
            movies.append({
                'douban_id': m['douban_id'],
                'title': m['title'],
                'year': m['year'],
                'rating': m['rating'],
                'poster_url': m.get('poster_url', ''),
            })

    return jsonify({'movies': movies})
