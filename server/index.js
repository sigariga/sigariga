const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs-extra');
const helmet = require('helmet');
const compression = require('compression');
const morgan = require('morgan');
require('dotenv').config();

const templatesRouter = require('./routes/templates');
const contentRouter = require('./routes/content');
const exportRouter = require('./routes/export');
const chatbotRouter = require('./routes/chatbot');
const flowchartRouter = require('./routes/flowchart');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(helmet());
app.use(compression());
app.use(morgan('combined'));
app.use(cors());
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Ensure required directories exist
const requiredDirs = [
  './uploads',
  './exports',
  './templates',
  './content',
  './flowcharts'
];

requiredDirs.forEach(dir => {
  fs.ensureDirSync(path.join(__dirname, dir));
});

// Routes
app.use('/api/templates', templatesRouter);
app.use('/api/content', contentRouter);
app.use('/api/export', exportRouter);
app.use('/api/chatbot', chatbotRouter);
app.use('/api/flowchart', flowchartRouter);

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ 
    error: 'Something went wrong!',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Internal server error'
  });
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});