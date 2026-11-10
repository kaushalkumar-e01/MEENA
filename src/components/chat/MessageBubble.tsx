'use client';

import React, { useState } from 'react';
import {
  Copy,
  Check,
  RotateCcw,
  Volume2,
  ThumbsUp,
  ThumbsDown,
  Edit3
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Message } from '@/types';

interface MessageBubbleProps {
  message: Message;
  onRegenerate?: () => void;
  onEdit?: (newContent: string) => void;
}

export function MessageBubble({ message, onRegenerate, onEdit }: MessageBubbleProps) {
  const isUser = message.role === 'user';
  const [copied, setCopied] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [feedback, setFeedback] = useState<'up' | 'down' | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(message.content);

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleReadAloud = () => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      if (isSpeaking) {
        window.speechSynthesis.cancel();
        setIsSpeaking(false);
      } else {
        const utterance = new SpeechSynthesisUtterance(message.content);
        utterance.onend = () => setIsSpeaking(false);
        setIsSpeaking(true);
        window.speechSynthesis.speak(utterance);
      }
    }
  };

  const handleSaveEdit = () => {
    if (onEdit && editText.trim()) {
      onEdit(editText.trim());
    }
    setIsEditing(false);
  };

  return (
    <div className={`w-full flex ${isUser ? 'justify-end' : 'justify-start'} mb-6 group`}>
      <div className={`flex gap-3 max-w-[85%] md:max-w-[78%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
        {/* Assistant Avatar Badge */}
        {!isUser && (
          <div className="w-7 h-7 rounded-full bg-accent-100 dark:bg-accent-500/20 text-accent-500 flex items-center justify-center shrink-0 mt-0.5 ring-1 ring-accent-200 dark:ring-accent-400/30 text-xs font-semibold shadow-sm">
            M
          </div>
        )}

        <div className="flex flex-col space-y-1.5 min-w-0">
          {/* Main Bubble Card */}
          <div className={`
            px-4 py-3 rounded-2xl text-[14.5px] leading-relaxed transition-all shadow-sm
            ${isUser
              ? 'bg-[#F9E4E8] dark:bg-[#2D1F24] border border-[#F4CAD2] dark:border-[#4A303A] text-text-primary-light dark:text-text-primary-dark rounded-br-sm'
              : 'bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] text-text-primary-light dark:text-text-primary-dark rounded-tl-sm'}
          `}>
            {isEditing ? (
              <div className="space-y-2 min-w-[260px]">
                <textarea
                  value={editText}
                  onChange={(e) => setEditText(e.target.value)}
                  className="w-full bg-transparent border border-accent-300 rounded-lg p-2 text-xs outline-none focus:ring-1 focus:ring-accent-400"
                  rows={3}
                />
                <div className="flex justify-end gap-1.5">
                  <button
                    onClick={() => setIsEditing(false)}
                    className="px-2 py-1 text-xs text-text-muted-light dark:text-text-muted-dark hover:underline"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSaveEdit}
                    className="px-2.5 py-1 text-xs bg-accent-500 text-white rounded-lg hover:bg-accent-600 transition"
                  >
                    Save & Regenerate
                  </button>
                </div>
              </div>
            ) : (
              <div className="prose prose-sm dark:prose-invert max-w-none break-words">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    p: ({ children }) => <p className="mb-2.5 last:mb-0 leading-relaxed">{children}</p>,
                    ul: ({ children }) => <ul className="list-disc pl-5 my-2 space-y-1">{children}</ul>,
                    ol: ({ children }) => <ol className="list-decimal pl-5 my-2 space-y-1">{children}</ol>,
                    code: ({ inline, className, children, ...props }: any) => {
                      return inline ? (
                        <code className="bg-black/5 dark:bg-white/10 px-1 py-0.5 rounded text-xs font-mono text-accent-600 dark:text-accent-400" {...props}>
                          {children}
                        </code>
                      ) : (
                        <pre className="bg-[#1A1218] text-slate-100 p-3 rounded-xl overflow-x-auto my-2 text-xs font-mono border border-[#382F34]">
                          <code>{children}</code>
                        </pre>
                      );
                    }
                  }}
                >
                  {message.content}
                </ReactMarkdown>
                {message.isStreaming && (
                  <span className="inline-block w-1.5 h-4 ml-1 bg-accent-400 streaming-cursor align-middle" />
                )}
              </div>
            )}
          </div>

          {/* Action Row */}
          {!message.isStreaming && (
            <div className={`
              flex items-center gap-1 text-text-muted-light dark:text-text-muted-dark
              opacity-0 group-hover:opacity-100 transition-opacity duration-150
              ${isUser ? 'justify-end' : 'justify-start'}
            `}>
              {/* Copy */}
              <button
                onClick={handleCopy}
                className="p-1 rounded-md hover:bg-black/5 dark:hover:bg-white/5 transition"
                title="Copy content"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-green-600" /> : <Copy className="w-3.5 h-3.5" />}
              </button>

              {/* User Edit */}
              {isUser && onEdit && (
                <button
                  onClick={() => setIsEditing(true)}
                  className="p-1 rounded-md hover:bg-black/5 dark:hover:bg-white/5 transition"
                  title="Edit prompt"
                >
                  <Edit3 className="w-3.5 h-3.5" />
                </button>
              )}

              {/* Assistant Read Aloud */}
              {!isUser && (
                <>
                  <button
                    onClick={handleReadAloud}
                    className={`p-1 rounded-md hover:bg-black/5 dark:hover:bg-white/5 transition ${isSpeaking ? 'text-accent-500' : ''}`}
                    title="Read aloud"
                  >
                    <Volume2 className="w-3.5 h-3.5" />
                  </button>

                  {/* Regenerate */}
                  {onRegenerate && (
                    <button
                      onClick={onRegenerate}
                      className="p-1 rounded-md hover:bg-black/5 dark:hover:bg-white/5 transition"
                      title="Regenerate response"
                    >
                      <RotateCcw className="w-3.5 h-3.5" />
                    </button>
                  )}

                  {/* Feedback Thumbs */}
                  <button
                    onClick={() => setFeedback(feedback === 'up' ? null : 'up')}
                    className={`p-1 rounded-md hover:bg-black/5 dark:hover:bg-white/5 transition ${feedback === 'up' ? 'text-accent-500' : ''}`}
                    title="Helpful response"
                  >
                    <ThumbsUp className="w-3.5 h-3.5" />
                  </button>

                  <button
                    onClick={() => setFeedback(feedback === 'down' ? null : 'down')}
                    className={`p-1 rounded-md hover:bg-black/5 dark:hover:bg-white/5 transition ${feedback === 'down' ? 'text-red-500' : ''}`}
                    title="Needs improvement"
                  >
                    <ThumbsDown className="w-3.5 h-3.5" />
                  </button>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
