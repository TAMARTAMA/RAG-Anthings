import React, { useState, useRef } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { Chat } from '../types/chat';
import ChatMessage from './ChatMessage';
import VoiceRecorder from './VoiceRecorder';
import { useChatScroll } from '../hooks/useChatScroll';

interface ChatInterfaceProps {
  activeChat: Chat | null;
  isLoading: boolean;
  onSendMessage: (message: string) => void;
  onRateMessage: (messageId: string, rating: 'like' | 'dislike' | null) => void;
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

  useChatScroll(messagesEndRef, activeChat);

  const handleSubmit = (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputMessage.trim() || isLoading) return;
    onSendMessage(inputMessage);
    setInputMessage('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
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
      {/* Header */}
      <div className="border-b border-gray-200 p-4 bg-white text-right">
        <h2 className="text-lg font-semibold text-gray-900">{activeChat.title}</h2>
        <p className="text-sm text-gray-500">{activeChat.messages.length} messages</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-1 px-4 py-2">
        {activeChat.messages.map((message) => (
          <ChatMessage key={message.id} message={message} onRate={onRateMessage} />
        ))}

        {isLoading && (
          <div className="flex gap-4 p-4">
            <Loader2 className="w-5 h-5 text-gray-600 animate-spin" />
            <p className="text-sm text-gray-600">BOT&lt;NET writing...</p>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 bg-gray-50 p-4">
        <form
          onSubmit={handleSubmit}
          className="flex items-end gap-2 bg-white border border-gray-300 rounded-2xl shadow-sm p-2 focus-within:ring-2 focus-within:ring-blue-500"
        >
          {/* כפתורי שליחה והקלטה בצד ימין */}
          <div className="flex items-center gap-2 pr-1">
            <VoiceRecorder
              inputRef={inputRef}
              onTranscription={(text) => setInputMessage(text)}
            />

            <button
              type="submit"
              disabled={!inputMessage.trim() || isLoading}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white p-3 rounded-xl transition-colors duration-200"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </div>

          {/* שדה הקלט */}
          <textarea
            ref={inputRef}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask BOT<NET> any question..."
            className="flex-1 resize-none outline-none px-3 py-2 text-right text-gray-900 placeholder-gray-400 rounded-xl bg-transparent"
            rows={1}
          />
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;
