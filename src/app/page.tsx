'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Sidebar } from '@/components/chat/Sidebar';
import { ChatHeader } from '@/components/chat/ChatHeader';
import { MessageBubble } from '@/components/chat/MessageBubble';
import { Composer } from '@/components/chat/Composer';
import { SettingsModal } from '@/components/modals/SettingsModal';
import { ShareModal } from '@/components/modals/ShareModal';
import { ProfileModal } from '@/components/modals/ProfileModal';
import { UpgradeModal } from '@/components/modals/UpgradeModal';
import { AuthModal } from '@/components/modals/AuthModal';
import { useMeenaStore } from '@/stores/meenaStore';
import { authService } from '@/lib/auth';
import { Message } from '@/types';
import { Sparkles, Compass, HeartHandshake, BookOpen, ShieldAlert } from 'lucide-react';

export default function Home() {
  const {
    conversations,
    activeConversationId,
    messages,
    addMessage,
    updateLastMessage,
    activeModal,
    setActiveModal,
    preferences,
    isTemporaryMode,
    temporaryMessages,
    addTemporaryMessage,
    updateLastTemporaryMessage,
    currentUser,
    setCurrentUser
  } = useMeenaStore();

  const [isGenerating, setIsGenerating] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check auth session on startup
  useEffect(() => {
    const session = authService.getSession();
    if (session.user) {
      setCurrentUser(session.user);
    } else {
      // Prompt sign in for first-time visitors as requested
      setActiveModal('auth');
    }
  }, []);

  // Display temporary messages when in temporary mode; otherwise display active conversation messages
  const activeMessages = isTemporaryMode
    ? temporaryMessages
    : (activeConversationId ? (messages[activeConversationId] || []) : []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [activeMessages]);

  const handleSendMessage = async (text: string, attachments: File[]) => {
    if (isGenerating) return;

    // 1. Construct user message
    const userMessage: Message = {
      id: `msg-${Date.now()}`,
      role: 'user',
      content: text,
      createdAt: new Date().toISOString(),
    };

    if (isTemporaryMode) {
      addTemporaryMessage(userMessage);
    } else if (activeConversationId) {
      addMessage(activeConversationId, userMessage);
    }

    // 2. Add assistant placeholder for token streaming
    const assistantMessageId = `msg-reply-${Date.now()}`;
    const assistantPlaceholder: Message = {
      id: assistantMessageId,
      role: 'assistant',
      content: '',
      createdAt: new Date().toISOString(),
      isStreaming: true,
    };

    if (isTemporaryMode) {
      addTemporaryMessage(assistantPlaceholder);
    } else if (activeConversationId) {
      addMessage(activeConversationId, assistantPlaceholder);
    }

    setIsGenerating(true);

    // 3. Initiate SSE Streaming Request with user details & context
    try {
      abortControllerRef.current = new AbortController();
      const currentStreamHistory = isTemporaryMode
        ? [...temporaryMessages, userMessage]
        : [...(activeConversationId ? (messages[activeConversationId] || []) : []), userMessage];

      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: currentStreamHistory,
          model: preferences.intelligenceMode === 'detailed' ? 'gemini-2.5-pro' : 'gemini-2.0-flash',
          customInstructions: preferences.customInstructions,
          userName: currentUser?.name || 'Friend',
          isTemporary: isTemporaryMode
        }),
        signal: abortControllerRef.current.signal,
      });

      if (!res.ok) {
        throw new Error('Failed to generate response');
      }

      const reader = res.body?.getReader();
      const decoder = new TextDecoder();
      let accumulatedText = '';

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const dataStr = line.replace('data: ', '').trim();
              if (dataStr === '[DONE]') {
                break;
              }
              try {
                const parsed = JSON.parse(dataStr);
                if (parsed.text) {
                  accumulatedText += parsed.text;
                  if (isTemporaryMode) {
                    updateLastTemporaryMessage(accumulatedText, true);
                  } else if (activeConversationId) {
                    updateLastMessage(activeConversationId, accumulatedText, true);
                  }
                }
              } catch (e) {
                // Ignore partial JSON chunks
              }
            }
          }
        }
      }

      // Mark generation as finished
      if (isTemporaryMode) {
        updateLastTemporaryMessage(accumulatedText, false);
      } else if (activeConversationId) {
        updateLastMessage(activeConversationId, accumulatedText, false);
      }
    } catch (err: any) {
      if (err.name === 'AbortError') {
        console.log('Generation stopped by user');
      } else {
        const fallbackErr = "I encountered a brief disruption connecting to my reasoning engine. Please try sending your message again.";
        if (isTemporaryMode) {
          updateLastTemporaryMessage(fallbackErr, false);
        } else if (activeConversationId) {
          updateLastMessage(activeConversationId, fallbackErr, false);
        }
      }
    } finally {
      setIsGenerating(false);
      abortControllerRef.current = null;
    }
  };

  const handleStopGenerating = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsGenerating(false);
    }
  };

  const handleRegenerate = () => {
    if (activeMessages.length < 2) return;
    const lastUserMsg = [...activeMessages].reverse().find(m => m.role === 'user');
    if (lastUserMsg) {
      handleSendMessage(lastUserMsg.content, []);
    }
  };

  const firstName = currentUser?.name ? currentUser.name.split(' ')[0] : 'there';

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#FAF7F2] dark:bg-[#161214] text-[#2A2325] dark:text-[#F5ECEF]">
      {/* Collapsible Left Navigation Sidebar */}
      <Sidebar />

      {/* Main Conversation Workspace */}
      <main className="flex-1 flex flex-col h-full min-w-0 relative">
        {/* Top Header */}
        <ChatHeader />

        {/* Temporary Mode Warning Banner - Only shown when active */}
        {isTemporaryMode && (
          <div className="px-4 py-2 bg-purple-50 dark:bg-purple-950/40 border-b border-purple-200 dark:border-purple-800 text-xs text-purple-800 dark:text-purple-200 flex items-center justify-center gap-2 font-medium animate-in fade-in duration-150">
            <ShieldAlert className="w-4 h-4 text-purple-600 dark:text-purple-400" />
            <span>Temporary Chat Active — Messages in this session will disappear completely once you exit temporary mode.</span>
          </div>
        )}

        {/* Conversation Message Canvas */}
        <div className="flex-1 overflow-y-auto px-4 py-6">
          <div className="max-w-3xl mx-auto">
            {activeMessages.length === 0 ? (
              /* Simple, friendly, human welcome screen with dynamic name */
              <div className="h-[60vh] flex flex-col items-center justify-center text-center space-y-4 px-4 select-none animate-in fade-in duration-300">
                <div className="w-12 h-12 rounded-2xl bg-accent-100 dark:bg-accent-500/20 text-accent-500 flex items-center justify-center shadow-sm font-bold text-xl">
                  M
                </div>
                <div className="space-y-1">
                  <h2 className="text-xl font-semibold text-text-primary-light dark:text-text-primary-dark">
                    {isTemporaryMode
                      ? `Temporary Chat Session`
                      : `Hey ${firstName}! What would you like to talk about today?`}
                  </h2>
                  <p className="text-xs text-text-muted-light dark:text-text-muted-dark max-w-sm">
                    {isTemporaryMode
                      ? "Ask questions or explore ideas with zero persistence or memory tracking."
                      : "Ask questions, practice languages, explore code, or share what's on your mind."}
                  </p>
                </div>

                {/* Quick Prompts */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 w-full max-w-md pt-4 text-xs">
                  <button
                    onClick={() => handleSendMessage("Hey! What are some great foreign language practice strategies?", [])}
                    className="p-3 bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] hover:border-accent-400 rounded-xl text-left transition shadow-sm space-y-1"
                  >
                    <BookOpen className="w-4 h-4 text-accent-500" />
                    <p className="font-medium">Language Practice</p>
                    <p className="text-[10px] text-text-muted-light">Practice conversational French, Spanish, or Hindi.</p>
                  </button>

                  <button
                    onClick={() => handleSendMessage("I need help reframing a challenging conversation at work.", [])}
                    className="p-3 bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] hover:border-accent-400 rounded-xl text-left transition shadow-sm space-y-1"
                  >
                    <HeartHandshake className="w-4 h-4 text-accent-500" />
                    <p className="font-medium">Mindful Reframing</p>
                    <p className="text-[10px] text-text-muted-light">Navigate difficult interpersonal situations.</p>
                  </button>

                  <button
                    onClick={() => handleSendMessage("What is Python and why is it so widely used in AI?", [])}
                    className="p-3 bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] hover:border-accent-400 rounded-xl text-left transition shadow-sm space-y-1"
                  >
                    <Compass className="w-4 h-4 text-accent-500" />
                    <p className="font-medium">Technical Learning</p>
                    <p className="text-[10px] text-text-muted-light">Explore programming, algorithms, and machine learning.</p>
                  </button>
                </div>
              </div>
            ) : (
              activeMessages.map((msg) => (
                <MessageBubble
                  key={msg.id}
                  message={msg}
                  onRegenerate={msg.role === 'assistant' ? handleRegenerate : undefined}
                />
              ))
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Fixed Message Composer */}
        <Composer
          onSendMessage={handleSendMessage}
          isGenerating={isGenerating}
          onStopGenerating={handleStopGenerating}
        />
      </main>

      {/* Modals & Dialogs */}
      <AuthModal
        isOpen={activeModal === 'auth'}
        onSuccess={(user) => {
          setCurrentUser(user);
          setActiveModal(null);
        }}
        onClose={() => {
          if (currentUser) setActiveModal(null);
        }}
      />
      <SettingsModal
        isOpen={activeModal === 'settings'}
        onClose={() => setActiveModal(null)}
      />
      <ShareModal
        isOpen={activeModal === 'share'}
        onClose={() => setActiveModal(null)}
      />
      <ProfileModal
        isOpen={activeModal === 'profile'}
        onClose={() => setActiveModal(null)}
      />
      <UpgradeModal
        isOpen={activeModal === 'upgrade'}
        onClose={() => setActiveModal(null)}
      />
    </div>
  );
}
