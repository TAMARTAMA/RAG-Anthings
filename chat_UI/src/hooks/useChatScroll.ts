import { useEffect } from 'react';
import { Chat } from '../types/chat';

export const useChatScroll = (
  ref: React.RefObject<HTMLDivElement>,
  chat: Chat | null
) => {
  useEffect(() => {
    ref.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chat?.messages]);
};
