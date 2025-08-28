import React from 'react';
import { ThumbsUp, ThumbsDown } from 'lucide-react';
import { Message } from '../types/chat';

interface ChatMessageProps {
  message: Message;
  onRate: (id: string, rating: 'like' | 'dislike' | null) => void;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, onRate }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex gap-4 p-4 ${isUser ? 'flex-row-reverse' : ''}`}>
      <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">
        {isUser ? '👤' : '🤖'}
      </div>
      <div className="flex-1 max-w-3xl">
        <div
          className={`rounded-2xl p-4 ${
            isUser
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 text-gray-900'
          }`}
        >
          <p className="text-sm">{message.content}</p>
        </div>

        {!isUser && (
          <div className="flex gap-2 justify-end mt-2">
            <button
              onClick={() => onRate(message.id, message.rating === 'like' ? null : 'like')}
              className={`p-1 rounded-full transition-colors duration-200 ${
                message.rating === 'like' ? 'text-yellow-500' : 'text-gray-400'
              }`}
            >
              <ThumbsUp className="w-4 h-4" />
            </button>
            <button
              onClick={() => onRate(message.id, message.rating === 'dislike' ? null : 'dislike')}
              className={`p-1 rounded-full transition-colors duration-200 ${
                message.rating === 'dislike' ? 'text-yellow-500' : 'text-gray-400'
              }`}
            >
              <ThumbsDown className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatMessage;