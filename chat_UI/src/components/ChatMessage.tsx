import React, { useState, useEffect } from 'react';
import { ThumbsUp, ThumbsDown, Volume2, Square } from 'lucide-react';
import { Message } from '../types/chat';
import { getProbabilityFromServer } from '../services/api';
interface ChatMessageProps {
  message: Message;
  onRate: (id: string, rating: 'like' | 'dislike' | null) => void;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, onRate }) => {
  const isUser = message.role === 'user';
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [rerender, setRerender] = useState(0);

  const synth = window.speechSynthesis;

  useEffect(() => {
    return () => {
      synth.cancel();
    };
  }, []);
useEffect(() => {
    const fetchProbability = async () => {
      if (!isUser && message.content && !message.probability) {
        try {
          const res = await getProbabilityFromServer(
            message.replyTo || "User question", 
            message.content
          );

          if (res.probability !== undefined) {
            message.probability = res.probability;
            setRerender((r) => r + 1);
          }
        } catch (err) {
          console.error(" Failed to get probability:", err);
        }
      }
    };

    fetchProbability();
  }, [message.content]);
  const handleSpeak = () => {
    if (isSpeaking) {
      synth.cancel();
      setIsSpeaking(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(message.content);
    utterance.lang = 'en-US';
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    synth.cancel();
    synth.speak(utterance);
  };

  return (
    <div className={`flex gap-4 p-4 ${isUser ? 'flex-row-reverse' : ''}`}>
      <div className="flex-shrink-0 w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">
        {isUser ? '👤' : '🤖'}
      </div>

      <div className="flex-1 max-w-3xl">
        <div
          className={`rounded-2xl p-4 ${isUser ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-900'}`}
        >
          <p className="text-sm">{message.content}</p>

          {/* Links display */}
          {message.links && message.links.length > 0 && (
            <div className="mt-2 space-y-1">
              {message.links.map((link, idx) => (
                <div key={idx} className="text-xs flex items-center gap-2">
                  <span className="font-medium text-gray-700">{link.title}</span>
                  <a
                    href={link.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    {link.url!= "No URL" ? link.url :""}
                  </a>
                </div>
              ))}
            </div>
          )}
        </div>

        {!isUser && (
          <div className="flex gap-3 justify-end mt-2 items-center">
            {/* Probability display */}
            {message.probability !== undefined && (
              <div
                className="flex items-center gap-1 text-xs font-medium text-gray-600 bg-white border border-gray-200 rounded-full px-3 py-1 shadow-sm"
                title="Answer confidence"
              >
<span className="text-blue-600">
  {((message.probability / 10) * 100).toFixed(0)}%
</span>
                <span className="text-gray-400">confidence</span>
              </div>
            )}

            {/* Speech button */}
            <button
              onClick={handleSpeak}
              title={isSpeaking ? 'Stop reading' : 'Read aloud'}
              className={`p-1 rounded-full transition-colors duration-200 ${
                isSpeaking ? 'text-red-500 animate-pulse' : 'text-gray-400 hover:text-blue-500'
              }`}
            >
              {isSpeaking ? <Square className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            </button>

            {/* Rating buttons */}
            <button
              onClick={() =>
                onRate(message.id, message.rating === 'like' ? null : 'like')
              }
              className={`p-1 rounded-full transition-colors duration-200 ${
                message.rating === 'like' ? 'text-yellow-500' : 'text-gray-400 hover:text-yellow-500'
              }`}
            >
              <ThumbsUp className="w-4 h-4" />
            </button>

            <button
              onClick={() =>
                onRate(message.id, message.rating === 'dislike' ? null : 'dislike')
              }
              className={`p-1 rounded-full transition-colors duration-200 ${
                message.rating === 'dislike' ? 'text-yellow-500' : 'text-gray-400 hover:text-yellow-500'
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