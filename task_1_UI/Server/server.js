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


// Import messengeRoute
const messengeRoute = require('./Routes/messengeRoute');


// Only use the message API route


// Mount the message route at /api/message
app.use('/api/message', messengeRoute);

app.listen(process.env.PORT, () => {
    console.log(`listening on port ${process.env.PORT}`);
})