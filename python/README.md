# ЭЛОу АВТ - Python Backend

Python backend для системы тренировок ЭЛОу АВТ с поддержкой машинного обучения, анализа данных и моделирования.

## Требования

- Python 3.8+
- pip
- virtualenv (рекомендуется)

## Установка

### 1. Создать виртуальное окружение

```bash
cd python
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Установить зависимости

```bash
pip install -r requirements.txt
```

### 3. Запустить сервер

```bash
python app.py
```

## Структура проекта

```
python/
├── app.py                    # Главное приложение Flask
├── requirements.txt          # Зависимости Python
├── config.py                 # Конфигурация
├── models/
│   ├── simulator.py         # Модель симулятора
│   ├── predictor.py         # Модель предсказания
│   └── analytics.py         # Анализ данных
├── routes/
│   ├── simulator.py         # Эндпоинты симулятора
│   ├── analysis.py          # Эндпоинты анализа
│   └── predictions.py       # Эндпоинты предсказания
├── utils/
│   ├── helpers.py           # Вспомогательные функции
│   └── validators.py        # Валидаторы
├── ml/
│   ├── trainer.py           # Обучение моделей
│   └── models.pkl           # Сохраненные модели
└── tests/
    └── test_simulator.py    # Тесты
```

## API Endpoints

### Симуляция

#### Запустить симуляцию
```bash
POST /api/python/simulator/start
{
  "scenario": "normal",
  "duration": 300,
  "parameters": {
    "voltage": 230,
    "speed": 50
  }
}
```

#### Обновить параметры симуляции
```bash
PUT /api/python/simulator/update
{
  "session_id": "123",
  "voltage": 240,
  "current": 5.2,
  "temperature": 35
}
```

#### Получить данные симуляции
```bash
GET /api/python/simulator/data/{session_id}
```

### Анализ

#### Анализ производительности
```bash
POST /api/python/analysis/performance
{
  "user_id": "123",
  "session_id": "456"
}
```

#### Анализ ошибок
```bash
POST /api/python/analysis/errors
{
  "session_id": "123"
}
```

#### Статистика по упражнениям
```bash
GET /api/python/analysis/exercises/{user_id}
```

### Предсказание

#### Предсказать результат
```bash
POST /api/python/prediction/score
{
  "user_id": "123",
  "exercise_level": 1,
  "previous_scores": [85, 88, 90]
}
```

#### Рекомендовать упражнение
```bash
POST /api/python/prediction/recommend
{
  "user_id": "123",
  "completed_exercises": [1, 2, 3]
}
```

#### Определить оптимальный уровень
```bash
POST /api/python/prediction/level
{
  "user_id": "123"
}
```

## Основные модули

### Simulator Module
Модельизирует работу оборудования ЭЛОу АВТ с реалистичными параметрами:
- Симуляция напряжения и тока
- Расчет температуры
- Моделирование сценариев (нормальный, предупреждение, аварийный)
- Логирование событий

### Predictor Module
Машинное обучение для предсказания:
- Предсказание результатов тренировок
- Рекомендация упражнений
- Определение оптимального уровня сложности
- Анализ прогресса

### Analytics Module
Анализ данных тренировок:
- Анализ производительности
- Выявление ошибок
- Статистика по упражнениям
- Тренды и прогноз

## Использование

### Пример: Запуск симуляции

```python
from models.simulator import ELOuSimulator

# Создать симулятор
sim = ELOuSimulator(scenario='normal')

# Запустить
data = sim.run(duration=300)

# Получить результаты
print(f"Voltage: {data['voltage']}V")
print(f"Current: {data['current']}A")
print(f"Temperature: {data['temperature']}°C")
```

### Пример: Анализ данных

```python
from models.analytics import TrainingAnalytics

# Создать аналитик
analytics = TrainingAnalytics()

# Анализировать сессию
results = analytics.analyze_session(session_id)

print(f"Performance score: {results['score']}")
print(f"Common errors: {results['errors']}")
```

### Пример: Предсказание

```python
from models.predictor import TrainingPredictor

# Создать предсказатель
predictor = TrainingPredictor()

# Предсказать результат
score = predictor.predict_score(
    user_id='123',
    exercise_level=2,
    previous_scores=[85, 88, 90]
)

print(f"Predicted score: {score}")
```

## Тестирование

```bash
# Запустить все тесты
python -m pytest

# Запустить конкретный тест
python -m pytest tests/test_simulator.py

# С покрытием кода
python -m pytest --cov=.
```

## Лицензия

MIT

## Автор

HCAvtoFan21
