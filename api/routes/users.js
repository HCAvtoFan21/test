const express = require('express');
const router = express.Router();
const User = require('../models/User');
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

// Get user profile
router.get('/profile', authMiddleware, async (req, res) => {
    try {
        const user = await User.findById(req.userId).populate('sessions');
        if (!user) {
            return res.status(404).json({ error: 'Пользователь не найден' });
        }
        res.json(user);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get all users
router.get('/', authMiddleware, async (req, res) => {
    try {
        const users = await User.find().select('-password');
        res.json(users);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get user by ID
router.get('/:id', authMiddleware, async (req, res) => {
    try {
        const user = await User.findById(req.params.id).populate('sessions');
        if (!user) {
            return res.status(404).json({ error: 'Пользователь не найден' });
        }
        res.json(user);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Update user level
router.put('/:id/level', authMiddleware, async (req, res) => {
    try {
        const { level } = req.body;
        if (level < 1 || level > 3) {
            return res.status(400).json({ error: 'Уровень должен быть от 1 до 3' });
        }

        const user = await User.findByIdAndUpdate(
            req.params.id,
            { level, updatedAt: Date.now() },
            { new: true }
        );

        res.json({ message: 'Уровень обновлен', user });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Update user stats
router.put('/:id/stats', authMiddleware, async (req, res) => {
    try {
        const { completedExercises, averageScore, totalTrainingTime } = req.body;
        const user = await User.findByIdAndUpdate(
            req.params.id,
            {
                completedExercises,
                averageScore,
                totalTrainingTime,
                updatedAt: Date.now()
            },
            { new: true }
        );

        res.json({ message: 'Статистика обнов��ена', user });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
