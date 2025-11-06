
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string; 
  rating?: 'like' | 'dislike' | null;
  replyTo?: string | null;
  probability?: number; 
}

export interface Chat {
  id: string;
  title: string;
  messages: Message[];
  createdAt: string;
  updatedAt: string;
}