import { User } from "lucide-react";

// const PORT_MAIN_SERVER = "https://television-man-recommendations-cast.trycloudflare.com";
const PORT_MAIN_SERVER = "http://localhost:8004";

export type AuthUser = { id: string; indexs: string[] };
export type AuthResp = { user: AuthUser; access_token: string; token_type: string };

export async function signup(userId: string, password: string): Promise<AuthResp> {
  const r = await fetch(`${PORT_MAIN_SERVER}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId, password })
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function login(userId: string, password: string): Promise<AuthResp> {
  const r = await fetch(`${PORT_MAIN_SERVER}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId, password })
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function getIndexes(token: string): Promise<string[]> {
  const r = await fetch(`${PORT_MAIN_SERVER}/auth/indexes`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!r.ok) throw new Error(await r.text());
  const data = await r.json();
  return data.indexs || ["wikipedia"];
}

export async function addIndex(token: string, userId: string, index: string, files?: File[]) {
  const form = new FormData();
  form.append("user_id", userId);
  form.append("index_name", index);
  if (files) {
    for (const f of files) {
      form.append("files", f);
    }
  }

  const r = await fetch(`${PORT_MAIN_SERVER}/api/message/add_index`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  

  if (!r.ok) throw new Error(await r.text());
  return r.json();
}


export async function removeIndex(token: string, index: string, UserId: string) {
  const r = await fetch(`${PORT_MAIN_SERVER}/api/message/remove_index`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ index ,UserId}),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json() as Promise<{ user: AuthUser }>;
}
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
  userId: string,
  index: string,
  chatId?: string | null
): Promise<{ 
  message: string; 
  chatId: string; 
  links?: { title: string; url: string }[]; 
}> 
{
  try {
    const response = await fetch(`${PORT_MAIN_SERVER}/api/message/add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        request: message,
        userId,
        index,
        chatId: chatId || null   // ← חשוב: אם "pending" מגיע, שולחים null
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Failed to send message");
    }

    return {
      message: data.answer,
      chatId: data.chatId,
      links: data.links || [],
    };

  } catch (error: any) {
    return {
      message: `Error: ${error.message}`,
      chatId: "",
      links: [],
    };
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
export async function getChatHistory(userId: string, token: string) {
  const res = await fetch(`${PORT_MAIN_SERVER}/api/message/history?userId=${userId}`, {
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) throw new Error("Failed to load chat history");
  return res.json();
}

export async function getSingleChat(chatId: string, token: string) {
  const res = await fetch(`${PORT_MAIN_SERVER}/api/message/chat/${chatId}`, {
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`,
    }
  });

  if (!res.ok) throw new Error("Failed to load chat");

  return res.json();
}
