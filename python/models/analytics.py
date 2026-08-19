import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class TrainingAnalytics:
    """
    Анализатор данных тренировок
    Выполняет статистический анализ и выявляет тренды
    """
    
    def __init__(self):
        self.sessions_data = []
    
    def analyze_session(self, session_data):
        """
        Анализировать сессию тренировки
        
        Args:
            session_data: данные сессии
        
        Returns:
            Анализ сессии с метриками
        """
        if not session_data:
            return None
        
        analysis = {
            'session_id': session_data.get('_id'),
            'timestamp': datetime.now().isoformat(),
            'metrics': self._calculate_metrics(session_data),
            'errors': self._identify_errors(session_data),
            'recommendations': self._generate_recommendations(session_data)
        }
        
        return analysis
    
    def _calculate_metrics(self, session_data):
        """Расчет метрик сессии"""
        correct_actions = session_data.get('correctActions', 0)
        errors = session_data.get('errors', 0)
        total = correct_actions + errors
        
        score = (correct_actions / total * 100) if total > 0 else 0
        duration = session_data.get('duration', 0)
        
        metrics = {
            'score': round(score, 2),
            'accuracy': round((correct_actions / total * 100), 2) if total > 0 else 0,
            'correct_actions': correct_actions,
            'errors': errors,
            'total_actions': total,
            'error_rate': round((errors / total * 100), 2) if total > 0 else 0,
            'duration': duration,
            'actions_per_minute': round((total / duration * 60), 2) if duration > 0 else 0
        }
        
        return metrics
    
    def _identify_errors(self, session_data):
        """Выявить ошибки в сессии"""
        errors_list = []
        events = session_data.get('events', [])
        
        for event in events:
            if event.get('result') == 'error':
                errors_list.append({
                    'action': event.get('action'),
                    'timestamp': event.get('timestamp'),
                    'value': event.get('value')
                })
        
        # Анализ типов ошибок
        error_types = {}
        for error in errors_list:
            action = error['action']
            error_types[action] = error_types.get(action, 0) + 1
        
        return {
            'count': len(errors_list),
            'error_types': error_types,
            'errors': errors_list[:10]  # Первые 10 ошибок
        }
    
    def _generate_recommendations(self, session_data):
        """Сгенерировать рекомендации"""
        metrics = self._calculate_metrics(session_data)
        recommendations = []
        
        if metrics['error_rate'] > 30:
            recommendations.append("Высокий процент ошибок. Повторите упражнение.")
        
        if metrics['score'] < 70:
            recommendations.append("Результат ниже требуемого. Потренируйтесь еще раз.")
        
        if metrics['actions_per_minute'] < 5:
            recommendations.append("Работайте быстрее. Недостаточная скорость действий.")
        
        if metrics['score'] >= 85:
            recommendations.append("Отличный результат! Готовы перейти на следующий уровень.")
        
        return recommendations
    
    def compare_sessions(self, session1, session2):
        """Сравнить две сессии"""
        metrics1 = self._calculate_metrics(session1)
        metrics2 = self._calculate_metrics(session2)
        
        comparison = {
            'session1_score': metrics1['score'],
            'session2_score': metrics2['score'],
            'score_improvement': round(metrics2['score'] - metrics1['score'], 2),
            'accuracy_change': round(metrics2['accuracy'] - metrics1['accuracy'], 2),
            'speed_change': round(metrics2['actions_per_minute'] - metrics1['actions_per_minute'], 2)
        }
        
        return comparison
    
    def analyze_user_progress(self, user_sessions):
        """
        Анализировать прогресс пользователя
        
        Args:
            user_sessions: список сессий пользователя
        
        Returns:
            Анализ прогресса с трендами
        """
        if not user_sessions:
            return None
        
        scores = [self._calculate_metrics(s)['score'] for s in user_sessions]
        accuracies = [self._calculate_metrics(s)['accuracy'] for s in user_sessions]
        
        progress = {
            'total_sessions': len(user_sessions),
            'average_score': round(np.mean(scores), 2),
            'best_score': round(max(scores), 2),
            'worst_score': round(min(scores), 2),
            'score_trend': self._calculate_trend(scores),
            'accuracy_trend': self._calculate_trend(accuracies),
            'improvement': self._calculate_improvement(scores),
            'consistency': round(1 - (np.std(scores) / np.mean(scores)), 2) if np.mean(scores) > 0 else 0
        }
        
        return progress
    
    def _calculate_trend(self, values):
        """Рассчитать тренд (улучшение/ухудшение)"""
        if len(values) < 2:
            return 'neutral'
        
        recent = np.mean(values[-3:]) if len(values) >= 3 else np.mean(values[-2:])
        earlier = np.mean(values[:3]) if len(values) >= 3 else values[0]
        
        change = recent - earlier
        
        if change > 5:
            return 'improving'
        elif change < -5:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_improvement(self, scores):
        """Рассчитать улучшение в процентах"""
        if len(scores) < 2:
            return 0
        
        return round(((scores[-1] - scores[0]) / scores[0] * 100), 2)
    
    def get_statistics_by_level(self, sessions, level):
        """Получить статистику по уровню сложности"""
        level_sessions = [s for s in sessions if s.get('exerciseLevel') == level]
        
        if not level_sessions:
            return None
        
        metrics_list = [self._calculate_metrics(s) for s in level_sessions]
        
        return {
            'level': level,
            'total_sessions': len(level_sessions),
            'average_score': round(np.mean([m['score'] for m in metrics_list]), 2),
            'average_accuracy': round(np.mean([m['accuracy'] for m in metrics_list]), 2),
            'average_errors': round(np.mean([m['errors'] for m in metrics_list]), 2),
            'success_rate': round(sum(1 for m in metrics_list if m['score'] >= 70) / len(metrics_list) * 100, 2)
        }
