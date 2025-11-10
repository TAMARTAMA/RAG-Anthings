import { Chat } from './types/chat';

const STORAGE_KEY = 'chatHistory';

export function loadChats(): Chat[] {
  if (typeof window === 'undefined') return [];
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? (JSON.parse(stored) as Chat[]) : [];
  } catch (err) {
    console.error('Failed to load chats from storage', err);
    return [];
  }
}

export function saveChats(chats: Chat[]): void {
  if (typeof window === 'undefined') return;
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(chats));
  } catch (err) {
    console.error('Failed to save chats to storage', err);
  }
}