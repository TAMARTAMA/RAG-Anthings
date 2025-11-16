import React, { useEffect, useMemo, useState } from "react";
import WelcomeScreen from "./components/WelcomeScreen";
import ChatSidebar from "./components/ChatSidebar";
import ChatInterface from "./components/ChatInterface";
import useChats from "./hooks/useChats";
import HeaderBar from "./components/HeaderBar";
import LoginModal from "./components/LoginModal";
import IndexesDrawer from "./components/IndexesDrawer";
import IndexSelect from "./components/IndexSelect";

/** Simple localStorage helpers */
function getStored(key: string) {
  try { return localStorage.getItem(key); } catch { return null; }
}
function setStored(key: string, val: string | null) {
  try { val == null ? localStorage.removeItem(key) : localStorage.setItem(key, val); } catch {}
}

export default function App() {
  // Always start with the Welcome screen
  const [showWelcome, setShowWelcome] = useState(true);

  // Auth state
  const [token, setToken] = useState<string | null>(() => getStored("token"));
  const [userId, setUserId] = useState<string | null>(() => getStored("userId"));


  // Overlays
  const [showLogin, setShowLogin] = useState(false);
  const [showIndexes, setShowIndexes] = useState(false);

  // Active index (persisted)
  const [activeIndex, setActiveIndex] = useState<string>(() => getStored("activeIndex") || "wikipedia");
  useEffect(() => setStored("activeIndex", activeIndex), [activeIndex]);
  const [indexesVersion, setIndexesVersion] = useState(0);
  const notifyIndexesChanged = () => setIndexesVersion(v => v + 1);

  // Chat logic
  const {
  chats,
  activeChat,
  isLoading,
  createNewChat,
  sendMessage,
  selectChat,
  deleteChat,
  rateMessage,
  clearChats
} = useChats(userId, token);

  // Persist auth
  useEffect(() => setStored("token", token), [token]);
  useEffect(() => setStored("userId", userId), [userId]);

  const isAuthed = useMemo(() => !!token && !!userId, [token, userId]);

  const handleStartChat = () => {
    if (showWelcome) setShowWelcome(false);
    createNewChat();
  };

  // Login success: get token + userId from modal
  const handleLoginSuccess = (t: string, uid: string) => {
    setToken(t);
    setUserId(uid);
    setShowLogin(false);
    if (showWelcome) {
      setShowWelcome(false);
      createNewChat();
    }
  };

  const handleLogout = () => {
    setToken(null);
    setUserId(null);
    setShowWelcome(true);
      // clean localStorage
  setStored("token", null);
  setStored("userId", null);
  setStored("activeIndex", null);
  clearChats();


  };

  /** Wrap sendMessage to include the active index in the payload */
  const sendWithIndex = (message: string) => {
    // If your hook supports options, this forwards the selected index.
    // Adjust the key name ("index") to match your backend if needed.
    return (sendMessage as any)(message,  activeIndex );
  };

  return (
    <div className="h-screen flex flex-col bg-white" dir="ltr">
      <HeaderBar
        isAuthed={isAuthed}
        onLoginClick={() => setShowLogin(true)}
        onLogoutClick={handleLogout}
        onIndexesClick={() => setShowIndexes(true)}
        rightExtra={
          isAuthed ? (
            <IndexSelect
              token={token}
              value={activeIndex}
              onChange={setActiveIndex}
              reloadKey={indexesVersion}   // <-- triggers re-fetch
            />
          ) : null
        }
      />

      {showWelcome ? (
        <div className="flex-1">
          <WelcomeScreen onStartChat={handleStartChat} />
        </div>
      ) : (
        <div className="flex flex-1">
          <ChatSidebar
            chats={chats}
            activeChat={activeChat}
            onNewChat={createNewChat}
            onSelectChat={selectChat}
            onDeleteChat={deleteChat}
          />
          <ChatInterface
            activeChat={activeChat}
            isLoading={isLoading}
            onSendMessage={sendWithIndex}   // <-- send with the active index
            onRateMessage={rateMessage}
          />
        </div>
      )}

      <LoginModal
        open={showLogin}
        onClose={() => setShowLogin(false)}
        onSuccess={handleLoginSuccess} // (token, userId)
      />

      {/* Show Indexes only if user is authenticated */}
      {isAuthed && (
        <IndexesDrawer
          open={showIndexes}
          onClose={() => setShowIndexes(false)}
          token={token}
          userId={userId}
          onIndexesChanged={notifyIndexesChanged}  // <-- notify App on changes
        />
      )}
    </div>
  );
}
