const express = require('express')
const app = express()

const bodyParser = require('body-parser')
app.use(bodyParser.json())
const env=require('dotenv')
env.config()

// Enable CORS for all origins (development only)
const cors = require('cors');
app.use(cors());


const jwt = require('jsonwebtoken')


app.use((req, res, next) => {
    console.log(new Date().toISOString(), req.method, req.url)
    next()
  })
  
  // --- NEW: simple health endpoint ---
  app.get('/healthz', (req, res) => res.send('ok'))
  
  // Import messengeRoute
  const messengeRoute = require('./Routes/messengeRoute')
  
  // Mount the message route at /api/message
  app.use('/api/message', messengeRoute)
  
  // --- NEW: global error handler to avoid “empty reply” ---
  app.use((err, req, res, next) => {
    console.error('Unhandled error:', err)
    res.status(500).json({ error: 'internal' })
  })
  
  app.listen(process.env.PORT, '0.0.0.0', () => {
    console.log(`listening on port ${process.env.PORT}`)
  })