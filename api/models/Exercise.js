const mongoose = require('mongoose');

const exerciseSchema = new mongoose.Schema({
    title: {
        type: String,
        required: true
    },
    description: {
        type: String,
        required: true
    },
    level: {
        type: Number,
        enum: [1, 2, 3],
        required: true
    },
    estimatedTime: {
        type: Number,
        required: true
    },
    difficulty: {
        type: String,
        enum: ['Easy', 'Medium', 'Hard'],
        required: true
    },
    objectives: [String],
    steps: [{
        stepNumber: Number,
        description: String,
        action: String,
        expectedResult: String
    }],
    courseId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'Course'
    },
    createdAt: {
        type: Date,
        default: Date.now
    }
});

module.exports = mongoose.model('Exercise', exerciseSchema);
