import { useState, useCallback, useEffect } from "react";
import { Chat, Message } from "../types/chat";
import { 
  sendMessageToAPI, 
  rateMessageToAPI, 
  getChatHistory,
  getSingleChat ,
  deleteChatFromServer
} from "../services/api";

export const useChats = (userId?: string | null, token?: string | null) => { 
  const [chats, setChats] = useState<Chat[]>([]);
  const [activeChat, setActiveChat] = useState<Chat | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // --- טוען היסטוריה ---
  useEffect(() => {
    const fetchChats = async () => {
      if (!userId || !token) return;
      try {
        setIsLoading(true);
        const data = await getChatHistory(userId, token);
        if (data?.chats) {
          const parsedChats: Chat[] = data.chats.map((c: any) => ({
            id: c.id,
            title: c.title || "Conversation",
            messages: (c.messages || []).map((m: any) => ({
              id: m.id,
              role: m.role,
              content: m.content,
              timestamp: m.timestamp,
              rating: m.rating ?? null,
              replyTo: m.replyTo ?? null,
              probability: m.probability,
              links: m.links || [],
            })),
            createdAt: c.createdAt || new Date().toISOString(),
            updatedAt: c.updatedAt || new Date().toISOString(),
          }));

          setChats(parsedChats);
          setActiveChat(parsedChats[0] ?? null);
        }
      } catch (err) {
        console.error("Error loading chat history:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchChats();
  }, [userId, token]);

  // --- יצירת שיחה חדשה ---
  const createNewChat = useCallback(() => {
    const now = new Date().toISOString();
    const newChat: Chat = {
      id: "pending",      // ← מזהה זמני עד שהשרת יחזיר chatId אמיתי
      title: "New conversation",
      messages: [],
      createdAt: now,
      updatedAt: now,
    };
    setChats((prev) => [newChat, ...prev]);
    setActiveChat(newChat);
    return newChat;
  }, []);

  // --- שליחת הודעה ---
  const sendMessage = useCallback(
    async (content: string, index?: any) => {
      if (!activeChat || !content.trim()) return;

      const now = new Date();
      const userMessage: Message = {
        id: now.getTime().toString(),
        role: "user",
        content: content.trim(),
        timestamp: now.toISOString(),
        rating: null,
        replyTo: null,
      };

      // עדכון מקומי מיידי
      const localChatUpdate: Chat = {
        ...activeChat,
        messages: [...activeChat.messages, userMessage],
        title:
          activeChat.messages.length === 0
            ? content.slice(0, 30) + (content.length > 30 ? "..." : "")
            : activeChat.title,
        updatedAt: new Date().toISOString(),
      };

      setActiveChat(localChatUpdate);
      setChats((prev) =>
        prev.map((c) => (c.id === activeChat.id ? localChatUpdate : c))
      );

      setIsLoading(true);

      try {
        // אם ה־chat עדיין pending, שולחים null
        const chatIdToSend =
          activeChat.id === "pending" ? null : activeChat.id;

        const { message, chatId, links } = await sendMessageToAPI(
          content,
          userId || "NoUser",
          index,
          chatIdToSend
        );

        // לאחר מכן, טוענים מהשרת רק את הצ'אט הספציפי
        const updatedChat = await getSingleChat(chatId, token!);

        // אם זה היה chat חדש → מחליפים את "pending" ב־chatId אמיתי
        if (activeChat.id === "pending") {
          setChats((prev) =>
            prev.map((c) =>
              c.id === "pending" ? updatedChat : c
            )
          );
        } else {
          // צ'אט קיים
          setChats((prev) =>
            prev.map((c) =>
              c.id === chatId ? updatedChat : c
            )
          );
        }

        setActiveChat(updatedChat);

      } catch (error) {
        console.error("Error sending message:", error);
      } finally {
        setIsLoading(false);
      }
    },
    [activeChat, userId, token]
  );

  // --- דירוג הודעה ---
  const rateMessage = useCallback(
    async (messageId: string, rating: "like" | "dislike" | null) => {
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

      await rateMessageToAPI(activeChat.id, messageId, rating);
    },
    [activeChat]
  );

  const selectChat = useCallback((chat: Chat) => setActiveChat(chat), []);

  const deleteChat = useCallback(
    async (chatId: string) => {
      if (!token) return;
      try {
        // מחיקה מהשרת
        await deleteChatFromServer(chatId, token);
        // מחיקה מקומית אחרי הצלחה
        setChats((prev) => prev.filter((chat) => chat.id !== chatId));
        if (activeChat?.id === chatId) {
          setActiveChat(null);
        }
      } catch (err) {
        console.error("Failed to delete chat:", err);
      }
    },
    [activeChat, token]
  );

  function clearChats() {
    setChats([]);
  }

  return {
    chats,
    activeChat,
    isLoading,
    createNewChat,
    sendMessage,
    selectChat,
    deleteChat,
    rateMessage,
    clearChats
  };
};

export default useChats;
