const express = require('express');
const router = express.Router();
const TrainingSession = require('../models/TrainingSession');
const jwt = require('jsonwebtoken');

// Middleware для проверки токена
const authMiddleware = (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
        return res.status(401).json({ error: 'Токен отсутствует' });
    }

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET || 'secret_key');
        req.userId = decoded.userId;
        next();
    } catch (error) {
        res.status(401).json({ error: 'Недействительный токен' });
    }
};

// Create new training session
router.post('/session/start', authMiddleware, async (req, res) => {
    try {
        const { exerciseId, scenario } = req.body;

        const session = new TrainingSession({
            userId: req.userId,
            exerciseId,
            scenario: scenario || 'normal'
        });

        await session.save();
        res.status(201).json({ message: 'Тренировка начата', session });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Update session with event
router.post('/session/:id/event', authMiddleware, async (req, res) => {
    try {
        const { action, result, value } = req.body;
        const session = await TrainingSession.findById(req.params.id);

        if (!session) {
            return res.status(404).json({ error: 'Сессия не найдена' });
        }

        session.events.push({
            timestamp: new Date(),
            action,
            result,
            value
        });

        if (result === 'success') {
            session.correctActions++;
        } else if (result === 'error') {
            session.errors++;
        }

        await session.save();
        res.json({ message: 'Событие записано', session });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// End training session
router.post('/session/:id/end', authMiddleware, async (req, res) => {
    try {
        const { parameters, status } = req.body;
        const session = await TrainingSession.findById(req.params.id);

        if (!session) {
            return res.status(404).json({ error: 'Сессия не найдена' });
        }

        session.endTime = new Date();
        session.duration = (session.endTime - session.startTime) / 1000; // в секундах
        session.status = status || 'completed';
        session.parameters = parameters;

        // Calculate score
        const total = session.correctActions + session.errors;
        session.score = total > 0 ? Math.round((session.correctActions / total) * 100) : 0;

        await session.save();
        res.json({ message: 'Тренировка завершена', session });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get user sessions
router.get('/user/sessions', authMiddleware, async (req, res) => {
    try {
        const sessions = await TrainingSession.find({ userId: req.userId })
            .populate('exerciseId')
            .sort({ startTime: -1 });
        res.json(sessions);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get session by ID
router.get('/session/:id', authMiddleware, async (req, res) => {
    try {
        const session = await TrainingSession.findById(req.params.id)
            .populate('exerciseId');
        if (!session) {
            return res.status(404).json({ error: 'Сессия не найдена' });
        }
        res.json(session);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
