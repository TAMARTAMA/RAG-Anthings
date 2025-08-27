import React from 'react';
import { User, Bot } from 'lucide-react';
import { Message } from '../types/chat';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('he-IL', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    });
  };

  return (
    <div className={`flex gap-4 p-4 ${message.isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
        message.isUser 
          ? 'bg-blue-600 text-white' 
          : 'bg-gray-100 text-gray-600'
      }`}>
        {message.isUser ? (
          <User className="w-5 h-5" />
        ) : (
          <Bot className="w-5 h-5" />
        )}
      </div>

      {/* Message Content */}
      <div className={`flex-1 max-w-3xl ${message.isUser ? 'text-right' : 'text-right'}`}>
        <div className={`rounded-2xl p-4 ${
          message.isUser
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-900'
        }`}>
          <p className="text-sm leading-relaxed whitespace-pre-wrap">
            {message.text}
          </p>
        </div>
        
        <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
          <span>{formatTime(message.timestamp)}</span>
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;