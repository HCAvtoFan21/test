import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from models.simulator import ELOuSimulator
from models.analytics import TrainingAnalytics
from models.predictor import TrainingPredictor

class TestSimulator:
    """Тесты симулятора"""
    
    def test_simulator_init(self):
        """Тест инициализации симулятора"""
        sim = ELOuSimulator('normal')
        assert sim.scenario == 'normal'
        assert sim.power_on == False
        assert sim.running == False
    
    def test_power_on(self):
        """Тест включения питания"""
        sim = ELOuSimulator()
        result = sim.power_switch(True)
        assert result == True
        assert sim.power_on == True
        assert sim.voltage == 230
    
    def test_power_off(self):
        """Тест выключения питания"""
        sim = ELOuSimulator()
        sim.power_switch(True)
        sim.power_switch(False)
        assert sim.power_on == False
        assert sim.voltage == 0
    
    def test_start_without_power(self):
        """Тест запуска без питания"""
        sim = ELOuSimulator()
        success, message = sim.start()
        assert success == False
    
    def test_start_with_power(self):
        """Тест запуска с питанием"""
        sim = ELOuSimulator()
        sim.power_switch(True)
        success, message = sim.start()
        assert success == True
        assert sim.running == True
    
    def test_set_speed(self):
        """Тест установки скорости"""
        sim = ELOuSimulator()
        sim.power_switch(True)
        sim.start()
        
        success, message = sim.set_speed(50)
        assert success == True
        assert sim.speed == 50
    
    def test_set_pressure(self):
        """Тест установки давления"""
        sim = ELOuSimulator()
        sim.power_switch(True)
        sim.start()
        
        success, message = sim.set_pressure(2.5)
        assert success == True
        assert sim.pressure == 2.5

class TestAnalytics:
    """Тесты аналитики"""
    
    def test_analytics_init(self):
        """Тест инициализации аналитики"""
        analytics = TrainingAnalytics()
        assert analytics.sessions_data == []
    
    def test_calculate_metrics(self):
        """Тест расчета метрик"""
        analytics = TrainingAnalytics()
        session = {
            '_id': '123',
            'correctActions': 8,
            'errors': 2,
            'duration': 300,
            'events': []
        }
        
        metrics = analytics._calculate_metrics(session)
        assert metrics['score'] == 80.0
        assert metrics['error_rate'] == 20.0
        assert metrics['total_actions'] == 10

class TestPredictor:
    """Тесты предсказателя"""
    
    def test_predictor_init(self):
        """Тест инициализации предсказателя"""
        predictor = TrainingPredictor()
        assert predictor.score_model is not None
    
    def test_predict_score(self):
        """Тест предсказания результата"""
        predictor = TrainingPredictor()
        score = predictor.predict_score({}, 1, [80, 85, 90])
        assert 0 <= score <= 100
    
    def test_predict_optimal_level(self):
        """Тест определения оптимального уровня"""
        predictor = TrainingPredictor()
        level = predictor.predict_optimal_level('user1', 5, [85, 88, 90, 92, 95])
        assert 1 <= level <= 3

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
