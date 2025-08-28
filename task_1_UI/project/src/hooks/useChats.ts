
import { useState, useCallback, useEffect } from 'react';
import { Chat, Message } from '../types/chat';
import { sendMessageToAPI } from '../services/api';
import { loadChats, saveChats } from '../storage';

export const useChats = () => {
  const initialChats = loadChats();
  const [chats, setChats] = useState<Chat[]>(initialChats);
  const [activeChat, setActiveChat] = useState<Chat | null>(
    initialChats[0] ?? null
  );
  const [isLoading, setIsLoading] = useState(false);

  const createNewChat = useCallback(() => {
    const now = new Date().toISOString();
    const newChat: Chat = {
      id: Date.now().toString(),
      title: 'שיחה חדשה',
      messages: [],
      createdAt: now,
      updatedAt: now,
    };

    setChats((prev) => [newChat, ...prev]);
    setActiveChat(newChat);
    return newChat;
  }, []);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!activeChat || !content.trim()) return;

      const now = new Date();
      const userMessage: Message = {
        id: now.getTime().toString(),
        role: 'user',
        content: content.trim(),
        timestamp: now.toISOString(),
        rating: null,
        replyTo: null,
      };

      const updatedChat: Chat = {
        ...activeChat,
        messages: [...activeChat.messages, userMessage],
        title:
          activeChat.messages.length === 0
            ? content.slice(0, 30) + (content.length > 30 ? '...' : '')
            : activeChat.title,
        updatedAt: new Date().toISOString(),
      };

      setActiveChat(updatedChat);
      setChats((prev) =>
        prev.map((chat) => (chat.id === activeChat.id ? updatedChat : chat))
      );

      setIsLoading(true);
      try {
        const response = await sendMessageToAPI(content);

        const botMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: response,
          timestamp: new Date().toISOString(),
          rating: null,
          replyTo: userMessage.id,
        };

        const finalChat: Chat = {
          ...updatedChat,
          messages: [...updatedChat.messages, botMessage],
          updatedAt: new Date().toISOString(),
        };

        setActiveChat(finalChat);
        setChats((prev) =>
          prev.map((chat) => (chat.id === activeChat.id ? finalChat : chat))
        );
      } catch (error) {
        console.error('Error sending message:', error);
      } finally {
        setIsLoading(false);
      }
    },
    [activeChat]
  );

  const rateMessage = useCallback(
    (messageId: string, rating: 'like' | 'dislike' | null) => {
      if (!activeChat) return;

      const updatedMessages = activeChat.messages.map((m) =>
        m.id === messageId ? { ...m, rating } : m
      );

      const updatedChat: Chat = {
        ...activeChat,
        messages: updatedMessages,
        updatedAt: new Date().toISOString(),
      };

      setActiveChat(updatedChat);
      setChats((prev) =>
        prev.map((chat) => (chat.id === activeChat.id ? updatedChat : chat))
      );
    },
    [activeChat]
  );

  const selectChat = useCallback((chat: Chat) => {
    setActiveChat(chat);
  }, []);

  const deleteChat = useCallback(
    (chatId: string) => {
      setChats((prev) => prev.filter((chat) => chat.id !== chatId));
      if (activeChat?.id === chatId) {
        setActiveChat(null);
      }
    },
    [activeChat]
  );

  useEffect(() => {
    saveChats(chats);
  }, [chats]);

  return {
    chats,
    activeChat,
    isLoading,
    createNewChat,
    sendMessage,
    selectChat,
    deleteChat,
    rateMessage,
  };
};

export default useChats;