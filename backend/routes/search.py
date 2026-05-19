from flask import Blueprint, request, jsonify, current_app
from neo4j import GraphDatabase

search_bp = Blueprint('search', __name__)


def get_driver():
    return current_app.config['get_db']()


@search_bp.route('/search')
def search():
    """关键词搜索：电影名/人名模糊匹配"""
    q = request.args.get('q', '').strip()
    if not q or len(q) < 1:
        return jsonify({'movies': [], 'persons': [], 'total': 0})

    driver = get_driver()
    movies = []
    persons = []

    with driver.session() as session:
        movie_result = session.run("""
            MATCH (m:Movie)
            WHERE m.title CONTAINS $q
            OPTIONAL MATCH (m)-[:BELONGS_TO]->(g:Genre)
            OPTIONAL MATCH (m)-[:RELEASED_IN]->(y:Year)
            RETURN m, collect(DISTINCT g.name) AS genres, y.value AS year
            ORDER BY m.rating DESC
            LIMIT 20
        """, q=q)
        for record in movie_result:
            m = record['m']
            movies.append({
                'douban_id': m['douban_id'],
                'title': m['title'],
                'year': record['year'],
                'rating': m['rating'],
                'genres': record['genres'],
                'poster_url': m.get('poster_url', ''),
                'type': 'movie',
            })

        person_result = session.run("""
            MATCH (p:Person)
            WHERE p.name CONTAINS $q
            OPTIONAL MATCH (p)-[:ACTS_IN]->(m:Movie)
            RETURN p, count(m) AS movie_count
            ORDER BY movie_count DESC
            LIMIT 10
        """, q=q)
        for record in person_result:
            p = record['p']
            persons.append({
                'douban_id': p['douban_id'],
                'name': p['name'],
                'gender': p.get('gender', ''),
                'birth_year': p['birth_year'],
                'movie_count': record['movie_count'],
                'type': 'person',
            })

    return jsonify({
        'movies': movies,
        'persons': persons,
        'total': len(movies) + len(persons),
    })


@search_bp.route('/filter')
def filter_movies():
    """分面筛选：按类型、年份、国家"""
    genre = request.args.get('genre', '').strip()
    year_from = request.args.get('year_from', type=int)
    year_to = request.args.get('year_to', type=int)
    country = request.args.get('country', '').strip()

    driver = get_driver()

    conditions = []
    params = {}

    if genre:
        conditions.append('(m)-[:BELONGS_TO]->(:Genre {name: $genre})')
        params['genre'] = genre

    if year_from:
        conditions.append('m.year >= $year_from')
        params['year_from'] = year_from

    if year_to:
        conditions.append('m.year <= $year_to')
        params['year_to'] = year_to

    if country:
        conditions.append('(m)-[:PRODUCED_IN]->(:Country {name: $country})')
        params['country'] = country

    where_clause = ' AND '.join(conditions) if conditions else 'true'
    query = f"""
        MATCH (m:Movie)
        WHERE {where_clause}
        OPTIONAL MATCH (m)-[:BELONGS_TO]->(g:Genre)
        RETURN m, collect(DISTINCT g.name) AS genres
        ORDER BY m.rating DESC
        LIMIT 30
    """

    movies = []
    with driver.session() as session:
        result = session.run(query, **params)
        for record in result:
            m = record['m']
            movies.append({
                'douban_id': m['douban_id'],
                'title': m['title'],
                'year': m['year'],
                'rating': m['rating'],
                'genres': record['genres'],
                'poster_url': m.get('poster_url', ''),
                'type': 'movie',
            })

    return jsonify({'movies': movies, 'total': len(movies)})


@search_bp.route('/genres')
def list_genres():
    """返回所有类型列表（供筛选面板使用）"""
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (g:Genre)
            OPTIONAL MATCH (m:Movie)-[:BELONGS_TO]->(g)
            RETURN g.name AS name, count(m) AS movie_count
            ORDER BY movie_count DESC
        """)
        genres = [{'name': r['name'], 'count': r['movie_count']} for r in result]
    return jsonify(genres)


@search_bp.route('/countries')
def list_countries():
    """返回所有国家列表"""
    driver = get_driver()
    with driver.session() as session:
        result = session.run("""
            MATCH (c:Country)
            OPTIONAL MATCH (m:Movie)-[:PRODUCED_IN]->(c)
            RETURN c.name AS name, count(m) AS movie_count
            ORDER BY movie_count DESC
        """)
        countries = [{'name': r['name'], 'count': r['movie_count']} for r in result]
    return jsonify(countries)
