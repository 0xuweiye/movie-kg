import os
from flask import Flask, render_template
from flask_cors import CORS
from neo4j import GraphDatabase

NEO4J_URI = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.environ.get('NEO4J_USER', 'neo4j')
NEO4J_PASS = os.environ.get('NEO4J_PASS', '12345678')


def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='../static')
    CORS(app)

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

    def get_db():
        return driver

    app.config['get_db'] = get_db

    from backend.routes.search import search_bp
    from backend.routes.graph import graph_bp
    from backend.routes.recommend import recommend_bp

    app.register_blueprint(search_bp, url_prefix='/api')
    app.register_blueprint(graph_bp, url_prefix='/api')
    app.register_blueprint(recommend_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
