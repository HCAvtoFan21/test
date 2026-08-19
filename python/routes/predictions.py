from flask import Blueprint, request, jsonify
from models.predictor import TrainingPredictor

prediction_bp = Blueprint('prediction', __name__, url_prefix='/api/python/prediction')

predictor = TrainingPredictor()

@prediction_bp.route('/score', methods=['POST'])
def predict_score():
    """Предсказать результат тренировки"""
    try:
        data = request.json
        user_id = data.get('user_id')
        exercise_level = data.get('exercise_level', 1)
        previous_scores = data.get('previous_scores', [])
        
        predicted_score = predictor.predict_score({}, exercise_level, previous_scores)
        
        return jsonify({
            'status': 'predicted',
            'user_id': user_id,
            'exercise_level': exercise_level,
            'predicted_score': predicted_score,
            'confidence': min(100, 70 + len(previous_scores) * 5)  # Увеличивается с опытом
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@prediction_bp.route('/level', methods=['POST'])
def predict_optimal_level():
    """Определить оптимальный уровень сложности"""
    try:
        data = request.json
        user_id = data.get('user_id')
        completed_exercises = data.get('completed_exercises', 0)
        scores = data.get('scores', [])
        
        optimal_level = predictor.predict_optimal_level(user_id, completed_exercises, scores)
        
        return jsonify({
            'status': 'predicted',
            'user_id': user_id,
            'optimal_level': optimal_level,
            'reason': f'Based on {len(scores)} completed exercises with average score {sum(scores)/len(scores):.0f}%' if scores else 'Start with level 1'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@prediction_bp.route('/recommend', methods=['POST'])
def recommend_exercise():
    """Рекомендовать следующее упражнение"""
    try:
        data = request.json
        user_id = data.get('user_id')
        completed_exercises = data.get('completed_exercises', [])
        scores = data.get('scores', [])
        
        recommendation = predictor.recommend_exercise(user_id, completed_exercises, scores)
        
        return jsonify({
            'status': 'recommended',
            'recommendation': recommendation
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@prediction_bp.route('/readiness', methods=['POST'])
def assess_readiness():
    """Оценить готовность к следующему уровню"""
    try:
        data = request.json
        user_id = data.get('user_id')
        current_level = data.get('current_level', 1)
        scores = data.get('scores', [])
        
        if not scores or len(scores) < 5:
            return jsonify({
                'user_id': user_id,
                'ready_for_next_level': False,
                'reason': 'Need at least 5 completed exercises',
                'exercises_needed': max(0, 5 - len(scores))
            }), 200
        
        avg_score = sum(scores) / len(scores)
        ready = avg_score >= 80
        
        return jsonify({
            'user_id': user_id,
            'current_level': current_level,
            'ready_for_next_level': ready,
            'average_score': round(avg_score, 2),
            'min_required_score': 80,
            'reason': 'Ready to advance!' if ready else f'Need average score of 80%, current is {avg_score:.0f}%'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
