import { create } from 'zustand';
import { Conversation, Message, AccentColor, UserPreferences } from '@/types';
import { authService, UserProfile } from '@/lib/auth';

export const ACCENT_PALETTES: Record<AccentColor, Record<string, string>> = {
  rose: {
    '--accent-50': '#FDF3F5',
    '--accent-100': '#F9E4E8',
    '--accent-200': '#F4CAD2',
    '--accent-300': '#ECA8B7',
    '--accent-400': '#DF7B93',
    '--accent-500': '#D15E78',
    '--accent-600': '#B94761',
  },
  lavender: {
    '--accent-50': '#F5F3FC',
    '--accent-100': '#ECE8F9',
    '--accent-200': '#D5CCF2',
    '--accent-300': '#A89BD6',
    '--accent-400': '#8B72C8',
    '--accent-500': '#7059B5',
    '--accent-600': '#5A45A0',
  },
  blue: {
    '--accent-50': '#EFF6FF',
    '--accent-100': '#DBEAFE',
    '--accent-200': '#BFDBFE',
    '--accent-300': '#93C5FD',
    '--accent-400': '#60A5FA',
    '--accent-500': '#3B82F6',
    '--accent-600': '#2563EB',
  },
  green: {
    '--accent-50': '#F0FDF4',
    '--accent-100': '#DCFCE7',
    '--accent-200': '#BBF7D0',
    '--accent-300': '#86EFAC',
    '--accent-400': '#4ADE80',
    '--accent-500': '#22C55E',
    '--accent-600': '#16A34A',
  },
  peach: {
    '--accent-50': '#FFF7ED',
    '--accent-100': '#FFEDD5',
    '--accent-200': '#FED7AA',
    '--accent-300': '#FDB77A',
    '--accent-400': '#FB923C',
    '--accent-500': '#F97316',
    '--accent-600': '#EA6C0A',
  },
  grey: {
    '--accent-50': '#F9FAFB',
    '--accent-100': '#F3F4F6',
    '--accent-200': '#E5E7EB',
    '--accent-300': '#9CA3AF',
    '--accent-400': '#6B7280',
    '--accent-500': '#4B5563',
    '--accent-600': '#374151',
  },
};

interface MeenaStore {
  // Navigation & UI
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  activeModal: string | null;
  setActiveModal: (modal: string | null) => void;

  // Authentication
  currentUser: UserProfile | null;
  setCurrentUser: (user: UserProfile | null) => void;
  logoutUser: () => void;

  // Conversations
  conversations: Conversation[];
  activeConversationId: string | null;
  setActiveConversationId: (id: string | null) => void;
  messages: Record<string, Message[]>;
  addMessage: (conversationId: string, message: Message) => void;
  updateLastMessage: (conversationId: string, content: string, isStreaming?: boolean) => void;
  createNewConversation: () => string;
  pinConversation: (id: string) => void;
  archiveConversation: (id: string) => void;
  deleteConversation: (id: string) => void;
  renameConversation: (id: string, newTitle: string) => void;

  // Temporary Chat
  isTemporaryMode: boolean;
  temporaryMessages: Message[];
  addTemporaryMessage: (msg: Message) => void;
  updateLastTemporaryMessage: (content: string, isStreaming?: boolean) => void;
  toggleTemporaryMode: (enable: boolean) => void;

  // Search & Filtering
  searchQuery: string;
  setSearchQuery: (query: string) => void;

  // Preferences
  preferences: UserPreferences;
  setPreference: <K extends keyof UserPreferences>(key: K, value: UserPreferences[K]) => void;
}

export const useMeenaStore = create<MeenaStore>((set, get) => ({
  isSidebarOpen: true,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  setSidebarOpen: (open) => set({ isSidebarOpen: open }),
  activeModal: null,
  setActiveModal: (modal) => set({ activeModal: modal }),

  // User State
  currentUser: null,
  setCurrentUser: (user) => set({ currentUser: user }),
  logoutUser: () => {
    authService.logout();
    set({
      currentUser: null,
      isTemporaryMode: false,
      temporaryMessages: [],
      activeModal: 'auth'
    });
  },

  conversations: [
    {
      id: 'conv-1',
      title: 'Mindful Morning Reflections',
      isPinned: true,
      isArchived: false,
      updatedAt: new Date().toISOString(),
    },
    {
      id: 'conv-2',
      title: 'Foreign Language Practice: French',
      isPinned: false,
      isArchived: false,
      updatedAt: new Date(Date.now() - 3600000).toISOString(),
    },
    {
      id: 'conv-3',
      title: 'Evolved Transformer Architecture Notes',
      isPinned: false,
      isArchived: false,
      updatedAt: new Date(Date.now() - 86400000).toISOString(),
    }
  ],
  activeConversationId: 'conv-1',
  setActiveConversationId: (id) => set({ activeConversationId: id }),

  messages: {
    'conv-1': [
      {
        id: 'msg-1',
        role: 'user',
        content: 'Hi MEENA, I want to take a pause and reflect on today before diving into work.',
        createdAt: new Date(Date.now() - 120000).toISOString(),
      },
      {
        id: 'msg-2',
        role: 'assistant',
        content: "Good morning! I'm glad you're choosing to begin your day with quiet intention. How are you feeling in this moment—both in your mind and body?",
        createdAt: new Date(Date.now() - 60000).toISOString(),
      }
    ]
  },

  addMessage: (conversationId, message) => set((state) => ({
    messages: {
      ...state.messages,
      [conversationId]: [...(state.messages[conversationId] || []), message]
    }
  })),

  updateLastMessage: (conversationId, content, isStreaming = false) => set((state) => {
    const chatMsgs = state.messages[conversationId] || [];
    if (chatMsgs.length === 0) return state;
    const last = { ...chatMsgs[chatMsgs.length - 1], content, isStreaming };
    return {
      messages: {
        ...state.messages,
        [conversationId]: [...chatMsgs.slice(0, -1), last]
      }
    };
  }),

  createNewConversation: () => {
    const id = `conv-${Date.now()}`;
    const newConv: Conversation = {
      id,
      title: 'New Conversation',
      isPinned: false,
      isArchived: false,
      isTemporary: false,
      updatedAt: new Date().toISOString(),
    };

    set((state) => ({
      conversations: [newConv, ...state.conversations],
      activeConversationId: id,
      messages: {
        ...state.messages,
        [id]: []
      }
    }));
    return id;
  },

  pinConversation: (id) => set((state) => ({
    conversations: state.conversations.map((c) => c.id === id ? { ...c, isPinned: !c.isPinned } : c)
  })),

  archiveConversation: (id) => set((state) => ({
    conversations: state.conversations.map((c) => c.id === id ? { ...c, isArchived: !c.isArchived } : c)
  })),

  deleteConversation: (id) => set((state) => ({
    conversations: state.conversations.filter((c) => c.id !== id),
    activeConversationId: state.activeConversationId === id ? (state.conversations.find(c => c.id !== id)?.id || null) : state.activeConversationId
  })),

  renameConversation: (id, newTitle) => set((state) => ({
    conversations: state.conversations.map((c) => c.id === id ? { ...c, title: newTitle } : c)
  })),

  // Temporary Chat implementation with clean state separation
  isTemporaryMode: false,
  temporaryMessages: [],

  addTemporaryMessage: (msg) => set((state) => ({
    temporaryMessages: [...state.temporaryMessages, msg]
  })),

  updateLastTemporaryMessage: (content, isStreaming = false) => set((state) => {
    if (state.temporaryMessages.length === 0) return state;
    const last = { ...state.temporaryMessages[state.temporaryMessages.length - 1], content, isStreaming };
    return {
      temporaryMessages: [...state.temporaryMessages.slice(0, -1), last]
    };
  }),

  toggleTemporaryMode: (enable: boolean) => set((state) => {
    if (enable) {
      // Enter Temporary mode: start fresh with clean welcome banner
      return {
        isTemporaryMode: true,
        temporaryMessages: []
      };
    } else {
      // Exit Temporary mode: Completely wipe ephemeral messages and restore normal chat
      return {
        isTemporaryMode: false,
        temporaryMessages: []
      };
    }
  }),

  searchQuery: '',
  setSearchQuery: (query) => set({ searchQuery: query }),

  preferences: {
    theme: 'light',
    accentColor: 'rose',
    fontSize: 'default',
    fontFamily: 'plus-jakarta',
    intelligenceMode: 'balanced',
    responseStyle: 'warm',
    warmthLevel: 2,
    enableMemory: true,
    customInstructions: '',
    webSearchEnabled: false,
    librarySearchEnabled: false,
    voiceLanguage: 'en-US',
    speechSpeed: 1.0,
  },

  setPreference: (key, value) => {
    set((state) => {
      const nextPref = { ...state.preferences, [key]: value };

      if (typeof window !== 'undefined') {
        if (key === 'theme') {
          const isDark = value === 'dark' || (value === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
          if (isDark) {
            document.documentElement.classList.add('dark');
          } else {
            document.documentElement.classList.remove('dark');
          }
        }

        if (key === 'accentColor') {
          const palette = ACCENT_PALETTES[value as AccentColor];
          if (palette) {
            Object.entries(palette).forEach(([varName, hex]) => {
              document.documentElement.style.setProperty(varName, hex);
            });
          }
        }
      }

      return { preferences: nextPref };
    });
  }
}));
