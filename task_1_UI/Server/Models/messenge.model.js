// Mongoose schema for Message and Chat based on frontend types
const mongoose = require('mongoose');

const MessageSchema = new mongoose.Schema({
  id: { type: String, required: true, unique: true },
  role: { type: String, enum: ['user', 'assistant'], required: true },
  content: { type: String, required: true },
  timestamp: { type: String, required: true }, // ISO8601 string
  rating: { type: String, enum: ['like', 'dislike', null], default: null },
  replyTo: { type: String, default: null },
});

const ChatSchema = new mongoose.Schema({
  id: { type: String, required: true, unique: true },
  title: { type: String, required: true },
  messages: { type: [MessageSchema], default: [] },
  createdAt: { type: String, required: true },
  updatedAt: { type: String, required: true },
});

module.exports = {
  Message: mongoose.model('Message', MessageSchema),
  Chat: mongoose.model('Chat', ChatSchema),
};
