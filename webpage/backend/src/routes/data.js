const express = require('express');
const router = express.Router();
const DataModel = require('../model/dataModel');


const app = express();
app.use(express.json());

router.post('/DataSave', async (req, res) => {
    try {
        const dataArray = req.body;
        const savedData = await DataModel.insertMany(dataArray);
        res.json(savedData);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

router.get('/DataSave', async (req, res) => {
    try {
        DataModel
        const data = await DataModel.find();
        res.json(data);
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

module.exports = router;
