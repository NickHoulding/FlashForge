const express = require('express');
const { Pool } = require('pg');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const cors = require('cors');
require('dotenv').config();

const app = express();

app.use(cors({
    origin: ['http://localhost:5173', 'http://localhost:3000'],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json());

const pool = new Pool({
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    user: process.env.DB_USER,
    password: process.env.DB_PASS,
    database: process.env.DB_NAME,
});

app.post('/api/register', async (req, res) => {
    const { username, password } = req.body;
    
    if (!username || !password) {
        return res.status(400).json({ msg: 'Username and password are required' });
    }

    try {
        const hashed = await bcrypt.hash(password, 10);
        await pool.query('INSERT INTO users (username, password_hash) values ($1, $2)', [username, hashed]);
        res.status(201).json({ msg: 'User created' });
    } catch (err) {
        if (err.code === '23505') {
            res.status(409).json({ msg: 'Username already exists' });
        } else {
            res.status(500).json({ msg: 'Server error during registration' });
        }
    }
});

app.post('/api/login', async (req, res) => {
    const { username, password } = req.body;
    
    if (!username || !password) {
        return res.status(400).json({ msg: 'Username and password are required' });
    }

    try {
        const result = await pool.query('SELECT * FROM users WHERE username = $1', [username]);
        
        if (result.rows.length && await bcrypt.compare(password, result.rows[0].password_hash)) {
            const token = jwt.sign({ userId: result.rows[0].id }, process.env.JWT_SECRET);
            res.json({ token });
        } else {
            res.status(401).json({ msg: 'Invalid credentials' });
        }
    } catch (err) {
        res.status(500).json({ msg: 'Server error during login' });
    }
});

const auth = (req, res, next) => {
    const token = req.headers.authorization?.split(' ')[1];

    if (!token) {
        return res.status(401).json({ msg: 'No token' })
    };

    try {
        req.user = jwt.verify(token, process.env.JWT_SECRET);
        next();
    } catch (err) {
        res.status(401).json({ msg: 'Invalid token' });
    }
};

app.get('/api/profile', auth, (req, res) => {
    res.json({ userId: req.user.userId });
});

app.listen(3001, () => {
    console.log('Server running on port 3001');
    console.log('Server available at: http://localhost:3001');
});
