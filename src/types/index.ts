export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  createdAt: string;
  isStreaming?: boolean;
}

export interface Conversation {
  id: string;
  title: string;
  isPinned: boolean;
  isArchived: boolean;
  isTemporary?: boolean;
  updatedAt: string;
}

export type AccentColor = 'rose' | 'lavender' | 'blue' | 'green' | 'peach' | 'grey';

export interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  accentColor: AccentColor;
  fontSize: 'small' | 'default' | 'large';
  fontFamily: 'plus-jakarta' | 'inter' | 'system';
  intelligenceMode: 'fast' | 'balanced' | 'detailed' | 'context-aware';
  responseStyle: string;
  warmthLevel: number;
  enableMemory: boolean;
  customInstructions: string;
  webSearchEnabled: boolean;
  librarySearchEnabled: boolean;
  voiceLanguage: string;
  speechSpeed: number;
}
