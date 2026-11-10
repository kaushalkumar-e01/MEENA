'use client';

import React, { useState } from 'react';
import {
  MessageSquare,
  Plus,
  Search,
  Pin,
  Archive,
  Trash2,
  Share2,
  Edit3,
  MoreVertical,
  PanelLeftClose,
  PanelLeft,
  User,
  Settings as SettingsIcon,
  LogOut,
  Sparkles,
  Users,
  ShieldCheck
} from 'lucide-react';
import { useMeenaStore } from '@/stores/meenaStore';
import { authService } from '@/lib/auth';

export function Sidebar() {
  const {
    isSidebarOpen,
    toggleSidebar,
    conversations,
    activeConversationId,
    setActiveConversationId,
    createNewConversation,
    pinConversation,
    archiveConversation,
    deleteConversation,
    renameConversation,
    searchQuery,
    setSearchQuery,
    setActiveModal,
    currentUser,
    logoutUser,
    setCurrentUser
  } = useMeenaStore();

  const [activeMenuId, setActiveMenuId] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [renameText, setRenameText] = useState('');
  const [isAccountMenuOpen, setIsAccountMenuOpen] = useState(false);
  const [isSwitchingAccount, setIsSwitchingAccount] = useState(false);

  const session = authService.getSession();
  const accounts = session.accounts || [];

  const filteredConversations = conversations.filter(c =>
    !c.isArchived && c.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const pinnedConversations = filteredConversations.filter(c => c.isPinned);
  const recentConversations = filteredConversations.filter(c => !c.isPinned);

  const handleStartRename = (id: string, currentTitle: string) => {
    setEditingId(id);
    setRenameText(currentTitle);
    setActiveMenuId(null);
  };

  const handleSaveRename = (id: string) => {
    if (renameText.trim()) {
      renameConversation(id, renameText.trim());
    }
    setEditingId(null);
  };

  const handleSwitchAccount = (email: string) => {
    const switched = authService.switchAccount(email);
    if (switched) {
      setCurrentUser(switched);
      setIsAccountMenuOpen(false);
      setIsSwitchingAccount(false);
    }
  };

  const initials = currentUser?.name
    ? currentUser.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    : 'M';

  return (
    <>
      {/* Mobile Backdrop */}
      {isSidebarOpen && (
        <div
          onClick={toggleSidebar}
          className="fixed inset-0 bg-black/20 backdrop-blur-sm z-30 md:hidden transition-opacity"
        />
      )}

      {/* Main Sidebar Container */}
      <aside className={`
        fixed md:static inset-y-0 left-0 z-40
        ${isSidebarOpen ? 'w-[280px]' : 'w-0 md:w-[64px]'}
        transition-all duration-200 ease-in-out
        bg-[#F2ECE6] dark:bg-[#292226] border-r border-[#E7DFD7] dark:border-[#382F34]
        flex flex-col h-full select-none overflow-hidden
      `}>
        {/* Header Section */}
        <div className="p-3.5 flex items-center justify-between border-b border-[#E7DFD7]/60 dark:border-[#382F34]/60">
          {isSidebarOpen ? (
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-xl bg-accent-100 dark:bg-accent-500/20 flex items-center justify-center text-accent-500 font-bold text-sm tracking-wide shadow-sm">
                M
              </div>
              <div className="flex flex-col">
                <span className="font-semibold text-sm tracking-tight text-text-primary-light dark:text-text-primary-dark">
                  MEENA
                </span>
                <span className="text-[10px] text-text-muted-light dark:text-text-muted-dark uppercase tracking-wider font-medium">
                  AI Companion
                </span>
              </div>
            </div>
          ) : (
            <button
              onClick={toggleSidebar}
              className="w-10 h-10 rounded-xl bg-accent-100 dark:bg-accent-500/20 flex items-center justify-center text-accent-500 font-bold text-base mx-auto hover:opacity-85 transition"
              title="Expand Sidebar"
            >
              M
            </button>
          )}

          {isSidebarOpen && (
            <button
              onClick={toggleSidebar}
              className="p-1.5 rounded-lg text-text-muted-light dark:text-text-muted-dark hover:bg-black/5 dark:hover:bg-white/5 transition"
              title="Collapse Sidebar"
            >
              <PanelLeftClose className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Action Buttons */}
        <div className="p-3 space-y-2">
          <button
            onClick={() => createNewConversation()}
            className={`
              w-full flex items-center justify-center gap-2 py-2.5 px-3
              bg-accent-500 hover:bg-accent-600 text-white
              font-medium text-xs rounded-xl shadow-sm transition-all duration-150
              ${!isSidebarOpen && 'md:p-2 md:rounded-lg'}
            `}
            title="Start New Conversation"
          >
            <Plus className="w-4 h-4" />
            {isSidebarOpen && <span>New Conversation</span>}
          </button>

          {isSidebarOpen && (
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-text-muted-light dark:text-text-muted-dark" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search conversations..."
                className="w-full bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] rounded-xl pl-8 pr-3 py-1.5 text-xs text-text-primary-light dark:text-text-primary-dark placeholder:text-text-muted-light dark:placeholder:text-text-muted-dark focus:outline-none focus:ring-1 focus:ring-accent-400"
              />
            </div>
          )}
        </div>

        {/* Scrollable Conversation List */}
        <div className="flex-1 overflow-y-auto px-2 space-y-4 py-1">
          {/* Pinned Section */}
          {pinnedConversations.length > 0 && isSidebarOpen && (
            <div>
              <div className="flex items-center gap-1.5 px-3 pb-1.5 text-[11px] font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wider">
                <Pin className="w-3 h-3 text-accent-500 rotate-45" />
                <span>Pinned</span>
              </div>
              <div className="space-y-0.5">
                {pinnedConversations.map((conv) => (
                  <ConversationItem
                    key={conv.id}
                    conv={conv}
                    isActive={activeConversationId === conv.id}
                    editingId={editingId}
                    renameText={renameText}
                    setRenameText={setRenameText}
                    handleSaveRename={handleSaveRename}
                    handleStartRename={handleStartRename}
                    activeMenuId={activeMenuId}
                    setActiveMenuId={setActiveMenuId}
                    setActiveConversationId={setActiveConversationId}
                    pinConversation={pinConversation}
                    archiveConversation={archiveConversation}
                    deleteConversation={deleteConversation}
                    setActiveModal={setActiveModal}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Recent Chats Section */}
          {isSidebarOpen && (
            <div>
              <div className="px-3 pb-1.5 text-[11px] font-semibold text-text-muted-light dark:text-text-muted-dark uppercase tracking-wider">
                Recent Chats
              </div>
              <div className="space-y-0.5">
                {recentConversations.map((conv) => (
                  <ConversationItem
                    key={conv.id}
                    conv={conv}
                    isActive={activeConversationId === conv.id}
                    editingId={editingId}
                    renameText={renameText}
                    setRenameText={setRenameText}
                    handleSaveRename={handleSaveRename}
                    handleStartRename={handleStartRename}
                    activeMenuId={activeMenuId}
                    setActiveMenuId={setActiveMenuId}
                    setActiveConversationId={setActiveConversationId}
                    pinConversation={pinConversation}
                    archiveConversation={archiveConversation}
                    deleteConversation={deleteConversation}
                    setActiveModal={setActiveModal}
                  />
                ))}
                {recentConversations.length === 0 && (
                  <div className="px-3 py-4 text-center text-xs text-text-muted-light dark:text-text-muted-dark italic">
                    No conversations yet
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* User Footer Profile & Account Menu */}
        <div className="p-2 border-t border-[#E7DFD7]/80 dark:border-[#382F34]/80 relative">
          <button
            onClick={() => setIsAccountMenuOpen(!isAccountMenuOpen)}
            className={`
              w-full flex items-center gap-2.5 p-2 rounded-xl
              hover:bg-white/80 dark:hover:bg-[#1F191C]/80 transition text-left
              ${!isSidebarOpen && 'justify-center p-1.5'}
            `}
          >
            <div className="w-8 h-8 rounded-full bg-accent-100 dark:bg-accent-500/20 text-accent-500 font-semibold flex items-center justify-center text-xs ring-1 ring-accent-200 dark:ring-accent-400/30">
              {initials}
            </div>
            {isSidebarOpen && (
              <div className="flex-1 min-w-0">
                <p className="text-xs font-medium text-text-primary-light dark:text-text-primary-dark truncate">
                  {currentUser?.name || 'Guest User'}
                </p>
                <p className="text-[10px] text-text-muted-light dark:text-text-muted-dark truncate capitalize">
                  {currentUser?.plan ? `${currentUser.plan} Plan` : 'Sign in'}
                </p>
              </div>
            )}
          </button>

          {/* Account Popup Menu */}
          {isAccountMenuOpen && (
            <div className="absolute bottom-14 left-2 right-2 bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] rounded-2xl shadow-xl p-1.5 z-50 text-xs space-y-0.5 animate-in fade-in zoom-in-95 duration-150">
              <button
                onClick={() => { setActiveModal('profile'); setIsAccountMenuOpen(false); }}
                className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-text-primary-light dark:text-text-primary-dark hover:bg-black/5 dark:hover:bg-white/5 transition"
              >
                <User className="w-4 h-4 text-text-muted-light dark:text-text-muted-dark" />
                <span>My Profile</span>
              </button>

              <button
                onClick={() => { setActiveModal('settings'); setIsAccountMenuOpen(false); }}
                className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-text-primary-light dark:text-text-primary-dark hover:bg-black/5 dark:hover:bg-white/5 transition"
              >
                <SettingsIcon className="w-4 h-4 text-text-muted-light dark:text-text-muted-dark" />
                <span>Settings</span>
              </button>

              <button
                onClick={() => { setActiveModal('upgrade'); setIsAccountMenuOpen(false); }}
                className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-accent-600 dark:text-accent-400 font-medium hover:bg-accent-50 dark:hover:bg-accent-500/10 transition"
              >
                <Sparkles className="w-4 h-4" />
                <span>Upgrade Plan</span>
              </button>

              {/* Multi-Account Switching Section */}
              <div className="border-t border-[#E7DFD7]/60 dark:border-[#382F34]/60 my-1" />

              <button
                onClick={() => setIsSwitchingAccount(!isSwitchingAccount)}
                className="w-full flex items-center justify-between px-3 py-2 rounded-lg text-text-primary-light dark:text-text-primary-dark hover:bg-black/5 transition"
              >
                <span className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-text-muted-light" />
                  <span>Switch Account</span>
                </span>
                <span className="text-[10px] text-text-muted-light">({accounts.length})</span>
              </button>

              {isSwitchingAccount && (
                <div className="pl-6 pr-2 py-1 space-y-1 bg-[#FAF7F2] dark:bg-[#161214] rounded-lg">
                  {accounts.map(acc => (
                    <button
                      key={acc.email}
                      onClick={() => handleSwitchAccount(acc.email)}
                      className={`w-full text-left py-1 text-[11px] truncate block ${acc.email === currentUser?.email ? 'font-semibold text-accent-600' : 'text-text-secondary-light hover:underline'}`}
                    >
                      {acc.name} ({acc.email})
                    </button>
                  ))}
                  <button
                    onClick={() => { setActiveModal('auth'); setIsAccountMenuOpen(false); }}
                    className="text-[11px] text-accent-500 font-medium hover:underline block pt-1"
                  >
                    + Add Account
                  </button>
                </div>
              )}

              <div className="border-t border-[#E7DFD7]/60 dark:border-[#382F34]/60 my-1" />

              {/* Real Working Logout */}
              <button
                onClick={() => {
                  logoutUser();
                  setIsAccountMenuOpen(false);
                }}
                className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20 transition font-medium"
              >
                <LogOut className="w-4 h-4" />
                <span>Log Out</span>
              </button>
            </div>
          )}
        </div>
      </aside>
    </>
  );
}

function ConversationItem({
  conv,
  isActive,
  editingId,
  renameText,
  setRenameText,
  handleSaveRename,
  handleStartRename,
  activeMenuId,
  setActiveMenuId,
  setActiveConversationId,
  pinConversation,
  archiveConversation,
  deleteConversation,
  setActiveModal
}: any) {
  return (
    <div className="relative group">
      {editingId === conv.id ? (
        <div className="px-2 py-1">
          <input
            type="text"
            value={renameText}
            onChange={(e) => setRenameText(e.target.value)}
            onBlur={() => handleSaveRename(conv.id)}
            onKeyDown={(e) => e.key === 'Enter' && handleSaveRename(conv.id)}
            autoFocus
            className="w-full bg-white dark:bg-[#1F191C] border border-accent-400 rounded-lg px-2 py-1 text-xs text-text-primary-light dark:text-text-primary-dark outline-none"
          />
        </div>
      ) : (
        <div
          onClick={() => setActiveConversationId(conv.id)}
          className={`
            w-full flex items-center justify-between px-3 py-2 rounded-xl text-xs cursor-pointer transition
            ${isActive
              ? 'bg-white dark:bg-[#1F191C] text-accent-600 dark:text-accent-400 font-medium shadow-sm border border-[#E7DFD7]/60 dark:border-[#382F34]/60'
              : 'text-text-secondary-light dark:text-text-secondary-dark hover:bg-white/50 dark:hover:bg-white/5'}
          `}
        >
          <span className="truncate pr-2">{conv.title}</span>

          <button
            onClick={(e) => {
              e.stopPropagation();
              setActiveMenuId(activeMenuId === conv.id ? null : conv.id);
            }}
            className="opacity-0 group-hover:opacity-100 p-1 hover:bg-black/5 dark:hover:bg-white/10 rounded-md transition"
          >
            <MoreVertical className="w-3.5 h-3.5 text-text-muted-light dark:text-text-muted-dark" />
          </button>
        </div>
      )}

      {/* Context Action Menu */}
      {activeMenuId === conv.id && (
        <div
          onClick={(e) => e.stopPropagation()}
          className="absolute right-2 top-8 w-36 bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] rounded-xl shadow-lg p-1 z-30 space-y-0.5 text-xs"
        >
          <button
            onClick={() => { setActiveModal('share'); setActiveMenuId(null); }}
            className="w-full flex items-center gap-2 px-2.5 py-1.5 rounded-lg hover:bg-black/5 dark:hover:bg-white/5 text-text-primary-light dark:text-text-primary-dark"
          >
            <Share2 className="w-3.5 h-3.5" />
            <span>Share</span>
          </button>
          <button
            onClick={() => handleStartRename(conv.id, conv.title)}
            className="w-full flex items-center gap-2 px-2.5 py-1.5 rounded-lg hover:bg-black/5 dark:hover:bg-white/5 text-text-primary-light dark:text-text-primary-dark"
          >
            <Edit3 className="w-3.5 h-3.5" />
            <span>Rename</span>
          </button>
          <button
            onClick={() => { pinConversation(conv.id); setActiveMenuId(null); }}
            className="w-full flex items-center gap-2 px-2.5 py-1.5 rounded-lg hover:bg-black/5 dark:hover:bg-white/5 text-text-primary-light dark:text-text-primary-dark"
          >
            <Pin className="w-3.5 h-3.5" />
            <span>{conv.isPinned ? 'Unpin' : 'Pin'}</span>
          </button>
          <button
            onClick={() => { archiveConversation(conv.id); setActiveMenuId(null); }}
            className="w-full flex items-center gap-2 px-2.5 py-1.5 rounded-lg hover:bg-black/5 dark:hover:bg-white/5 text-text-primary-light dark:text-text-primary-dark"
          >
            <Archive className="w-3.5 h-3.5" />
            <span>Archive</span>
          </button>
          <div className="border-t border-[#E7DFD7]/60 dark:border-[#382F34]/60 my-0.5" />
          <button
            onClick={() => { deleteConversation(conv.id); setActiveMenuId(null); }}
            className="w-full flex items-center gap-2 px-2.5 py-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-950/20 text-red-600 dark:text-red-400"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Delete</span>
          </button>
        </div>
      )}
    </div>
  );
}
