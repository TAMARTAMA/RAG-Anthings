const express = require('express')//יבוא
const app = express()//מימוש שרת של מודול אקספרס
const PORT = 5000//פורט להאזנת השרת
const bodyParser = require('body-parser')//ספריה להמרת אובייקטים לגייסון - שימושי לנו לאובייקטים שנשלחים בBODY
app.use(bodyParser.json())//הפונקציה שממירה את האובייקטים לגייסון
const env=require('dotenv')//ספריה לשימוש בקובץ 
env.config()
//מודול שנותן לנו להשתמש בקובץ מערכת למשתני סביבה - dotenv  
// הגישה למשתנים שרשומים שם - process.env.VARIABLE_NAME
//מחזיר אובייקט המייצג את תוכן הקובץ 

const jwt = require('jsonwebtoken')//ספריה ליצירת מחרוזת טוקן להצפנת פרטי משתמש לשימוש ברשת

// ...existing code...

// Import messengeRoute
const messengeRoute = require('./Routes/messengeRoute');


// Only use the message API route


// Mount the message route at /api/message
app.use('/api/message', messengeRoute);

app.listen(process.env.PORT, () => {
    console.log(`listening on port ${process.env.PORT}`);
})