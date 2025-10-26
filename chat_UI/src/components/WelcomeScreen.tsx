import React from 'react';
import { Bot, Sparkles, MessageCircle } from 'lucide-react';

interface WelcomeScreenProps {
  onStartChat: () => void;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onStartChat }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full text-center">
        <div className="relative">
          <div className="absolute inset-0 -m-4">
            <div className="absolute top-0 left-1/4 w-32 h-32 bg-blue-200 rounded-full opacity-20 animate-pulse"></div>
            <div className="absolute bottom-0 right-1/4 w-24 h-24 bg-blue-300 rounded-full opacity-20 animate-pulse delay-1000"></div>
          </div>
          
          <div className="relative bg-white rounded-3xl shadow-2xl p-12 border border-blue-100">
            <div className="flex items-center justify-center mb-8">
              <div className="relative">
                <Bot className="w-16 h-16 text-blue-600 animate-bounce" />
                <Sparkles className="w-6 h-6 text-blue-400 absolute -top-2 -right-2 animate-ping" />
              </div>
            </div>
            
            <h1 className="text-5xl font-bold text-gray-900 mb-4">
              BOT<span className="text-blue-600">NET</span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 leading-relaxed">
              A smart and advanced chat experience<br />
              Ask any question and get accurate and professional answers.
            </p>
            
            <div className="grid md:grid-cols-3 gap-6 mb-10">
              <div className="flex flex-col items-center p-4 rounded-xl bg-blue-50 border border-blue-100 hover:shadow-lg transition-all duration-300">
                <MessageCircle className="w-8 h-8 text-blue-600 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Smart calls</h3>
                <p className="text-sm text-gray-600 text-center">Advanced chat with full memory</p>
              </div>
              
              <div className="flex flex-col items-center p-4 rounded-xl bg-blue-50 border border-blue-100 hover:shadow-lg transition-all duration-300">
                <Bot className="w-8 h-8 text-blue-600 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Artificial Intelligence</h3>
                <p className="text-sm text-gray-600 text-center">Advanced and accurate answers</p>
              </div>
              
              <div className="flex flex-col items-center p-4 rounded-xl bg-blue-50 border border-blue-100 hover:shadow-lg transition-all duration-300">
                <Sparkles className="w-8 h-8 text-blue-600 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Perfect experience</h3>
                <p className="text-sm text-gray-600 text-center">Convenient and user-friendly interface</p>
              </div>
            </div>
            
            {/* CTA Button */}
            <button
              onClick={onStartChat}
              className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-10 py-4 rounded-2xl text-lg font-semibold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 flex items-center mx-auto gap-3"
            >
              <MessageCircle className="w-6 h-6" />
              Start a new conversation
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WelcomeScreen;