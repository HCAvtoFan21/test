// Application State
const appState = {
    user: {
        name: 'Оператор',
        level: 1,
        totalExercises: 0,
        avgScore: 0,
        trainingDays: 0
    },
    simulator: {
        powerOn: false,
        running: false,
        voltage: 0,
        current: 0,
        temperature: 25,
        pressure: 1,
        speed: 0,
        correct: 0,
        errors: 0,
        scenario: 'normal'
    },
    training: {
        completedExercises: 0,
        totalExercises: 0,
        time: 0,
        sessions: []
    }
};

// Initialize App
window.addEventListener('DOMContentLoaded', () => {
    loadStoredData();
    setupNavigationListeners();
    setupSimulatorControls();
    updateDashboard();
    startSystemUpdates();
});

// Storage Management
function saveToStorage() {
    localStorage.setItem('appState', JSON.stringify(appState));
}

function loadStoredData() {
    const stored = localStorage.getItem('appState');
    if (stored) {
        Object.assign(appState, JSON.parse(stored));
    }
}

// Navigation
function setupNavigationListeners() {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.dataset.page;
            switchPage(page);
        });
    });
}

function switchPage(pageName) {
    // Hide all sections
    document.querySelectorAll('.page-section').forEach(section => {
        section.classList.remove('active');
    });

    // Remove active from nav
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });

    // Show selected section
    const pageElement = document.getElementById(pageName);
    if (pageElement) {
        pageElement.classList.add('active');
    }

    // Mark nav as active
    document.querySelector(`[data-page="${pageName}"]`).classList.add('active');

    // Update header
    updatePageHeader(pageName);
}

function updatePageHeader(page) {
    const titles = {
        'dashboard': { title: 'Панель управления', subtitle: 'Добро пожаловать в систему тренировок' },
        'simulator': { title: 'Интерактивный симулятор', subtitle: 'Управляйте оборудованием ЭЛОу АВТ' },
        'courses': { title: 'Курсы обучения', subtitle: 'Выберите курс для начала обучения' },
        'exercises': { title: 'Упражнения', subtitle: 'Практикуйте различные задачи' },
        'stats': { title: 'Статистика', subtitle: 'Анализ вашего прогресса' },
        'profile': { title: 'Профиль', subtitle: 'Управление настройками профиля' }
    };

    const pageInfo = titles[page] || titles['dashboard'];
    document.getElementById('pageTitle').textContent = pageInfo.title;
    document.getElementById('pageSubtitle').textContent = pageInfo.subtitle;
}

// Simulator Controls
function setupSimulatorControls() {
    // Power Button
    const powerBtn = document.getElementById('powerBtn');
    powerBtn.addEventListener('click', () => {
        appState.simulator.powerOn = !appState.simulator.powerOn;
        updateSimulatorUI();
        if (appState.simulator.powerOn) {
            logEvent('success', 'Питание включено');
        } else {
            logEvent('info', 'Питание отключено');
            appState.simulator.running = false;
        }
    });

    // Start Button
    const startBtn = document.getElementById('startBtn');
    startBtn.addEventListener('click', () => {
        if (appState.simulator.powerOn) {
            appState.simulator.running = true;
            logEvent('success', 'Система запущена');
            updateSimulatorUI();
        }
    });

    // Stop Button
    const stopBtn = document.getElementById('stopBtn');
    stopBtn.addEventListener('click', () => {
        appState.simulator.running = false;
        logEvent('info', 'Система остановлена');
        updateSimulatorUI();
    });

    // Speed Slider
    const speedSlider = document.getElementById('speedCtrl');
    speedSlider.addEventListener('input', (e) => {
        appState.simulator.speed = e.target.value;
        document.getElementById('speedVal').textContent = e.target.value;
        if (appState.simulator.running) {
            appState.simulator.current = (e.target.value / 100) * 5;
        }
        logEvent('info', `Скорость установлена: ${e.target.value}%`);
    });

    // Pressure Slider
    const pressSlider = document.getElementById('pressCtrl');
    pressSlider.addEventListener('input', (e) => {
        appState.simulator.pressure = e.target.value;
        document.getElementById('pressVal').textContent = e.target.value;
        logEvent('info', `Давление установлено: ${e.target.value} Bar`);
    });

    // Scenario Buttons
    document.getElementById('normalScene').addEventListener('click', () => {
        setScenario('normal');
    });

    document.getElementById('warningScene').addEventListener('click', () => {
        if (appState.simulator.powerOn) {
            setScenario('warning');
        }
    });

    document.getElementById('emergencyScene').addEventListener('click', () => {
        if (appState.simulator.powerOn) {
            setScenario('emergency');
            appState.simulator.errors++;
        }
    });
}

function setScenario(scenario) {
    appState.simulator.scenario = scenario;
    document.querySelectorAll('.scenario-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(scenario + 'Scene').classList.add('active');
    logEvent('warning', `Сценарий: ${scenario}`);
}

function updateSimulatorUI() {
    const powerBtn = document.getElementById('powerBtn');
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const speedSlider = document.getElementById('speedCtrl');
    const pressSlider = document.getElementById('pressCtrl');
    const statusInd = document.getElementById('statusInd');
    const statusText = document.getElementById('statusText');

    if (appState.simulator.powerOn) {
        powerBtn.classList.add('active');
        startBtn.disabled = false;
        speedSlider.disabled = false;
        pressSlider.disabled = false;
    } else {
        powerBtn.classList.remove('active');
        startBtn.disabled = true;
        stopBtn.disabled = true;
        speedSlider.disabled = true;
        pressSlider.disabled = true;
        speedSlider.value = 0;
        appState.simulator.speed = 0;
    }

    if (appState.simulator.running) {
        stopBtn.disabled = false;
        statusInd.classList.add('active');
        statusText.textContent = 'Система работает';
        document.getElementById('simStatus').textContent = 'Работает';
    } else {
        stopBtn.disabled = true;
        statusInd.classList.remove('active');
        statusText.textContent = 'Система остановлена';
        document.getElementById('simStatus').textContent = 'Остановлена';
    }

    updateSimulatorValues();
    saveToStorage();
}

function updateSimulatorValues() {
    if (appState.simulator.powerOn) {
        document.getElementById('simVoltage').textContent = '230V';
    } else {
        document.getElementById('simVoltage').textContent = '0V';
    }

    document.getElementById('simCurrent').textContent = appState.simulator.current.toFixed(1) + 'A';
    document.getElementById('simTemp').textContent = appState.simulator.temperature + '°C';
    document.getElementById('correct').textContent = appState.simulator.correct;
    document.getElementById('errors').textContent = appState.simulator.errors;

    const score = appState.simulator.correct + appState.simulator.errors > 0
        ? Math.round((appState.simulator.correct / (appState.simulator.correct + appState.simulator.errors)) * 100)
        : 0;
    document.getElementById('score').textContent = score;
}

function logEvent(type, message) {
    const log = document.getElementById('simLog');
    const entry = document.createElement('div');
    entry.className = 'log-entry ' + type;
    entry.textContent = `[${getTime()}] ${message}`;
    log.appendChild(entry);
    log.scrollTop = log.scrollHeight;
}

function getTime() {
    const now = new Date();
    return `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
}

// System Updates
function startSystemUpdates() {
    setInterval(() => {
        if (appState.simulator.running) {
            // Simulate temperature change
            appState.simulator.temperature += Math.random() - 0.5;
            appState.simulator.temperature = Math.min(Math.max(appState.simulator.temperature, 20), 80);

            // Simulate random correct actions
            if (Math.random() > 0.7) {
                appState.simulator.correct++;
            }

            updateSimulatorValues();
        }

        // Update time display
        document.getElementById('simTime').textContent = getTime();
        saveToStorage();
    }, 1000);
}

// Dashboard Update
function updateDashboard() {
    const total = appState.training.totalExercises || 1;
    const completed = appState.training.completedExercises;
    const percentage = Math.round((completed / total) * 100);

    // Update progress circle
    const dashoffset = 282.6 * (1 - percentage / 100);
    document.getElementById('progressCircle').style.strokeDashoffset = dashoffset;
    document.getElementById('progressPercent').textContent = percentage + '%';

    // Update stats
    document.getElementById('totalTime').textContent = appState.training.time;
    document.getElementById('avgScore').textContent = Math.round(appState.user.avgScore);
    document.getElementById('userLevel').textContent = appState.user.level;
    document.getElementById('profileName').textContent = appState.user.name;
    document.getElementById('profileLevel').textContent = `Уровень ${appState.user.level}`;

    saveToStorage();
}

// Logout
document.querySelector('.btn-logout').addEventListener('click', () => {
    if (confirm('Вы уверены, что хотите выйти?')) {
        alert('Спасибо за тренировку!');
        window.location.reload();
    }
});

// Load sample exercises
function loadSampleData() {
    appState.training.totalExercises = 5;
    appState.training.completedExercises = 0;
    appState.training.time = 2;
    appState.user.avgScore = 85;
    updateDashboard();
}

// Initialize with sample data
loadSampleData();

console.log('🚀 Приложение ЭЛОу АВТ инициализировано');
