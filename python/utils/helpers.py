def calculate_average(values):
    """Рассчитать среднее значение"""
    return sum(values) / len(values) if values else 0

def calculate_std_dev(values):
    """Рассчитать стандартное отклонение"""
    if not values:
        return 0
    avg = calculate_average(values)
    return (sum((x - avg) ** 2 for x in values) / len(values)) ** 0.5

def normalize_score(score, min_val=0, max_val=100):
    """Нормализовать оценку в диапазон"""
    return max(min_val, min(max_val, score))

def format_duration(seconds):
    """Форматировать длительность в читаемый вид"""
    minutes = seconds // 60
    secs = seconds % 60
    return f"{int(minutes)}:{int(secs):02d}"

def get_performance_level(score):
    """Получить уровень производительности"""
    if score >= 85:
        return 'Excellent'
    elif score >= 70:
        return 'Good'
    elif score >= 50:
        return 'Average'
    else:
        return 'Poor'
