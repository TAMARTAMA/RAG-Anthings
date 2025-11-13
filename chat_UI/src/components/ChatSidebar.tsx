// import React from 'react';
// import { Plus, MessageCircle, Trash2, Bot } from 'lucide-react';
// import { Chat } from '../types/chat';

// interface ChatSidebarProps {
//   chats: Chat[];
//   activeChat: Chat | null;
//   onNewChat: () => void;
//   onSelectChat: (chat: Chat) => void;
//   onDeleteChat: (chatId: string) => void;
// }

// const ChatSidebar: React.FC<ChatSidebarProps> = ({
//   chats,
//   activeChat,
//   onNewChat,
//   onSelectChat,
//   onDeleteChat,
// }) => {

//  const formatDate = (dateStr: string) => {
//   if (!dateStr) return "unknown";
//   const date = new Date(dateStr);
  
//   if (isNaN(date.getTime())) return "unknown";
//   const now = new Date();
//   const diff = now.getTime() - date.getTime();
//   const days = Math.floor(diff / (1000 * 60 * 60 * 24));
//   if (days === 0) return 'today';
//   if (days === 1) return 'yesterday';
//   if (days < 7) return `${days} days`;
//   return date.toLocaleDateString('he-IL');
// };
//   return (
//     <div className="w-80 bg-white border-r border-gray-200 flex flex-col h-full">
//       {/* Header */}
//       <div className="p-6 border-b border-gray-200">
//         <div className="flex items-center gap-3 mb-4">
//           <Bot className="w-8 h-8 text-blue-600" />
//           <h1 className="text-2xl font-bold text-gray-900">
//             BOT<span className="text-blue-600">NET</span>
//           </h1>
//         </div>

//         <button
//           onClick={onNewChat}
//           className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-xl font-medium flex items-center justify-center gap-2 transition-colors duration-200"
//         >
//           <Plus className="w-5 h-5" />
//           New conversation
//         </button>
//       </div>

//       {/* Chat List */}
//       <div className="flex-1 overflow-y-auto">
//         {chats.length === 0 ? (
//           <div className="p-6 text-center text-gray-500">
//             <MessageCircle className="w-12 h-12 mx-auto mb-3 text-gray-300" />
//             <p>No calls yet</p>
//             <p className="text-sm mt-1">Click New Conversation to start</p>
//           </div>
//         ) : (
//           <div className="p-4 space-y-2">
//             {chats.map((chat) => (
//               <div
//                 key={chat.id}
//                 onClick={() => onSelectChat(chat)}
//                 className={`group p-4 rounded-xl cursor-pointer transition-all duration-200 ${
//                   activeChat?.id === chat.id
//                     ? 'bg-blue-50 border border-blue-200 shadow-sm'
//                     : 'hover:bg-gray-50 border border-transparent'
//                 }`}
//               >
//                 <div className="flex items-start justify-between">
//                   <div className="flex-1 min-w-0">
//                     <h3 className="font-medium text-gray-900 truncate text-right">
//                       {chat.title}
//                     </h3>
//                     <p className="text-sm text-gray-500 mt-1 text-right">
//                       {formatDate(chat.updatedAt)}
//                     </p>
//                     {chat.messages.length > 0 && (
//                       <p className="text-xs text-gray-400 mt-2 line-clamp-2 text-right">
//                         {chat.messages[chat.messages.length - 1].content}
//                       </p>
//                     )}
//                   </div>

//                   <button
//                     onClick={(e) => {
//                       e.stopPropagation();
//                       onDeleteChat(chat.id);
//                     }}
//                     className="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-500 transition-all duration-200 p-1"
//                   >
//                     <Trash2 className="w-4 h-4" />
//                   </button>
//                 </div>
//               </div>
//             ))}
//           </div>
//         )}
//       </div>
//     </div>
//   );
// };

// export default ChatSidebar;
import React from 'react';
import { Plus, MessageCircle, Trash2, Bot, Sparkles } from 'lucide-react';
import { Chat } from '../types/chat';

interface ChatSidebarProps {
  chats: Chat[];
  activeChat: Chat | null;
  onNewChat: () => void;
  onSelectChat: (chat: Chat) => void;
  onDeleteChat: (chatId: string) => void;
}

const ChatSidebar: React.FC<ChatSidebarProps> = ({
  chats,
  activeChat,
  onNewChat,
  onSelectChat,
  onDeleteChat,
}) => {
  const formatDate = (dateStr: string) => {
    if (!dateStr) return 'unknown';
    const date = new Date(dateStr);

    if (isNaN(date.getTime())) return 'unknown';
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    if (days === 0) return 'today';
    if (days === 1) return 'yesterday';
    if (days < 7) return `${days} days`;
    return date.toLocaleDateString('he-IL');
  };
  
  return (
    <div className="w-80 bg-white border-r border-gray-200 flex flex-col h-full">
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center gap-3 mb-4">
          <div className="relative">
            <Bot className="w-8 h-8 text-blue-600 animate-bounce" />
            <Sparkles className="w-4 h-4 text-blue-400 absolute -top-2 -right-2 animate-ping" />
          </div>
          <h1 className="text-2xl font-bold text-gray-900">
            RAG<span className="text-blue-600"> Anything</span>
          </h1>
        </div>

        <button
          onClick={onNewChat}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-xl font-medium flex items-center justify-center gap-2 transition-colors duration-200"
        >
          <Plus className="w-5 h-5" />
          New conversation
        </button>
      </div>

      {/* Chat List */}
      <div className="flex-1 overflow-y-auto">
        {chats.length === 0 ? (
          <div className="p-6 text-center text-gray-500">
            <MessageCircle className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p>No calls yet</p>
            <p className="text-sm mt-1">Click New Conversation to start</p>
          </div>
        ) : (
          <div className="p-4 space-y-2">
            {chats.map((chat) => (
              <div
                key={chat.id}
                onClick={() => onSelectChat(chat)}
                className={`group p-4 rounded-xl cursor-pointer transition-all duration-200 ${
                  activeChat?.id === chat.id
                    ? 'bg-blue-50 border border-blue-200 shadow-sm'
                    : 'hover:bg-gray-50 border border-transparent'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-gray-900 truncate text-right">
                      {chat.title}
                    </h3>
                    <p className="text-sm text-gray-500 mt-1 text-right">
                      {formatDate(chat.updatedAt)}
                    </p>
                    {chat.messages.length > 0 && (
                      <p className="text-xs text-gray-400 mt-2 line-clamp-2 text-right">
                        {chat.messages[chat.messages.length - 1].content}
                      </p>
                    )}
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteChat(chat.id);
                    }}
                    className="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-500 transition-all duration-200 p-1"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatSidebar;
