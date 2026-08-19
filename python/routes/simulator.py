from flask import Blueprint, request, jsonify
from models.simulator import ELOuSimulator
import uuid

simulator_bp = Blueprint('simulator', __name__, url_prefix='/api/python/simulator')

# Хранилище активных сессий
active_sessions = {}

@simulator_bp.route('/start', methods=['POST'])
def start_simulation():
    """Запустить новую симуляцию"""
    try:
        data = request.json
        scenario = data.get('scenario', 'normal')
        initial_voltage = data.get('initial_voltage', 230)
        
        # Создать новую симуляцию
        sim = ELOuSimulator(scenario=scenario, initial_voltage=initial_voltage)
        session_id = str(uuid.uuid4())
        active_sessions[session_id] = sim
        
        # Запустить питание
        sim.power_switch(True)
        
        return jsonify({
            'status': 'started',
            'session_id': session_id,
            'scenario': scenario,
            'data': sim.get_data()
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@simulator_bp.route('/update', methods=['PUT'])
def update_simulation():
    """Обновить параметры симуляции"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id not in active_sessions:
            return jsonify({'error': 'Session not found'}), 404
        
        sim = active_sessions[session_id]
        
        # Обновить параметры
        if 'start' in data:
            success, message = sim.start()
            if not success:
                return jsonify({'error': message}), 400
        
        if 'stop' in data:
            sim.stop()
        
        if 'speed' in data:
            sim.set_speed(data['speed'])
        
        if 'pressure' in data:
            sim.set_pressure(data['pressure'])
        
        # Обновить параметры системы
        sim.update_parameters()
        
        return jsonify({
            'status': 'updated',
            'session_id': session_id,
            'data': sim.get_data()
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@simulator_bp.route('/data/<session_id>', methods=['GET'])
def get_simulation_data(session_id):
    """Получить данные симуляции"""
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    sim = active_sessions[session_id]
    
    return jsonify({
        'session_id': session_id,
        'current_data': sim.get_data(),
        'events': sim.get_events()[-10:],  # Последние 10 событий
        'total_events': len(sim.get_events())
    }), 200

@simulator_bp.route('/end/<session_id>', methods=['POST'])
def end_simulation(session_id):
    """Завершить симуляцию"""
    if session_id not in active_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    sim = active_sessions[session_id]
    sim.stop()
    
    result = {
        'session_id': session_id,
        'status': 'ended',
        'final_data': sim.get_data(),
        'all_events': sim.get_events()
    }
    
    # Удалить сессию
    del active_sessions[session_id]
    
    return jsonify(result), 200

@simulator_bp.route('/scenarios', methods=['GET'])
def get_scenarios():
    """Получить доступные сценарии"""
    return jsonify({
        'scenarios': [
            {'name': 'normal', 'description': 'Нормальная работа оборудования'},
            {'name': 'warning', 'description': 'Система в режиме предупреждения'},
            {'name': 'emergency', 'description': 'Аварийная ситуация'}
        ]
    }), 200
