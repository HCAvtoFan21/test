import numpy as np
from datetime import datetime
import json

class ELOuSimulator:
    """
    Симулятор оборудования ЭЛОу АВТ
    Моделирует реальную работу оборудования с различными сценариями
    """
    
    def __init__(self, scenario='normal', initial_voltage=230):
        self.scenario = scenario
        self.initial_voltage = initial_voltage
        self.voltage = initial_voltage
        self.current = 0.0
        self.temperature = 25.0
        self.pressure = 1.0
        self.speed = 0
        self.events = []
        self.start_time = datetime.now()
        self.running = False
        self.power_on = False
        
    def power_switch(self, state):
        """Включить/выключить питание"""
        self.power_on = state
        if state:
            self.voltage = self.initial_voltage
            self.events.append({
                'timestamp': datetime.now().isoformat(),
                'event': 'power_on',
                'status': 'success'
            })
        else:
            self.voltage = 0
            self.current = 0
            self.speed = 0
            self.events.append({
                'timestamp': datetime.now().isoformat(),
                'event': 'power_off',
                'status': 'success'
            })
        return self.power_on
    
    def start(self):
        """Запустить систему"""
        if not self.power_on:
            return False, "Питание не включено"
        
        self.running = True
        self.events.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'system_start',
            'status': 'success'
        })
        return True, "Система запущена"
    
    def stop(self):
        """Остановить систему"""
        self.running = False
        self.speed = 0
        self.events.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'system_stop',
            'status': 'success'
        })
        return True, "Система остановлена"
    
    def set_speed(self, speed):
        """Установить скорость вращения"""
        if not self.running:
            return False, "Система не запущена"
        
        speed = max(0, min(100, speed))  # Ограничение 0-100%
        self.speed = speed
        self.current = (speed / 100) * 10  # Максимум 10A
        
        self.events.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'speed_set',
            'value': speed,
            'status': 'success'
        })
        return True, f"Скорость установлена: {speed}%"
    
    def set_pressure(self, pressure):
        """Установить давление"""
        if not self.running:
            return False, "Система не запущена"
        
        pressure = max(0, min(10, pressure))  # Ограничение 0-10 Bar
        self.pressure = pressure
        
        self.events.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'pressure_set',
            'value': pressure,
            'status': 'success'
        })
        return True, f"Давление установлено: {pressure} Bar"
    
    def update_parameters(self):
        """Обновить параметры системы на основе текущего сценария"""
        if not self.running:
            return
        
        # Симуляция изменения температуры
        if self.speed > 0:
            self.temperature += (self.speed / 100) * 0.5 + np.random.normal(0, 0.1)
            self.temperature = max(20, min(80, self.temperature))
        else:
            self.temperature -= 0.1 + np.random.normal(0, 0.05)
            self.temperature = max(20, self.temperature)
        
        # Обработка сценариев
        if self.scenario == 'warning':
            self.temperature += 2  # Перегрев при предупреждении
            self._log_warning()
        
        elif self.scenario == 'emergency':
            self.temperature += 5  # Критический перегрев
            self.voltage -= np.random.normal(0, 1)  # Скачки напряжения
            self._log_error()
    
    def _log_warning(self):
        """Логировать предупреждение"""
        self.events.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'temperature_warning',
            'value': self.temperature,
            'status': 'warning'
        })
    
    def _log_error(self):
        """Логировать ошибку"""
        self.events.append({
            'timestamp': datetime.now().isoformat(),
            'event': 'system_error',
            'value': self.temperature,
            'status': 'error'
        })
    
    def get_data(self):
        """Получить текущие данные системы"""
        return {
            'scenario': self.scenario,
            'power_on': self.power_on,
            'running': self.running,
            'voltage': round(self.voltage, 2),
            'current': round(self.current, 2),
            'temperature': round(self.temperature, 2),
            'pressure': round(self.pressure, 2),
            'speed': self.speed,
            'timestamp': datetime.now().isoformat(),
            'events_count': len(self.events)
        }
    
    def get_events(self):
        """Получить список событий"""
        return self.events
    
    def run(self, duration=300, update_interval=0.1):
        """Запустить симуляцию на определенное время"""
        data_points = []
        steps = int(duration / update_interval)
        
        self.start()
        
        for _ in range(steps):
            self.update_parameters()
            data_points.append(self.get_data())
        
        self.stop()
        
        return {
            'data_points': data_points,
            'events': self.get_events(),
            'final_state': self.get_data()
        }
