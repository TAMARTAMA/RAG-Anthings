// Simulated API service - replace with your actual API endpoint
//TODO change to real API call
export const sendMessageToAPI = async (message: string): Promise<string> => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
  
  // Simulated responses - replace with actual API call
  const responses = [
    `שלום! קיבלתי את השאלה שלך: "${message}". זוהי תשובה מדומה מ-BOT<NET.`,
    `מעניין! בקשר לשאלתך "${message}" - אני יכול לעזור לך עם זה. זוהי דוגמה לתשובה.`,
    `תודה על השאלה "${message}". אני מעבד את המידע ומחזיר לך תשובה רלוונטית.`,
    `בהתבסס על השאלה שלך "${message}", הנה התובנות שלי בנושא.`,
    `אני מבין שאתה שואל על "${message}". תן לי לספק לך מידע מפורט בנושא.`
  ];
  
  return responses[Math.floor(Math.random() * responses.length)];
  
  // Replace with actual API call:
  /*
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ message }),
  });
  
  const data = await response.json();
  return data.response;
  */
};