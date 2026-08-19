def validate_exercise_level(level):
    """Проверить корректность уровня упражнения"""
    if not isinstance(level, int):
        return False, "Level must be an integer"
    if level < 1 or level > 3:
        return False, "Level must be between 1 and 3"
    return True, "Valid"

def validate_scenario(scenario):
    """Проверить корректность сценария"""
    valid_scenarios = ['normal', 'warning', 'emergency']
    if scenario not in valid_scenarios:
        return False, f"Scenario must be one of: {', '.join(valid_scenarios)}"
    return True, "Valid"

def validate_user_data(data):
    """Проверить данные пользователя"""
    required_fields = ['user_id', 'name', 'level']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    return True, "Valid"

def validate_session_data(data):
    """Проверить данные сессии"""
    required_fields = ['session_id', 'exercise_id', 'correctActions', 'errors']
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
    return True, "Valid"
