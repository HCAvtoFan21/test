from flask import Flask
from flask_cors import CORS
from config import config
import os

from routes.simulator import simulator_bp
from routes.analysis import analysis_bp
from routes.predictions import prediction_bp

def create_app(config_name=None):
    """Фабрика приложения Flask"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Включить CORS
    CORS(app)
    
    # Регистрировать blueprints
    app.register_blueprint(simulator_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(prediction_bp)
    
    # Health check endpoint
    @app.route('/api/python/health', methods=['GET'])
    def health_check():
        return {
            'status': 'ok',
            'message': 'Python backend is running',
            'version': '1.0.0'
        }, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Endpoint not found'}, 404
    
    @app.errorhandler(500)
    def server_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PYTHON_PORT', 5001))
    print(f'🚀 Python backend запущен на порту {port}')
    print(f'📡 API доступен по адресу: http://localhost:{port}/api/python')
    app.run(host='0.0.0.0', port=port, debug=True)
