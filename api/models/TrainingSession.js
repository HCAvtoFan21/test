const mongoose = require('mongoose');

const trainingSessionSchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    exerciseId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Exercise',
        required: true
    },
    scenario: {
        type: String,
        enum: ['normal', 'warning', 'emergency'],
        default: 'normal'
    },
    startTime: {
        type: Date,
        default: Date.now
    },
    endTime: Date,
    duration: Number,
    correctActions: {
        type: Number,
        default: 0
    },
    errors: {
        type: Number,
        default: 0
    },
    score: {
        type: Number,
        min: 0,
        max: 100
    },
    status: {
        type: String,
        enum: ['in_progress', 'completed', 'failed'],
        default: 'in_progress'
    },
    events: [{
        timestamp: Date,
        action: String,
        result: String,
        value: mongoose.Schema.Types.Mixed
    }],
    parameters: {
        voltage: Number,
        current: Number,
        temperature: Number,
        pressure: Number,
        speed: Number
    },
    feedback: String
});

module.exports = mongoose.model('TrainingSession', trainingSessionSchema);
