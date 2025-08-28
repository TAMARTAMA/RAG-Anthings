const router = require('express').Router();
const { giveResponse } = require('../Controllers/messengeController');

// Only the message response route is used
router.post('/add', giveResponse);

module.exports = router;