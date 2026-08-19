const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true,
        unique: true,
        lowercase: true
    },
    password: {
        type: String,
        required: true
    },
    level: {
        type: Number,
        default: 1,
        min: 1,
        max: 3
    },
    totalExercises: {
        type: Number,
        default: 0
    },
    completedExercises: {
        type: Number,
        default: 0
    },
    averageScore: {
        type: Number,
        default: 0
    },
    totalTrainingTime: {
        type: Number,
        default: 0
    },
    sessions: [{
        type: mongoose.Schema.Types.ObjectId,
        ref: 'TrainingSession'
    }],
    createdAt: {
        type: Date,
        default: Date.now
    },
    updatedAt: {
        type: Date,
        default: Date.now
    }
});

module.exports = mongoose.model('User', userSchema);
