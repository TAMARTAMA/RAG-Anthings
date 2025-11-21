import React from 'react';
import { Bot, Sparkles, MessageCircle } from 'lucide-react';

interface WelcomeScreenProps {
  onStartChat: () => void;
}

const WelcomeScreen: React.FC<WelcomeScreenProps> = ({ onStartChat }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-100 flex items-center justify-center p-4">
      <div className="max-w-3xl w-full text-center"> {/* increased max width */}
        <div className="relative">
          <div className="absolute inset-0 -m-4">
            <div className="absolute top-0 left-1/4 w-32 h-32 bg-blue-200 rounded-full opacity-20 animate-pulse"></div>
            <div className="absolute bottom-0 right-1/4 w-24 h-24 bg-blue-300 rounded-full opacity-20 animate-pulse delay-1000"></div>
          </div>

          <div className="relative bg-white rounded-3xl shadow-2xl p-16 border border-blue-100"> {/* bigger box */}
            <div className="flex flex-col items-center justify-center mb-6 gap-2">
              <div className="relative">
                <Bot className="w-16 h-16 text-blue-600 animate-bounce" />
                <Sparkles className="w-6 h-6 text-blue-400 absolute -top-2 -right-2 animate-ping" />
              </div>
              <span className="text-sm font-medium tracking-wide text-blue-600 uppercase">
                Welcome to
              </span>
            </div>

            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              RAG<span className="text-blue-600"> Anything</span>
            </h1>

            <p className="text-xl text-gray-600 mb-12 leading-relaxed">
              A flexible and intelligent RAG-powered chatbot designed to answer questions,
              explore information, and adapt to your data — all in one clean, modern interface.
            </p>

            <div className="grid md:grid-cols-3 gap-6 mb-12">
              <div className="flex flex-col items-center p-6 rounded-xl bg-blue-50 border border-blue-100 hover:shadow-lg transition-all duration-300">
                <MessageCircle className="w-8 h-8 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">
                  Ask Anything
                </h3>
                <p className="text-sm text-gray-600 text-center">
                  Start chatting instantly and get high-quality answers.
                </p>
              </div>

              <div className="flex flex-col items-center p-6 rounded-xl bg-blue-50 border border-blue-100 hover:shadow-lg transition-all duration-300">
                <Bot className="w-8 h-8 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">
                  Add Your Data
                </h3>
                <p className="text-sm text-gray-600 text-center">
                  Upload documents, create indexes, and expand your knowledge base.
                </p>
              </div>

              <div className="flex flex-col items-center p-6 rounded-xl bg-blue-50 border border-blue-100 hover:shadow-lg transition-all duration-300">
                <Sparkles className="w-8 h-8 mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">
                  Index-Aware Answers
                </h3>
                <p className="text-sm text-gray-600 text-center">
                  Choose an index and get tailored contextual answers.                </p>
              </div>
            </div>

            <button
              onClick={onStartChat}
              className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 
                         text-white px-10 py-4 rounded-2xl text-lg font-semibold shadow-lg hover:shadow-xl 
                         transform hover:scale-105 transition-all duration-300 flex items-center mx-auto gap-3"
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
