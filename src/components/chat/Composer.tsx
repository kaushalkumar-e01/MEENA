'use client';

import React, { useState, useRef, useEffect } from 'react';
import {
  Plus,
  ArrowUp,
  Square,
  Mic,
  MicOff,
  Image,
  FileText,
  Camera,
  X,
  Paperclip
} from 'lucide-react';

interface ComposerProps {
  onSendMessage: (text: string, attachments: File[]) => void;
  isGenerating: boolean;
  onStopGenerating: () => void;
}

export function Composer({ onSendMessage, isGenerating, onStopGenerating }: ComposerProps) {
  const [text, setText] = useState('');
  const [attachments, setAttachments] = useState<File[]>([]);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingSeconds, setRecordingSeconds] = useState(0);

  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [text]);

  // Voice recording timer
  useEffect(() => {
    let timer: any;
    if (isRecording) {
      timer = setInterval(() => setRecordingSeconds(s => s + 1), 1000);
    } else {
      setRecordingSeconds(0);
    }
    return () => clearInterval(timer);
  }, [isRecording]);

  const handleSend = () => {
    if ((!text.trim() && attachments.length === 0) || isGenerating) return;
    onSendMessage(text.trim(), attachments);
    setText('');
    setAttachments([]);
    if (textareaRef.current) {
      textareaRef.current.style.height = '52px';
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setAttachments(prev => [...prev, ...Array.from(e.target.files!)]);
      setIsMenuOpen(false);
    }
  };

  const removeAttachment = (index: number) => {
    setAttachments(prev => prev.filter((_, i) => i !== index));
  };

  // Web Speech API Voice Dictation
  const toggleRecording = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert("Speech recognition isn't supported in this browser. Please try Chrome or Edge.");
      return;
    }

    if (isRecording) {
      setIsRecording(false);
    } else {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = true;

      recognition.onstart = () => setIsRecording(true);
      recognition.onresult = (event: any) => {
        const transcript = Array.from(event.results)
          .map((r: any) => r[0].transcript)
          .join('');
        setText(prev => (prev ? prev + ' ' : '') + transcript);
      };
      recognition.onerror = () => setIsRecording(false);
      recognition.onend = () => setIsRecording(false);
      recognition.start();
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto px-4 pb-4 select-none">
      {/* Hidden inputs */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileSelect}
        className="hidden"
        multiple
      />
      <input
        type="file"
        ref={imageInputRef}
        onChange={handleFileSelect}
        accept="image/*"
        className="hidden"
        multiple
      />

      {/* Attachment Previews Strip */}
      {attachments.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-2 p-2 bg-white/60 dark:bg-[#1F191C]/60 rounded-xl border border-[#E7DFD7] dark:border-[#382F34]">
          {attachments.map((file, i) => (
            <div
              key={i}
              className="flex items-center gap-1.5 px-2.5 py-1 bg-white dark:bg-[#292226] border border-[#E7DFD7] dark:border-[#382F34] rounded-lg text-xs"
            >
              <Paperclip className="w-3.5 h-3.5 text-accent-500" />
              <span className="max-w-[120px] truncate text-text-primary-light dark:text-text-primary-dark">
                {file.name}
              </span>
              <button onClick={() => removeAttachment(i)} className="text-text-muted-light hover:text-red-500 ml-1">
                <X className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Main Composer Box */}
      <div className="relative bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] rounded-2xl shadow-sm focus-within:ring-2 focus-within:ring-accent-300/40 focus-within:border-accent-400 transition-all p-2 flex items-end gap-2">
        {/* Attachment Plus Button */}
        <div className="relative">
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="p-2 rounded-xl text-text-muted-light dark:text-text-muted-dark hover:bg-black/5 dark:hover:bg-white/5 hover:text-accent-500 transition"
            title="Attach file or image"
          >
            <Plus className="w-4 h-4" />
          </button>

          {/* Plus Menu Popover */}
          {isMenuOpen && (
            <div className="absolute bottom-12 left-0 w-44 bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] rounded-2xl shadow-xl p-1.5 z-50 text-xs space-y-0.5">
              <button
                onClick={() => imageInputRef.current?.click()}
                className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl hover:bg-black/5 dark:hover:bg-white/5 text-text-primary-light dark:text-text-primary-dark transition text-left"
              >
                <Image className="w-4 h-4 text-accent-500" />
                <span>Upload Image</span>
              </button>
              <button
                onClick={() => fileInputRef.current?.click()}
                className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl hover:bg-black/5 dark:hover:bg-white/5 text-text-primary-light dark:text-text-primary-dark transition text-left"
              >
                <FileText className="w-4 h-4 text-accent-500" />
                <span>Upload Document</span>
              </button>
            </div>
          )}
        </div>

        {/* Text Input */}
        <div className="flex-1 min-w-0">
          <textarea
            ref={textareaRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={isRecording ? `Listening... (${recordingSeconds}s)` : "Message MEENA..."}
            rows={1}
            className="w-full bg-transparent border-none outline-none resize-none py-1.5 text-[14.5px] leading-relaxed text-text-primary-light dark:text-text-primary-dark placeholder:text-text-muted-light dark:placeholder:text-text-muted-dark"
          />
        </div>

        {/* Voice Microphone Button */}
        <button
          onClick={toggleRecording}
          className={`
            p-2 rounded-xl transition
            ${isRecording
              ? 'bg-red-50 text-red-500 animate-pulse'
              : 'text-text-muted-light dark:text-text-muted-dark hover:bg-black/5 dark:hover:bg-white/5 hover:text-accent-500'}
          `}
          title={isRecording ? "Stop recording" : "Voice input"}
        >
          {isRecording ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
        </button>

        {/* Send / Stop Generating Button */}
        {isGenerating ? (
          <button
            onClick={onStopGenerating}
            className="w-8 h-8 rounded-xl bg-slate-800 dark:bg-slate-200 text-white dark:text-slate-900 flex items-center justify-center hover:opacity-90 transition shadow-sm"
            title="Stop generating"
          >
            <Square className="w-3.5 h-3.5 fill-current" />
          </button>
        ) : (
          <button
            onClick={handleSend}
            disabled={!text.trim() && attachments.length === 0}
            className={`
              w-8 h-8 rounded-xl flex items-center justify-center transition shadow-sm
              ${text.trim() || attachments.length > 0
                ? 'bg-accent-500 hover:bg-accent-600 text-white'
                : 'bg-black/5 dark:bg-white/5 text-text-muted-light dark:text-text-muted-dark cursor-not-allowed'}
            `}
            title="Send message"
          >
            <ArrowUp className="w-4 h-4" />
          </button>
        )}
      </div>

      <p className="text-[11px] text-center text-text-muted-light dark:text-text-muted-dark mt-2 tracking-wide">
        MEENA may produce thoughtful insights. Please verify important information.
      </p>
    </div>
  );
}
