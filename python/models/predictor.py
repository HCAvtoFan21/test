import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
from datetime import datetime

class TrainingPredictor:
    """
    Предсказатель результатов тренировок на основе машинного обучения
    """
    
    def __init__(self, model_path='ml/models.pkl'):
        self.model_path = model_path
        self.score_model = None
        self.level_model = None
        self.scaler = StandardScaler()
        self._load_models()
    
    def _load_models(self):
        """Загрузить сохраненные модели"""
        try:
            models = joblib.load(self.model_path)
            self.score_model = models['score_model']
            self.level_model = models['level_model']
        except:
            # Если модели не найдены, создать новые
            self.score_model = RandomForestRegressor(n_estimators=100, random_state=42)
            self.level_model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    def predict_score(self, user_data, exercise_level, previous_scores):
        """
        Предсказать результат на основе истории и уровня упражнения
        
        Args:
            user_data: данные пользователя
            exercise_level: уровень упражнения (1-3)
            previous_scores: список предыдущих результатов
        
        Returns:
            Предсказанный результат (0-100)
        """
        # Подготовить признаки
        features = self._prepare_features(user_data, exercise_level, previous_scores)
        
        # Если модель обучена
        if self.score_model.n_estimators > 0:
            prediction = self.score_model.predict([features])[0]
        else:
            # Простой расчет на основе среднего
            avg_score = np.mean(previous_scores) if previous_scores else 70
            prediction = avg_score * (0.9 if exercise_level > len(previous_scores) // 5 else 1.1)
        
        # Ограничить результат 0-100
        return max(0, min(100, round(prediction, 2)))
    
    def predict_optimal_level(self, user_id, completed_exercises, scores):
        """
        Определить оптимальный уровень сложности для пользователя
        
        Args:
            user_id: ID пользователя
            completed_exercises: количество завершенных упражнений
            scores: список результатов
        
        Returns:
            Рекомендуемый уровень (1-3)
        """
        if not scores:
            return 1
        
        avg_score = np.mean(scores)
        
        if avg_score >= 85:
            return min(3, int(completed_exercises / 10) + 1)
        elif avg_score >= 70:
            return 2
        else:
            return 1
    
    def recommend_exercise(self, user_id, completed_exercises, scores):
        """
        Рекомендовать следующее упражнение
        
        Args:
            user_id: ID пользователя
            completed_exercises: список ID выполненных упражнений
            scores: список результатов
        
        Returns:
            Рекомендуемое упражнение с уровнем сложности
        """
        optimal_level = self.predict_optimal_level(user_id, len(completed_exercises), scores)
        
        recommendation = {
            'user_id': user_id,
            'recommended_level': optimal_level,
            'estimated_score': self.predict_score({}, optimal_level, scores),
            'timestamp': datetime.now().isoformat(),
            'exercise_types': self._get_exercise_types(optimal_level, completed_exercises)
        }
        
        return recommendation
    
    def _prepare_features(self, user_data, exercise_level, previous_scores):
        """Подготовить признаки для модели"""
        avg_score = np.mean(previous_scores) if previous_scores else 50
        score_trend = (previous_scores[-1] - previous_scores[0]) if len(previous_scores) > 1 else 0
        
        features = [
            exercise_level,
            avg_score,
            score_trend,
            len(previous_scores),
            np.std(previous_scores) if len(previous_scores) > 1 else 0
        ]
        
        return features
    
    def _get_exercise_types(self, level, completed):
        """Получить типы упражнений для уровня"""
        exercise_types = {
            1: ['power_on', 'system_start', 'speed_control'],
            2: ['pressure_management', 'temperature_control', 'scenario_warning'],
            3: ['emergency_response', 'advanced_diagnostics', 'optimization']
        }
        
        return exercise_types.get(level, [])
    
    def train(self, X_train, y_train):
        """Обучить модель"""
        self.score_model.fit(X_train, y_train)
        self._save_models()
    
    def _save_models(self):
        """Сохранить модели"""
        models = {
            'score_model': self.score_model,
            'level_model': self.level_model
        }
        joblib.dump(models, self.model_path)
