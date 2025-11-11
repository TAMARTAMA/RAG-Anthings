// import React, { useState } from 'react';
// import WelcomeScreen from './components/WelcomeScreen';
// import ChatSidebar from './components/ChatSidebar';
// import ChatInterface from './components/ChatInterface';
// import { useChats } from './hooks/useChats';

// function App() {
//   const [showWelcome, setShowWelcome] = useState(true);
//   const {
//     chats,
//     activeChat,
//     isLoading,
//     createNewChat,
//     sendMessage,
//     selectChat,
//     deleteChat,
//     rateMessage,
//   } = useChats();

//   const handleStartChat = () => {
//     setShowWelcome(false);
//     createNewChat();
//   };

//   if (showWelcome) {
//     return <WelcomeScreen onStartChat={handleStartChat} />;
//   }

//   return (
//     <div className="h-screen bg-gray-50 flex" dir="rtl">
//       <ChatSidebar
//         chats={chats}
//         activeChat={activeChat}
//         onNewChat={createNewChat}
//         onSelectChat={selectChat}
//         onDeleteChat={deleteChat}
//       />

//       <ChatInterface
//         activeChat={activeChat}
//         isLoading={isLoading}
//         onSendMessage={sendMessage}
//         onRateMessage={rateMessage}
//       />
//     </div>
//   );
// }

// export default App;

// src/App.tsx
import { useEffect, useState } from "react";
import Login from "./components/Login";
import { getIndexes, addIndex, removeIndex } from "./services/api";

export default function App() {
  // טוקן כמחרוזת (ריקה כשאין)
  const [token, setToken] = useState<string>(localStorage.getItem("token") ?? "");
  const [userId, setUserId] = useState<string>(localStorage.getItem("userId") ?? "");
  const [indexes, setIndexes] = useState<string[]>([]);
  const [newIndex, setNewIndex] = useState<string>("");

  // אחרי שיש טוקן—טען רשימת אינדקסים
  useEffect(() => {
    if (!token) return;
    getIndexes(token)
      .then(setIndexes)
      .catch(() => setIndexes(["wikipedia"]));
  }, [token]);

  // callback מה-Login
  function onAuth(t: string, uid: string, ix: string[]) {
    localStorage.setItem("token", t);
    localStorage.setItem("userId", uid);
    setToken(t);
    setUserId(uid);
    setIndexes(ix);
  }


  async function onAddIndex() {
  const name = newIndex.trim();
  if (!name) return;

  const resp = await addIndex(token, userId, name);
  setIndexes(resp.user.indexs);
  setNewIndex("");
}

  async function onRemoveIndex(ix: string) {
    const resp = await removeIndex(token, ix, userId);
    setIndexes(resp.user.indexs);
  }

  function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("userId");
    setToken("");
    setUserId("");
    setIndexes([]);
  }

  // אם אין טוקן—מציגים Login
  if (!token || !userId) {
    return <Login onAuth={onAuth} />;
  }

  return (
    <div style={{ maxWidth: 720, margin: "0 auto", padding: 24 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 24 }}>
        <h1 style={{ fontSize: 22, fontWeight: 700 }}>Hello, {userId}</h1>
        <button onClick={logout} style={{ textDecoration: "underline", fontSize: 14 }}>
          Logout
        </button>
      </div>

      <section style={{ border: "1px solid #e5e7eb", borderRadius: 12, padding: 16, marginBottom: 24 }}>
        <h2 style={{ fontWeight: 600, marginBottom: 12 }}>Your Indexes</h2>

        {indexes.length === 0 ? (
          <div style={{ color: "#6b7280", fontSize: 14 }}>No indexes yet</div>
        ) : (
          <ul style={{ paddingLeft: 20 }}>
            {indexes.map((ix) => (
              <li key={ix} style={{ display: "flex", alignItems: "center", gap: 8, margin: "6px 0" }}>
                <span style={{ fontFamily: "monospace" }}>{ix}</span>
                {ix !== "wikipedia" && (
                  <button
                    onClick={() => onRemoveIndex(ix)}
                    style={{ fontSize: 12, border: "1px solid #e5e7eb", padding: "4px 8px", borderRadius: 6 }}
                  >
                    remove
                  </button>
                )}
              </li>
            ))}
          </ul>
        )}

        <div style={{ display: "flex", gap: 8, marginTop: 12 }}>
          <input
            placeholder="new index name"
            value={newIndex}
            onChange={(e) => setNewIndex(e.target.value)}
            style={{ flex: 1, border: "1px solid #e5e7eb", borderRadius: 8, padding: "8px 10px" }}
          />
          <button
            onClick={onAddIndex}
            style={{ background: "#16a34a", color: "white", borderRadius: 8, padding: "8px 12px" }}
          >
            Add
          </button>
        </div>
      </section>

      {/* כאן בהמשך נשתול Dropdown לבחירת אינדקס לצ'אט/חיפוש */}
    </div>
  );
}
