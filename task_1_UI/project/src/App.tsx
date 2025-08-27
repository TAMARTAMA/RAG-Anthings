import React, { useState } from 'react';
import WelcomeScreen from './components/WelcomeScreen';
import ChatSidebar from './components/ChatSidebar';
import ChatInterface from './components/ChatInterface';
import { useChats } from './hooks/useChats';

function App() {
  const [showWelcome, setShowWelcome] = useState(true);
  const {
    chats,
    activeChat,
    isLoading,
    createNewChat,
    sendMessage,
    selectChat,
    deleteChat,
  } = useChats();

  const handleStartChat = () => {
    setShowWelcome(false);
    createNewChat();
  };

  if (showWelcome) {
    return <WelcomeScreen onStartChat={handleStartChat} />;
  }

  return (
    <div className="h-screen bg-gray-50 flex" dir="rtl">
      <ChatSidebar
        chats={chats}
        activeChat={activeChat}
        onNewChat={createNewChat}
        onSelectChat={selectChat}
        onDeleteChat={deleteChat}
      />
      
      <ChatInterface
        activeChat={activeChat}
        isLoading={isLoading}
        onSendMessage={sendMessage}
      />
    </div>
  );
}

export default App;