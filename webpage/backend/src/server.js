require('dotenv').config();
const connectDB = require('./db/mongoConfig');
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const DataRouter = require('./routes/data');
const fs = require('fs');

const app = express();
const PORT = process.env.BACKEND_PORT;
const JSON = process.env.JSON_PORT;
const MONGO = process.env.MONGO_URI;
const IP = process.env.IP_HOST;
const API_KEY = process.env.API_KEY;
const UPLOAD_TIME = process.env.UPLOAD_TIME;
const LOAD_INFO = process.env.LOAD_INFO;
const JSON_IP = process.env.JSON_IP;

const corsConfig = {
    origin: `http://$(IP):${JSON}`,
    methods: ['GET', 'POST'],
    credentials: false,
};

app.use(cors(corsConfig));
app.options('*', cors(corsConfig)); 


app.use(express.json({ limit: '10mb' }));


app.use('/api', DataRouter);
app.get('/predict', (req, res) => {
    const filePath = path.join(__dirname, './predicho.txt');
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            res.status(500).send('Error al leer el archivo');
            return;
        }
        res.send(data);
    });
});

app.use(
    '/data.json',
    createProxyMiddleware({
        target: `http://${IP}:${JSON}`, 
        changeOrigin: true,
        pathRewrite: { '^/data.json': '/data.json' },
        logLevel: 'debug',
    })
);


app.use(express.static(path.join(__dirname, '../../frontend/public')));


app.get('5000', (req, res) => {
    res.sendFile(path.join(__dirname, '../../frontend/public', 'index.html'));
});

app.get('/env.js', (req, res) => {
    res.type('application/javascript');
    res.send(`
	const JSON_IP = "${JSON_IP}";
	const UPLOAD_TIME = "${UPLOAD_TIME}";
	const LOAD_INFO = "${LOAD_INFO}";
	const BACKEND_PORT = "${PORT}";
    `);
});

async function initApp() {
    try {
        await mongoose.connection.close();
        await connectDB(MONGO); 
        app.listen(PORT, () => console.log(`Listening on ${IP}:${PORT}`)); 
    } catch (err) {
        console.error(err);
        process.exit(1); 
    }
}

initApp();
