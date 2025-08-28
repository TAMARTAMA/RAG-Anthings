const fs = require('fs');
const path = require('path');
const chatsPath = path.join(__dirname, '../../project/chats.json');

// Simulated responses
const responses = [
  'Hello, how can I help you?',
  'This is a simulated response.',
  'Your request has been received.'
];

function loadChats() {
  try {
    if (!fs.existsSync(chatsPath)) return [];
    const data = fs.readFileSync(chatsPath, 'utf-8');
    return data ? JSON.parse(data) : [];
  } catch (e) {
    return [];
  }
}

function saveChats(chats) {
  fs.writeFileSync(chatsPath, JSON.stringify(chats, null, 2), 'utf-8');
}

const giveResponse = (req, res) => {
  try {
    const { userId, requset } = req.body;
    if (!userId || requset === undefined)
      return res.status(400).json({ error: "Missing fields" });

    // Load chat history
    let chats = loadChats();
    let chat = chats.find(c => c.userId === userId);
    if (!chat) {
      chat = {
        userId,
        messages: []
      };
      chats.push(chat);
    }

    // Add user message
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: requset,
      timestamp: new Date().toISOString(),
    };
    chat.messages.push(userMessage);

    // Add assistant message
    const responseMsg = responses[Math.floor(Math.random() * responses.length)];

    // Add assistant message with rating=null by default
    const assistantMessage = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: responseMsg,
      timestamp: new Date().toISOString(),
      replyTo: userMessage.id,
      rating: null
    };
  chat.messages.push(assistantMessage);

  // Save updated chats
    saveChats(chats);

    res.status(200).json({ message: responseMsg });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
const getHistory = (req, res) => {
  try {
    const userId = req.query.userId;
    if (!userId) return res.status(400).json({ error: 'Missing userId' });
    const chats = loadChats();
    const chat = chats.find(c => c.userId === userId);
    res.status(200).json(chat ? chat : { userId, messages: [] });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

// Endpoint to update rating for a specific assistant message
const rateMessage = (req, res) => {
  try {
    const { userId, messageId, rating } = req.body;
    if (!userId || !messageId || (rating !== 'like' && rating !== 'dislike' && rating !== null)) {
      return res.status(400).json({ error: 'Missing or invalid fields' });
    }
    let chats = loadChats();
    let chat = chats.find(c => c.userId === userId);
    if (!chat) return res.status(404).json({ error: 'Chat not found' });

    // Find the message by id regardless of role
    let msg = chat.messages.find(m => m.id === messageId);
    if (!msg) return res.status(404).json({ error: 'Message not found' });

    // If the found message is an assistant message, rate it directly
    if (msg.role === 'assistant') {
      msg.rating = rating;
      saveChats(chats);
      return res.status(200).json({ success: true });
    }

    // If the found message is a user message, try to find the assistant reply
    const assistantReply = chat.messages.find(m => m.role === 'assistant' && m.replyTo === messageId);
    if (!assistantReply) return res.status(404).json({ error: 'Assistant reply not found for this message' });
    assistantReply.rating = rating;
    saveChats(chats);
    res.status(200).json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

module.exports = { giveResponse, getHistory, rateMessage };