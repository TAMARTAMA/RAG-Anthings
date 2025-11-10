
const PORT_MAIN_SERVER = "https://television-man-recommendations-cast.trycloudflare.com";


export async function rateMessageToAPI(userId: string, messageId: string, rating: 'like' | 'dislike' | null) {
  try {
    const response = await fetch(`${PORT_MAIN_SERVER}/api/message/rate`, {
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
): Promise<{ message: string; messageId?: string; chatHistory?: any, links?: { title: string; url: string }[] }>  {
  try {
    const response = await fetch(`${PORT_MAIN_SERVER}/api/message/add`, {
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
    
    return { message: data.answer || 'Message sent!', messageId: data.messageId ,chatHistory: data.chatHistory,
    links: data.links || [],};
  } catch (error: any) {
    return { message: `Error: ${error.message}` };
  }
}
export async function getProbabilityFromServer(
  question: string,
  answer: string
): Promise<{ probability?: number; error?: string }> {
  try {
    const response = await fetch(`${PORT_MAIN_SERVER}/api/prob/get_probalitiy`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question, answer }),
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const data = await response.json();
    return { probability: data.probability };
  } catch (err: any) {
    console.error(" Error fetching probability:", err);
    return { error: err.message };
  }
}
// Optionally, fetch the full chat history after sending a message
    // let chatHistory;
    // try {
    //   const historyRes = await fetch(PORT_MAIN_SERVER+`api/message/history?userId=${encodeURIComponent(userId)}`);
    //   chatHistory = await historyRes.json();
    // } catch {}