from flask import Blueprint, request, jsonify, current_app

graph_bp = Blueprint('graph', __name__)


def get_driver():
    return current_app.config['get_db']()


@graph_bp.route('/graph/entity/<entity_type>/<douban_id>')
def get_entity_graph(entity_type, douban_id):
    """获取以某实体为中心的 1-2 跳邻居子图"""
    driver = get_driver()
    label = 'Movie' if entity_type == 'movie' else 'Person'

    query = f"""
        MATCH (center:{label} {{douban_id: $id}})
        OPTIONAL MATCH (center)-[r]-(neighbor)
        WHERE type(r) IN ['ACTS_IN', 'DIRECTED', 'WROTE', 'BELONGS_TO',
                           'PRODUCED_IN', 'IN_LANGUAGE', 'RELEASED_IN',
                           'COLLABORATED_WITH', 'SIMILAR_TO']
        RETURN center, r, neighbor, labels(neighbor) AS neighbor_labels
        LIMIT 200
    """

    nodes = {}
    links = []

    with driver.session() as session:
        result = session.run(query, id=douban_id)
        records = list(result)

    if not records:
        return jsonify({'error': 'Entity not found'}), 404

    for record in records:
        center = record['center']
        neighbor = record['neighbor']
        rel = record['r']

        center_key = f"{list(center.labels)[0]}_{center['douban_id']}"
        if center_key not in nodes:
            nodes[center_key] = _node_to_dict(center)

        if neighbor:
            neighbor_labels = record['neighbor_labels']
            n_label = neighbor_labels[0] if neighbor_labels else 'Unknown'
            n_id = neighbor.get('douban_id') or neighbor.get('name') or neighbor.get('value')
            neighbor_key = f"{n_label}_{n_id}"
            if neighbor_key not in nodes:
                nodes[neighbor_key] = _node_to_dict(neighbor)

            links.append({
                'source': center_key,
                'target': neighbor_key,
                'type': type(rel).__name__,
                'properties': dict(rel) if rel else {},
            })

    return jsonify({
        'nodes': list(nodes.values()),
        'links': links,
    })


@graph_bp.route('/graph/path')
def find_path():
    """两实体间最短路径"""
    from_id = request.args.get('from_id', '')
    to_id = request.args.get('to_id', '')

    if not from_id or not to_id:
        return jsonify({'error': 'Missing from_id or to_id'}), 400

    driver = get_driver()

    with driver.session() as session:
        result = session.run("""
            MATCH (start {douban_id: $from_id}), (end {douban_id: $to_id})
            MATCH path = shortestPath((start)-[*..6]-(end))
            RETURN path LIMIT 1
        """, from_id=from_id, to_id=to_id)
        record = result.single()

    if not record:
        return jsonify({'error': 'No path found within 6 hops'}), 404

    path = record['path']
    nodes = {}
    links = []

    for node in path.nodes:
        labels = list(node.labels)
        key = f"{labels[0]}_{node.get('douban_id') or node.get('name') or node.get('value')}"
        if key not in nodes:
            nodes[key] = _node_to_dict(node)

    for rel in path.relationships:
        start_node = rel.start_node
        end_node = rel.end_node
        s_labels = list(start_node.labels)
        e_labels = list(end_node.labels)
        s_key = f"{s_labels[0]}_{start_node.get('douban_id') or start_node.get('name') or start_node.get('value')}"
        e_key = f"{e_labels[0]}_{end_node.get('douban_id') or end_node.get('name') or end_node.get('value')}"
        links.append({
            'source': s_key,
            'target': e_key,
            'type': type(rel).__name__,
        })

    return jsonify({'nodes': list(nodes.values()), 'links': links, 'path_found': True})


@graph_bp.route('/graph/stats')
def get_stats():
    """获取图谱统计信息"""
    driver = get_driver()
    stats = {}
    queries = {
        'movie_count': 'MATCH (m:Movie) RETURN count(m) AS c',
        'person_count': 'MATCH (p:Person) RETURN count(p) AS c',
        'genre_count': 'MATCH (g:Genre) RETURN count(g) AS c',
        'relation_count': 'MATCH ()-[r]->() RETURN count(r) AS c',
    }
    with driver.session() as session:
        for key, q in queries.items():
            res = session.run(q)
            record = res.single()
            stats[key] = record['c'] if record else 0
    return jsonify(stats)


def _node_to_dict(node):
    """将 neo4j Node 转为 dict"""
    labels = list(node.labels)
    label = labels[0] if labels else 'Unknown'
    d = dict(node)
    d['label'] = label
    d['id'] = d.get('douban_id') or d.get('name') or str(d.get('value', ''))
    return d
