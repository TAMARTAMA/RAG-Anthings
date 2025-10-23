
// /home/ext-z/Moptimizer/task_1_UI/Server/Controllers/messengeController.js
// Keeps your original functions; only switches the assistant response to call the Python FastAPI model.
// Requires: npm install node-fetch@2

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');

const chatsPath = path.resolve(__dirname, '../../project/chats.json');

// Keep your original simulated responses array as a fallback
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

const MODEL_URL = process.env.MODEL_URL || 'http://127.0.0.1:8001/generate';

// === Only this function is altered to call the model; the rest stays the same ===
const giveResponse = async (req, res) => {
  try {
    const { userId, requset } = req.body; // משאיר את השם המקורי "requset"
    if (!userId || requset === undefined) {
      return res.status(400).json({ error: 'Missing fields' });
    }

    // 1) נירמול קלט: תמיד מחרוזת
    let userText = typeof requset === 'string' ? requset : String(requset ?? '');
    userText = userText.trim();
    

    // (אופציונלי) אם שדה הקלט הוא רק מספר ארוך (10–16 ספרות) — סביר שזה ID בטעות
    // לא חוסם, רק מתעד לוג כדי שתדעי לזהות
    if (/^\d{10,16}$/.test(userText)) {
      console.warn('[warn] received numeric-only input (looks like an ID):', userText);
    }

    // 2) טעינת היסטוריה
    let chats = loadChats();
    let chat = chats.find(c => c.userId === userId);
    if (!chat) {
      chat = { userId, messages: [] };
      chats.push(chat);
    }

    // 3) הוספת הודעת משתמש (שומר את הטקסט, לא מזהה)
    const userMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: userText,
      timestamp: new Date().toISOString(),
    };
    chat.messages.push(userMessage);

    // 4) קריאה למודל (FastAPI)
    let responseMsg;
    try {
      const body = {
        prompt: userText,
        num_samples: 1,
        max_new_tokens: 120,
        temperature: 0.4,  // מעט "קר" לשיפור קוהרנטיות
        top_k: 60,
        seed: 0,
        seed_increment: true
      };

      const resp = await fetch(MODEL_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
        timeout: 60000
      });

      if (!resp.ok) {
        const errText = await resp.text();
        throw new Error(`Model server error ${resp.status}: ${errText}`);
      }

      const data = await resp.json();
      const rawText = data?.completions?.[0] ?? '';

      // 5) ניקוי מספר/טיימסטמפ שמופיע בתחילת תשובת המודל
      //    (10–16 ספרות בתחילת הטקסט + רווח/שורה חדשה)
      const cleaned = String(rawText)
        .replace(/^\s*\d{10,16}\s*(\r?\n)?/, '')
        .trim();

      if (cleaned !== rawText) {
        console.log('[cleaned-leading-id]', rawText.slice(0, 40), '=>', cleaned.slice(0, 40));
      }

      responseMsg = cleaned || responses[Math.floor(Math.random() * responses.length)];
    } catch (e) {
      console.error('Model call failed:', e.message);
      responseMsg = responses[Math.floor(Math.random() * responses.length)]; // נפילה -> fallback
    }

    // 6) הוספת הודעת הסייען (עם תוכן נקי)
    const assistantMessage = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: responseMsg,
      timestamp: new Date().toISOString(),
      replyTo: userMessage.id,
      rating: null
    };
    chat.messages.push(assistantMessage);

    // 7) שמירה והחזרה ללקוח
    saveChats(chats);
    return res.status(200).json({ message: responseMsg });
  } catch (error) {
    console.error('giveResponse error:', error);
    return res.status(500).json({ error: error.message });
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

module.exports = { giveResponse, getHistory, rateMessage };
