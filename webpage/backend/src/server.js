require('dotenv').config();
const connectDB = require('./db/mongoConfig');
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const DataRouter = require('./routes/data');

const app = express();
const PORT = process.env.BACKEND_PORT;
const JSON = process.env.JSON_PORT;
const MONGO = process.env.MONGO_URI;
const IP = process.env.IP_HOST;

const corsConfig = {
    origin: `http://$(IP):${JSON}`,
    methods: ['GET', 'POST'],
    credentials: false,
};

app.use(cors(corsConfig));
app.options('*', cors(corsConfig)); 


app.use(express.json({ limit: '10mb' }));


app.use('/api', DataRouter);
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


app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../../frontend/public', 'index.html'));
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
