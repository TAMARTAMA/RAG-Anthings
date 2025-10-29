const PORT_MAIN_SERVER = "http://192.168.50.3:8002/"
export async function rateMessageToAPI(userId: string, messageId: string, rating: 'like' | 'dislike' | null) {
  try {
    const response = await fetch(PORT_MAIN_SERVER+'api/message/rate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ userId, messageId, rating }),
    });
    return await response.json();
  } catch (error: any) {
    return { error: error.message };
  }
}

export async function sendMessageToAPI(
  message: string,
  userId: string
): Promise<{ message: string; messageId?: string; chatHistory?: any }>  {
  try {
    const response = await fetch(PORT_MAIN_SERVER+'api/message/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ request: message, userId }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to send message');
    }
    
    return { message: data.answer || 'Message sent!', messageId: data.messageId };
  } catch (error: any) {
    return { message: `Error: ${error.message}` };
  }
}
// Optionally, fetch the full chat history after sending a message
    // let chatHistory;
    // try {
    //   const historyRes = await fetch(PORT_MAIN_SERVER+`api/message/history?userId=${encodeURIComponent(userId)}`);
    //   chatHistory = await historyRes.json();
    // } catch {}