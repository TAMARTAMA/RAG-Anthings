type Props = {
  isAuthed: boolean;
  onLoginClick: () => void;
  onLogoutClick: () => void;
  onIndexesClick: () => void;
  rightExtra?: React.ReactNode; // new prop for selector
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
      <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between gap-3">
        <div className="font-bold text-lg"></div>

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
        </div>
      </div>
    </header>
  );
}
