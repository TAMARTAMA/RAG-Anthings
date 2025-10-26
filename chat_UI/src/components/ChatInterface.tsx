import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { Chat } from '../types/chat';
import ChatMessage from './ChatMessage';

interface ChatInterfaceProps {
  activeChat: Chat | null;
  isLoading: boolean;
  onSendMessage: (message: string) => void;
  onRateMessage: (
    messageId: string,
    rating: 'like' | 'dislike' | null
  ) => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  activeChat,
  isLoading,
  onSendMessage,
  onRateMessage,
}) => {
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [activeChat?.messages]);

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, [activeChat]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;

    onSendMessage(inputMessage);
    setInputMessage('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  if (!activeChat) {
    return (
      <div className="flex-1 flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="w-24 h-24 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Send className="w-12 h-12 text-blue-600" />
          </div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">
            Select a conversation or start a new one
          </h2>
          <p className="text-gray-500">
            Create a new conversation to start chatting with BOT&lt;NET
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* Chat Header */}
      <div className="border-b border-gray-200 p-4 bg-white">
        <h2 className="text-lg font-semibold text-gray-900 text-right">
          {activeChat.title}
        </h2>
        <p className="text-sm text-gray-500 text-right">
          {activeChat.messages.length} messages
        </p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        {activeChat.messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <div className="text-center">
              <p className="text-lg mb-2">Start a new conversation</p>
              <p className="text-sm">Ask any question that interests you</p>
            </div>
          </div>
        ) : (
          <div className="space-y-1">
            {activeChat.messages.map((message) => (
              <ChatMessage
                key={message.id}
                message={message}
                onRate={onRateMessage}
              />
            ))}

            {isLoading && (
              <div className="flex gap-4 p-4">
                <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">
                  <Loader2 className="w-5 h-5 text-gray-600 animate-spin" />
                </div>
                <div className="flex-1 max-w-3xl">
                  <div className="bg-gray-100 rounded-2xl p-4">
                    <p className="text-sm text-gray-600">BOT&lt;NET writing...</p>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        )}
      </div>


      <div className="border-t border-gray-200 p-4 bg-white">
        <form onSubmit={handleSubmit} className="flex gap-3">
          <button
            type="submit"
            disabled={!inputMessage.trim() || isLoading}
            className="flex-shrink-0 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white p-3 rounded-xl transition-colors duration-200"
          >
            {isLoading ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>

          <textarea
            ref={inputRef}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask BOT<NET any question..."
            className="flex-1 resize-none border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-right"
            rows={1}
            style={{ minHeight: '48px', maxHeight: '120px' }}
            disabled={isLoading}
          />
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;