import React, { useState } from "react";
import { login, signup } from "../services/api";

type Props = {
  open: boolean;
  onClose: () => void;
  onSuccess: (token: string, userId: string) => void;
};

export default function LoginModal({ open, onClose, onSuccess }: Props) {
  const [mode, setMode] = useState<"login" | "signup">("login");
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState("");
  const [loading, setLoading] = useState(false);

  if (!open) return null;

  async function submit() {
    setErr("");
    if (!userId.trim() || !password.trim()) {
      setErr("Please fill username and password");
      return;
    }
    setLoading(true);
    try {
      const resp = mode === "login"
        ? await login(userId.trim(), password)
        : await signup(userId.trim(), password);

      localStorage.setItem("token", resp.access_token);
      localStorage.setItem("userId", resp.user.id);

      onSuccess(resp.access_token, resp.user.id);
    } catch (e: any) {
      setErr(e?.message || "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 bg-black/40 flex items-center justify-center">
      <div className="bg-white w-full max-w-md rounded-2xl p-4 shadow-xl">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-lg font-bold">
            {mode === "login" ? "Login" : "Sign up"}
          </h2>
          <button onClick={onClose} className="text-sm hover:underline">Close</button>
        </div>

        <div className="flex gap-2 mb-4">
          <button
            className={`px-3 py-1 rounded-xl border ${mode === "login" ? "bg-gray-100" : ""}`}
            onClick={() => setMode("login")}
          >
            Login
          </button>
          <button
            className={`px-3 py-1 rounded-xl border ${mode === "signup" ? "bg-gray-100" : ""}`}
            onClick={() => setMode("signup")}
          >
            Sign up
          </button>
        </div>

        <div className="space-y-3">
          <div>
            <label className="text-sm">Username</label>
            <input
              className="w-full border rounded-xl px-3 py-2"
              value={userId}
              onChange={(e) => setUserId(e.target.value)}
              placeholder="username"
            />
          </div>
          <div>
            <label className="text-sm">Password</label>
            <input
              type="password"
              className="w-full border rounded-xl px-3 py-2"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="password"
            />
          </div>
          {err && <div className="text-red-600 text-sm">{err}</div>}

          <button
            onClick={submit}
            disabled={loading}
            className="w-full rounded-xl bg-blue-600 text-white py-2 hover:bg-blue-700 disabled:opacity-60"
          >
            {loading ? "Loading..." : mode === "login" ? "Login" : "Create account"}
          </button>
        </div>
      </div>
    </div>
  );
}
