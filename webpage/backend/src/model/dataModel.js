const mongoose = require('mongoose');

const dataSchema = new mongoose.Schema({
    timestamp: { type: Date, required: true },
    device: { type: String, required: true },
    temperatura: { type: Number, required: true },
    co2: { type: Number, required: true },
    humedad: { type: Number, required: true },
    uvs: { type: Number, required: false },
    luminica: { type: Number, required: false }
});

module.exports = mongoose.model('Data', dataSchema);
