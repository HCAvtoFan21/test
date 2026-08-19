# ЭЛОу АВТ Training API

API сервер для тренировочного комплекса ЭЛОу АВТ. Обеспечивает управление пользователями, упражнениями, сессиями тренировок и статистикой.

## Установка

### Требования
- Node.js 14+
- MongoDB 4.0+
- npm или yarn

### Шаги установки

1. Перейдите в директорию API:
```bash
cd api
```

2. Установите зависимости:
```bash
npm install
```

3. Создайте файл `.env`:
```bash
cp .env.example .env
```

4. Отредактируйте `.env` и установите переменные:
```env
MONGODB_URI=mongodb://localhost:27017/elou-avt
PORT=5000
JWT_SECRET=your_secure_secret_key
NODE_ENV=development
```

5. Убедитесь, что MongoDB запущена:
```bash
# Для Linux/Mac
mongod

# Или используйте Docker:
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

6. Запустите сервер:
```bash
npm start
# или для разработки с автозагрузкой
npm run dev
```

## API Endpoints

### Authentication

#### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "name": "Оператор",
  "email": "user@example.com",
  "password": "password123",
  "level": 1
}

Response: 201 Created
{
  "message": "Пользователь зарегистрирован",
  "token": "eyJhbGc...",
  "user": {...}
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response: 200 OK
{
  "message": "Вход успешен",
  "token": "eyJhbGc...",
  "user": {...}
}
```

#### Verify Token
```http
POST /api/auth/verify
Authorization: Bearer {token}

Response: 200 OK
{
  "valid": true,
  "userId": "507f1f77bcf86cd799439011"
}
```

### Users

#### Get Profile
```http
GET /api/users/profile
Authorization: Bearer {token}

Response: 200 OK
{"id": "...", "name": "...", ...}
```

#### Get All Users
```http
GET /api/users
Authorization: Bearer {token}

Response: 200 OK
[{...}, {...}]
```

#### Get User by ID
```http
GET /api/users/{id}
Authorization: Bearer {token}

Response: 200 OK
{"id": "...", ...}
```

#### Update User Level
```http
PUT /api/users/{id}/level
Authorization: Bearer {token}
Content-Type: application/json

{
  "level": 2
}

Response: 200 OK
```

#### Update User Stats
```http
PUT /api/users/{id}/stats
Authorization: Bearer {token}
Content-Type: application/json

{
  "completedExercises": 5,
  "averageScore": 85,
  "totalTrainingTime": 120
}

Response: 200 OK
```

### Exercises

#### Get All Exercises
```http
GET /api/exercises?level=1&difficulty=Easy
Authorization: Bearer {token}

Response: 200 OK
[{...}, {...}]
```

#### Get Exercise by ID
```http
GET /api/exercises/{id}
Authorization: Bearer {token}

Response: 200 OK
{"id": "...", "title": "...", ...}
```

#### Create Exercise
```http
POST /api/exercises
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Базовый запуск системы",
  "description": "...",
  "level": 1,
  "estimatedTime": 5,
  "difficulty": "Easy",
  "objectives": ["..."],
  "steps": [...]
}

Response: 201 Created
```

#### Update Exercise
```http
PUT /api/exercises/{id}
Authorization: Bearer {token}
Content-Type: application/json

{...}

Response: 200 OK
```

#### Delete Exercise
```http
DELETE /api/exercises/{id}
Authorization: Bearer {token}

Response: 200 OK
```

### Training Simulator

#### Start Training Session
```http
POST /api/simulator/session/start
Authorization: Bearer {token}
Content-Type: application/json

{
  "exerciseId": "507f1f77bcf86cd799439011",
  "scenario": "normal"
}

Response: 201 Created
{
  "message": "Тренировка начата",
  "session": {...}
}
```

#### Log Training Event
```http
POST /api/simulator/session/{sessionId}/event
Authorization: Bearer {token}
Content-Type: application/json

{
  "action": "power_on",
  "result": "success",
  "value": {"voltage": 230}
}

Response: 200 OK
```

#### End Training Session
```http
POST /api/simulator/session/{sessionId}/end
Authorization: Bearer {token}
Content-Type: application/json

{
  "parameters": {
    "voltage": 230,
    "current": 5,
    "temperature": 35,
    "pressure": 1.5,
    "speed": 75
  },
  "status": "completed"
}

Response: 200 OK
```

#### Get User Sessions
```http
GET /api/simulator/user/sessions
Authorization: Bearer {token}

Response: 200 OK
[{...}, {...}]
```

#### Get Session Details
```http
GET /api/simulator/session/{sessionId}
Authorization: Bearer {token}

Response: 200 OK
{...}
```

### Statistics

#### Get User Statistics
```http
GET /api/stats/user
Authorization: Bearer {token}

Response: 200 OK
{
  "user": {
    "id": "...",
    "name": "...",
    "level": 1,
    "totalSessions": 10,
    "completedSessions": 8,
    "averageScore": 85,
    "totalTrainingTime": 300
  }
}
```

#### Get Leaderboard
```http
GET /api/stats/leaderboard
Authorization: Bearer {token}

Response: 200 OK
[
  {
    "rank": 1,
    "name": "...",
    "level": 3,
    "averageScore": 95,
    "totalSessions": 50
  },
  {...}
]
```

#### Get Scenario Statistics
```http
GET /api/stats/scenarios
Authorization: Bearer {token}

Response: 200 OK
[...]
```

#### Get Recent Activity
```http
GET /api/stats/activity
Authorization: Bearer {token}

Response: 200 OK
[...]
```

## Структура проекта

```
api/
├── server.js              # Главный файл приложения
├── package.json           # Зависимости
├── .env.example           # Шаблон переменных окружения
├── models/
│   ├── User.js           # Модель пользователя
│   ├── Exercise.js       # Модель упражнения
│   └── TrainingSession.js # Модель сессии тренировки
└── routes/
    ├── auth.js           # Аутентификация
    ├── users.js          # Управление пользователями
    ├── exercises.js      # Управление упражнениями
    ├── simulator.js      # Тренировочные сессии
    └── stats.js          # Статистика и аналитика
```

## Примеры использования

### JavaScript/Fetch

```javascript
// Регистрация
const response = await fetch('http://localhost:5000/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        name: 'Оператор',
        email: 'user@example.com',
        password: 'password123',
        level: 1
    })
});

const data = await response.json();
const token = data.token;

// Запрос с токеном
const profileResponse = await fetch('http://localhost:5000/api/users/profile', {
    headers: { 'Authorization': `Bearer ${token}` }
});

const profile = await profileResponse.json();
console.log(profile);
```

### cURL

```bash
# Регистрация
curl -X POST http://localhost:5000/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Оператор",
    "email": "user@example.com",
    "password": "password123",
    "level": 1
  }'

# Запрос профиля
curl -X GET http://localhost:5000/api/users/profile \
  -H 'Authorization: Bearer YOUR_TOKEN_HERE'
```

## Безопасность

- ✅ JWT токены для аутентификации
- ✅ Хеширование паролей с bcryptjs
- ✅ CORS настроен для безопасности
- ✅ Валидация входных данных
- ✅ Проверка прав доступа на всех эндпоинтах

## Лицензия

MIT

## Автор

HCAvtoFan21
