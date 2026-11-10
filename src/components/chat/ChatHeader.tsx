'use client';

import React, { useState } from 'react';
import {
  EyeOff,
  Share2,
  Edit2,
  Check,
  X,
  PanelLeft,
  Sun,
  Moon,
  Sparkles
} from 'lucide-react';
import { useMeenaStore } from '@/stores/meenaStore';

export function ChatHeader() {
  const {
    conversations,
    activeConversationId,
    renameConversation,
    isSidebarOpen,
    toggleSidebar,
    isTemporaryMode,
    toggleTemporaryMode,
    setActiveModal,
    preferences,
    setPreference
  } = useMeenaStore();

  const activeConv = conversations.find(c => c.id === activeConversationId);
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const [titleText, setTitleText] = useState(activeConv?.title || '');

  const handleSaveTitle = () => {
    if (activeConversationId && titleText.trim()) {
      renameConversation(activeConversationId, titleText.trim());
    }
    setIsEditingTitle(false);
  };

  const toggleTheme = () => {
    const nextTheme = preferences.theme === 'dark' ? 'light' : 'dark';
    setPreference('theme', nextTheme);
  };

  return (
    <header className="h-14 px-4 border-b border-[#E7DFD7] dark:border-[#382F34] bg-white/70 dark:bg-[#1F191C]/70 backdrop-blur-md flex items-center justify-between shrink-0 select-none z-10">
      {/* Left Title and Controls */}
      <div className="flex items-center gap-3 min-w-0">
        {!isSidebarOpen && (
          <button
            onClick={toggleSidebar}
            className="p-1.5 rounded-lg hover:bg-black/5 dark:hover:bg-white/5 text-text-muted-light dark:text-text-muted-dark transition"
            title="Expand Sidebar"
          >
            <PanelLeft className="w-4 h-4" />
          </button>
        )}

        {isTemporaryMode ? (
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-purple-500 animate-pulse" />
            <span className="font-semibold text-xs text-purple-700 dark:text-purple-300">
              Temporary Chat (Ephemeral Session)
            </span>
          </div>
        ) : isEditingTitle ? (
          <div className="flex items-center gap-1.5">
            <input
              type="text"
              value={titleText}
              onChange={(e) => setTitleText(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSaveTitle()}
              autoFocus
              className="bg-white dark:bg-[#161214] border border-accent-400 rounded-lg px-2 py-0.5 text-xs text-text-primary-light dark:text-text-primary-dark outline-none"
            />
            <button onClick={handleSaveTitle} className="text-accent-500 hover:opacity-80 p-0.5">
              <Check className="w-3.5 h-3.5" />
            </button>
            <button onClick={() => setIsEditingTitle(false)} className="text-text-muted-light dark:text-text-muted-dark hover:opacity-80 p-0.5">
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-2 min-w-0 group">
            <h1 className="font-semibold text-sm text-text-primary-light dark:text-text-primary-dark truncate">
              {activeConv?.title || 'New Conversation'}
            </h1>
            <button
              onClick={() => { setTitleText(activeConv?.title || ''); setIsEditingTitle(true); }}
              className="opacity-0 group-hover:opacity-100 text-text-muted-light dark:text-text-muted-dark hover:text-accent-500 transition p-0.5"
              title="Edit title"
            >
              <Edit2 className="w-3 h-3" />
            </button>
          </div>
        )}
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-2">
        {/* Temporary Mode Button - Toggles in and out cleanly */}
        <button
          onClick={() => toggleTemporaryMode(!isTemporaryMode)}
          className={`
            flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition
            ${isTemporaryMode
              ? 'bg-purple-100 dark:bg-purple-950/40 text-purple-700 dark:text-purple-300 ring-1 ring-purple-300 dark:ring-purple-700 shadow-sm'
              : 'hover:bg-black/5 dark:hover:bg-white/5 text-text-secondary-light dark:text-text-secondary-dark'}
          `}
          title={isTemporaryMode ? "Exit Temporary Chat (Wipes ephemeral messages)" : "Start Temporary Incognito Chat"}
        >
          <EyeOff className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">
            {isTemporaryMode ? 'Exit Temporary' : 'Temporary'}
          </span>
        </button>

        {/* Share Button (disabled in temporary mode) */}
        {!isTemporaryMode && (
          <button
            onClick={() => setActiveModal('share')}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium bg-white dark:bg-[#292226] border border-[#E7DFD7] dark:border-[#382F34] text-text-secondary-light dark:text-text-secondary-dark hover:bg-black/5 dark:hover:bg-white/5 transition shadow-sm"
          >
            <Share2 className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Share</span>
          </button>
        )}

        {/* Light/Dark Theme Switcher */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded-xl text-text-secondary-light dark:text-text-secondary-dark hover:bg-black/5 dark:hover:bg-white/5 transition"
          title="Toggle Light/Dark Theme"
        >
          {preferences.theme === 'dark' ? (
            <Sun className="w-4 h-4 text-amber-400" />
          ) : (
            <Moon className="w-4 h-4 text-slate-600" />
          )}
        </button>
      </div>
    </header>
  );
}
