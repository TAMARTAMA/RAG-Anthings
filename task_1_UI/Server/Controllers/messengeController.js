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
    const assistantMessage = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: responseMsg,
      timestamp: new Date().toISOString(),
      replyTo: userMessage.id
    };
    chat.messages.push(assistantMessage);

    // Save updated chats
    saveChats(chats);

    res.status(200).json({ message: responseMsg });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
module.exports = { giveResponse };