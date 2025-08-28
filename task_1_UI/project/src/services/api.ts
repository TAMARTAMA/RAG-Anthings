
export async function sendMessageToAPI(message: string): Promise<{ message: string; chatHistory?: any }> {
  try {
    const response = await fetch('http://localhost:5000/api/message/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ requset: message, userId: 'testUser' }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to send message');
    }
    // Optionally, fetch the full chat history after sending a message
    let chatHistory;
    try {
      const historyRes = await fetch('http://localhost:5000/api/message/history?userId=testUser');
      chatHistory = await historyRes.json();
    } catch {}
    return { message: data.message || 'Message sent!', chatHistory };
  } catch (error: any) {
    return { message: `Error: ${error.message}` };
  }
}