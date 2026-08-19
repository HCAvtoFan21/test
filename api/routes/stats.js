const express = require('express');
const router = express.Router();
const User = require('../models/User');
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

// Get user statistics
router.get('/user', authMiddleware, async (req, res) => {
    try {
        const user = await User.findById(req.userId);
        if (!user) {
            return res.status(404).json({ error: 'Пользователь не найден' });
        }

        const sessions = await TrainingSession.find({ userId: req.userId });
        const completedSessions = sessions.filter(s => s.status === 'completed');
        const avgScore = completedSessions.length > 0
            ? Math.round(completedSessions.reduce((sum, s) => sum + s.score, 0) / completedSessions.length)
            : 0;

        res.json({
            user: {
                id: user._id,
                name: user.name,
                level: user.level,
                totalSessions: sessions.length,
                completedSessions: completedSessions.length,
                averageScore: avgScore,
                totalTrainingTime: completedSessions.reduce((sum, s) => sum + (s.duration || 0), 0)
            }
        });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get leaderboard
router.get('/leaderboard', authMiddleware, async (req, res) => {
    try {
        const sessions = await TrainingSession.aggregate([
            { $match: { status: 'completed' } },
            { $group: {
                _id: '$userId',
                totalScore: { $sum: '$score' },
                sessionCount: { $sum: 1 },
                averageScore: { $avg: '$score' }
            }},
            { $sort: { averageScore: -1 } },
            { $limit: 20 },
            { $lookup: {
                from: 'users',
                localField: '_id',
                foreignField: '_id',
                as: 'user'
            }}
        ]);

        const leaderboard = sessions.map((item, index) => ({
            rank: index + 1,
            userId: item._id,
            name: item.user[0]?.name || 'Unknown',
            level: item.user[0]?.level || 1,
            averageScore: Math.round(item.averageScore),
            totalSessions: item.sessionCount
        }));

        res.json(leaderboard);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get scenario statistics
router.get('/scenarios', authMiddleware, async (req, res) => {
    try {
        const stats = await TrainingSession.aggregate([
            { $match: { userId: require('mongoose').Types.ObjectId(req.userId) } },
            { $group: {
                _id: '$scenario',
                count: { $sum: 1 },
                averageScore: { $avg: '$score' },
                successCount: { $sum: { $cond: [{ $eq: ['$status', 'completed'] }, 1, 0] } }
            }}
        ]);

        res.json(stats);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Get recent activity
router.get('/activity', authMiddleware, async (req, res) => {
    try {
        const sessions = await TrainingSession.find({ userId: req.userId })
            .populate('exerciseId', 'title level')
            .sort({ endTime: -1 })
            .limit(10);

        const activity = sessions.map(session => ({
            id: session._id,
            exercise: session.exerciseId?.title,
            level: session.exerciseId?.level,
            score: session.score,
            status: session.status,
            date: session.endTime || session.startTime,
            duration: session.duration
        }));

        res.json(activity);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;
