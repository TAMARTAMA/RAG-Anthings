import React from 'react';
import { Bot } from 'lucide-react';

type Props = {
  isAuthed: boolean;
  onLoginClick: () => void;
  onLogoutClick: () => void;
  onIndexesClick: () => void;
  rightExtra?: React.ReactNode;
};

export default function HeaderBar({
  isAuthed,
  onLoginClick,
  onLogoutClick,
  onIndexesClick,
  rightExtra,
}: Props) {
  return (
    <header className="w-full border-b bg-white">
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-end gap-3">
        {/* Right side: buttons + project name */}
        <div className="flex items-center gap-3">
          {isAuthed && rightExtra}

          {isAuthed && (
            <button
              className="px-3 py-1 rounded-xl border hover:bg-gray-50"
              onClick={onIndexesClick}
            >
              Indexes
            </button>
          )}

          {!isAuthed ? (
            <button
              className="px-3 py-1 rounded-xl bg-blue-600 text-white hover:bg-blue-700"
              onClick={onLoginClick}
            >
              Login / Sign up
            </button>
          ) : (
            <button
              className="px-3 py-1 rounded-xl bg-gray-200 hover:bg-gray-300"
              onClick={onLogoutClick}
            >
              Logout
            </button>
          )}

          {/* Project name on the right side */}
          <div className="flex items-center gap-2 select-none">
            <span className="text-xl font-bold text-gray-900">
              RAG<span className="text-blue-600"> Anything</span>
            </span>
          </div>
        </div>
      </div>
    </header>
  );
}
