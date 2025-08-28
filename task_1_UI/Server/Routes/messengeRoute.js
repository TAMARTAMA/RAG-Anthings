const router = require('express').Router();
const { giveResponse, getHistory, rateMessage } = require('../Controllers/messengeController');

// Message response route
router.post('/add', giveResponse);
// Chat history route
router.get('/history', getHistory);

// Rate assistant message
router.post('/rate', rateMessage);

module.exports = router;