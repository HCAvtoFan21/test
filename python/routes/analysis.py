from flask import Blueprint, request, jsonify
from models.analytics import TrainingAnalytics

analysis_bp = Blueprint('analysis', __name__, url_prefix='/api/python/analysis')

analytics = TrainingAnalytics()

@analysis_bp.route('/session/<session_id>', methods=['POST'])
def analyze_session(session_id):
    """Анализировать сессию тренировки"""
    try:
        data = request.json
        
        # Предполагаем, что данные приходят от API сервера
        session_data = {
            '_id': session_id,
            'correctActions': data.get('correctActions', 0),
            'errors': data.get('errors', 0),
            'duration': data.get('duration', 0),
            'events': data.get('events', []),
            'exerciseLevel': data.get('exerciseLevel')
        }
        
        analysis = analytics.analyze_session(session_data)
        
        return jsonify({
            'status': 'analyzed',
            'session_id': session_id,
            'analysis': analysis
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@analysis_bp.route('/user/<user_id>', methods=['GET'])
def analyze_user_progress(user_id):
    """Анализировать прогресс пользователя"""
    try:
        # В реальном приложении данные должны загружаться из базы данных
        # Здесь показан пример структуры
        user_sessions = request.json.get('sessions', []) if request.json else []
        
        if not user_sessions:
            return jsonify({'error': 'No sessions found'}), 404
        
        progress = analytics.analyze_user_progress(user_sessions)
        
        return jsonify({
            'user_id': user_id,
            'progress': progress
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@analysis_bp.route('/compare', methods=['POST'])
def compare_sessions():
    """Сравнить две сессии"""
    try:
        data = request.json
        session1 = data.get('session1')
        session2 = data.get('session2')
        
        if not session1 or not session2:
            return jsonify({'error': 'Both sessions required'}), 400
        
        comparison = analytics.compare_sessions(session1, session2)
        
        return jsonify({
            'status': 'compared',
            'comparison': comparison
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@analysis_bp.route('/level-stats/<user_id>', methods=['POST'])
def get_level_statistics(user_id):
    """Получить статистику по уровням сложности"""
    try:
        data = request.json
        sessions = data.get('sessions', [])
        
        statistics = {}
        for level in [1, 2, 3]:
            stats = analytics.get_statistics_by_level(sessions, level)
            if stats:
                statistics[f'level_{level}'] = stats
        
        return jsonify({
            'user_id': user_id,
            'statistics': statistics
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
