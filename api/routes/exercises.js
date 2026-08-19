const express = require('express');
const router = express.Router();
const Exercise = require('../models/Exercise');
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

// Get all exercises
router.get('/', authMiddleware, async (req, res) => {
    try {
        const { level, difficulty } = req.query;
        const filter = {};
        if (level) filter.level = level;
        if (difficulty) filter.difficulty = difficulty;

        const exercises = await Exercise.find(filter);
        res.json(exercises);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get exercise by ID
router.get('/:id', authMiddleware, async (req, res) => {
    try {
        const exercise = await Exercise.findById(req.params.id);
        if (!exercise) {
            return res.status(404).json({ error: 'Упражнение не найдено' });
        }
        res.json(exercise);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Create exercise (admin only)
router.post('/', authMiddleware, async (req, res) => {
    try {
        const { title, description, level, estimatedTime, difficulty, objectives, steps } = req.body;

        const exercise = new Exercise({
            title,
            description,
            level,
            estimatedTime,
            difficulty,
            objectives,
            steps
        });

        await exercise.save();
        res.status(201).json({ message: 'Упражнение создано', exercise });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Update exercise
router.put('/:id', authMiddleware, async (req, res) => {
    try {
        const exercise = await Exercise.findByIdAndUpdate(
            req.params.id,
            req.body,
            { new: true }
        );
        res.json({ message: 'Упражнение обновлено', exercise });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Delete exercise
router.delete('/:id', authMiddleware, async (req, res) => {
    try {
        await Exercise.findByIdAndDelete(req.params.id);
        res.json({ message: 'Упражнение удалено' });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
