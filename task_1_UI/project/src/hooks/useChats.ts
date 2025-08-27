import { useState, useCallback } from 'react';
import { Chat, Message } from '../types/chat';
import { sendMessageToAPI } from '../services/api';

export const useChats = () => {
  const [chats, setChats] = useState<Chat[]>([]);
  const [activeChat, setActiveChat] = useState<Chat | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const createNewChat = useCallback(() => {
    const newChat: Chat = {
      id: Date.now().toString(),
      title: 'שיחה חדשה',
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    setChats(prev => [newChat, ...prev]);
    setActiveChat(newChat);
    return newChat;
  }, []);

  const sendMessage = useCallback(async (text: string) => {
    if (!activeChat || !text.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: text.trim(),
      isUser: true,
      timestamp: new Date(),
    };

    // Update chat with user message
    const updatedChat = {
      ...activeChat,
      messages: [...activeChat.messages, userMessage],
      title: activeChat.messages.length === 0 ? text.slice(0, 30) + (text.length > 30 ? '...' : '') : activeChat.title,
      updatedAt: new Date(),
    };

    setActiveChat(updatedChat);
    setChats(prev => prev.map(chat => chat.id === activeChat.id ? updatedChat : chat));

    // Send to API and get response
    setIsLoading(true);
    try {
      const response = await sendMessageToAPI(text);
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response,
        isUser: false,
        timestamp: new Date(),
      };

      const finalChat = {
        ...updatedChat,
        messages: [...updatedChat.messages, botMessage],
        updatedAt: new Date(),
      };

      setActiveChat(finalChat);
      setChats(prev => prev.map(chat => chat.id === activeChat.id ? finalChat : chat));
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsLoading(false);
    }
  }, [activeChat]);

  const selectChat = useCallback((chat: Chat) => {
    setActiveChat(chat);
  }, []);

  const deleteChat = useCallback((chatId: string) => {
    setChats(prev => prev.filter(chat => chat.id !== chatId));
    if (activeChat?.id === chatId) {
      setActiveChat(null);
    }
  }, [activeChat]);

  return {
    chats,
    activeChat,
    isLoading,
    createNewChat,
    sendMessage,
    selectChat,
    deleteChat,
  };
};