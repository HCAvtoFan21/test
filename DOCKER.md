# ЭЛОу АВТ - Docker Deployment

## 🚀 Быстрый старт с Docker

### Требования
- Docker 20.10+
- Docker Compose 2.0+

### Установка Docker

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

**Mac/Windows:**
Загрузите [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Запуск системы

#### 1️⃣ Клонируйте репозиторий
```bash
git clone https://github.com/HCAvtoFan21/test.git
cd test
```

#### 2️⃣ Запустите все сервисы
```bash
docker-compose up -d
```

Эта команда запустит:
- 🗄️ MongoDB (база данных)
- 🔌 Node.js API сервер
- 🐍 Python backend
- 🌐 Nginx (фронтенд)

#### 3️⃣ Откройте приложение в браузере

**Главная страница:**
```
http://localhost
```

**Приложение для тренировок:**
```
http://localhost/app.html
```

**Интерактивный симулятор:**
```
http://localhost/simulator.html
```

**API документация:**
```
http://localhost/api/health
http://localhost/api/python/health
```

---

## 📋 Полезные команды Docker

### Просмотр статуса контейнеров
```bash
docker-compose ps
```

### Просмотр логов
```bash
# Все логи
docker-compose logs

# Логи конкретного сервиса
docker-compose logs api
docker-compose logs python
docker-compose logs mongodb
```

### Остановка системы
```bash
docker-compose down
```

### Полное удаление (включая данные)
```bash
docker-compose down -v
```

### Пересборка образов
```bash
docker-compose build --no-cache
```

### Перезапуск сервиса
```bash
docker-compose restart api
```

---

## 🔍 Проверка работы

### 1. Проверить MongoDB
```bash
docker-compose exec mongodb mongosh -u root -p password
```

### 2. Проверить API сервер
```bash
curl http://localhost:5000/api/health
```

Ожидаемый ответ:
```json
{"status":"ok","message":"API сервер работает"}
```

### 3. Проверить Python backend
```bash
curl http://localhost:5001/api/python/health
```

Ожидаемый ответ:
```json
{"status":"ok","message":"Python backend is running","version":"1.0.0"}
```

---

## 🌐 Архитектура системы в Docker

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Network                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐                     │
│  │   Frontend   │      │   Nginx      │                     │
│  │  (HTML/CSS)  │  ←─→ │ (Reverse     │ ←──── http://localhost
│  │              │      │  Proxy)      │                     │
│  └──────────────┘      └──────────────┘                     │
│         │                      │                             │
│         ↓                      ↓                             │
│  ┌──────────────┐      ┌──────────────────┐                │
│  │ Node.js API  │      │  Python Backend  │                │
│  │   (port      │  ←─→ │     (port 5001)  │                │
│  │   5000)      │      │                  │                │
│  └──────────────┘      └──────────────────┘                │
│         │                      │                             │
│         └──────────┬───────────┘                            │
│                    ↓                                         │
│            ┌──────────────┐                                 │
│            │   MongoDB    │                                 │
│            │  (port 27017)│                                 │
│            └──────────────┘                                 │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Переменные окружения

Создайте файл `.env` в корневой папке:

```env
# MongoDB
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=password
MONGODB_URI=mongodb://root:password@mongodb:27017/elou-avt

# Node.js API
PORT=5000
JWT_SECRET=your_secure_secret_key_here
NODE_ENV=production

# Python
PYTHON_PORT=5001
FLASK_ENV=production
API_SERVER=http://api:5000
```

---

## 🐛 Решение проблем

### Порты уже заняты
```bash
# Измените порты в docker-compose.yml
# Например, вместо 80:80 используйте 8080:80
```

### Контейнер не запускается
```bash
# Проверьте логи
docker-compose logs api

# Пересоберите образ
docker-compose build --no-cache
```

### MongoDB не подключается
```bash
# Убедитесь, что MongoDB запустилась
docker-compose logs mongodb

# Перезапустите MongoDB
docker-compose restart mongodb
```

---

## 📚 Дополнительные ресурсы

- [Docker документация](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Nginx документация](https://nginx.org/)
- [Node.js в Docker](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/)
- [Python в Docker](https://docs.docker.com/language/python/)

---

## 🎯 Следующие шаги

После развертки в Docker вы можете:

1. **Развернуть на облачном сервере** (AWS, Google Cloud, Azure)
2. **Настроить CI/CD** (GitHub Actions, GitLab CI)
3. **Добавить SSL сертификат** (Let's Encrypt)
4. **Масштабировать систему** (Kubernetes, Docker Swarm)
5. **Добавить мониторинг** (Prometheus, Grafana)

---

**Система готова к боевому использованию!** 🚀
