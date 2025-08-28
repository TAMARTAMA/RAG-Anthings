
export async function sendMessageToAPI(message: string): Promise<string> {
  try {
    const response = await fetch('http://localhost:5000/api/message/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ requset: message, userId: 'testUser' }), // Replace userId as needed
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || 'Failed to send message');
    }
    return data.message || 'Message sent!';
  } catch (error: any) {
    return `Error: ${error.message}`;
  }
}