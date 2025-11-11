import { useState } from "react";
import { login, signup } from "../services/api";

export default function Login({ onAuth }: { onAuth: (token: string, userId: string, indexs: string[]) => void }) {
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [mode, setMode] = useState<"login" | "signup">("login");
  const [err, setErr] = useState("");

  async function submit() {
    setErr("");
    if (!userId.trim() || !password.trim()) { setErr("נא למלא שם משתמש וסיסמה"); return; }
    try {
      const resp = mode === "login" ? await login(userId.trim(), password) : await signup(userId.trim(), password);
      localStorage.setItem("token", resp.access_token);
      localStorage.setItem("userId", resp.user.id);
      onAuth(resp.access_token, resp.user.id, resp.user.indexs);
    } catch (e: any) {
      setErr(e.message || "Auth failed");
    }
  }

  return (
    <div className="max-w-sm mx-auto p-6 border rounded mt-10">
      <h2 className="text-xl font-bold mb-4">Welcome</h2>
      <label className="block text-sm mb-1">User ID</label>
      <input className="border rounded w-full p-2 mb-3" value={userId} onChange={e=>setUserId(e.target.value)} />
      <label className="block text-sm mb-1">Password</label>
      <input type="password" className="border rounded w-full p-2 mb-3" value={password} onChange={e=>setPassword(e.target.value)} />
      <div className="flex items-center gap-3 mb-3">
        <label><input type="radio" checked={mode==="login"} onChange={()=>setMode("login")} /> Login</label>
        <label><input type="radio" checked={mode==="signup"} onChange={()=>setMode("signup")} /> Signup</label>
      </div>
      {err && <div className="text-red-600 text-sm mb-2">{err}</div>}
      <button className="bg-blue-600 text-white px-4 py-2 rounded w-full" onClick={submit}>
        {mode === "login" ? "Login" : "Create account"}
      </button>
    </div>
  );
}
