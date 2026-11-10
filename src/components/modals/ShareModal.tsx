'use client';

import React, { useState, useEffect } from 'react';
import {
  X,
  Copy,
  Check,
  Share2,
  Globe,
  ShieldCheck,
  MessageCircle,
  Mail,
  ExternalLink,
  Ban
} from 'lucide-react';
import { useMeenaStore } from '@/stores/meenaStore';

export function ShareModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const { conversations, activeConversationId, messages } = useMeenaStore();
  const activeConv = conversations.find(c => c.id === activeConversationId);
  const activeMsgs = activeConversationId ? (messages[activeConversationId] || []) : [];

  const [copied, setCopied] = useState(false);
  const [shareId, setShareId] = useState<string | null>(null);
  const [shareUrl, setShareUrl] = useState('');
  const [isRevoked, setIsRevoked] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen && activeConversationId) {
      setIsRevoked(false);
      setLoading(true);

      // Register public share snapshot in backend
      fetch('/api/share', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'create',
          conversationId: activeConversationId,
          title: activeConv?.title || 'Shared Conversation',
          messages: activeMsgs
        })
      })
        .then(res => res.json())
        .then(data => {
          if (data.shareId) {
            setShareId(data.shareId);
            const fullUrl = `${window.location.origin}/share/${data.shareId}`;
            setShareUrl(fullUrl);
          }
        })
        .catch(err => console.error(err))
        .finally(() => setLoading(false));
    }
  }, [isOpen, activeConversationId]);

  if (!isOpen) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(shareUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Web Share API for Mobile & Supported Browsers
  const handleNativeShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: `MEENA: ${activeConv?.title || 'Shared Conversation'}`,
          text: `Read this thoughtful conversation on MEENA:`,
          url: shareUrl
        });
      } catch (err) {
        // User cancelled share
      }
    } else {
      handleCopy();
    }
  };

  // WhatsApp Direct Link
  const handleWhatsAppShare = () => {
    const text = encodeURIComponent(`Read this conversation with MEENA: ${shareUrl}`);
    window.open(`https://api.whatsapp.com/send?text=${text}`, '_blank');
  };

  // Email Direct Link
  const handleEmailShare = () => {
    const subject = encodeURIComponent(`MEENA Conversation: ${activeConv?.title}`);
    const body = encodeURIComponent(`Hi,\n\nI wanted to share this conversation from MEENA with you:\n${shareUrl}\n\nWarmly`);
    window.open(`mailto:?subject=${subject}&body=${body}`, '_blank');
  };

  // Revoke Share Link
  const handleRevoke = async () => {
    if (!shareId) return;
    try {
      await fetch('/api/share', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'revoke', shareId })
      });
      setIsRevoked(true);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm select-none">
      <div className="w-full max-w-md bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] rounded-2xl shadow-2xl p-6 space-y-4 animate-in fade-in zoom-in-95 duration-200">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Share2 className="w-4 h-4 text-accent-500" />
            <h3 className="font-semibold text-sm text-text-primary-light dark:text-text-primary-dark">
              Share Conversation
            </h3>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-text-muted-light hover:bg-black/5 dark:hover:bg-white/5">
            <X className="w-4 h-4" />
          </button>
        </div>

        {isRevoked ? (
          <div className="p-4 bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900 rounded-xl text-xs space-y-2 text-amber-800 dark:text-amber-200">
            <div className="flex items-center gap-2 font-semibold">
              <Ban className="w-4 h-4" />
              <span>Public Link Revoked</span>
            </div>
            <p>Access to this shared conversation has been disabled. Nobody with the old link can view it anymore.</p>
          </div>
        ) : (
          <>
            <p className="text-xs text-text-muted-light dark:text-text-muted-dark leading-relaxed">
              Anyone with this link will view a clean, read-only snapshot of <strong className="text-text-primary-light dark:text-text-primary-dark font-medium">&quot;{activeConv?.title}&quot;</strong>. Your account credentials and private memories are never shared.
            </p>

            {/* Direct Social / App Buttons */}
            <div className="grid grid-cols-3 gap-2 text-xs">
              <button
                type="button"
                onClick={handleNativeShare}
                className="flex flex-col items-center justify-center gap-1.5 p-2.5 rounded-xl border border-[#E7DFD7] dark:border-[#382F34] hover:bg-black/5 dark:hover:bg-white/5 transition"
              >
                <Share2 className="w-4 h-4 text-accent-500" />
                <span className="text-[11px] font-medium">Native Share</span>
              </button>

              <button
                type="button"
                onClick={handleWhatsAppShare}
                className="flex flex-col items-center justify-center gap-1.5 p-2.5 rounded-xl border border-[#E7DFD7] dark:border-[#382F34] hover:bg-black/5 dark:hover:bg-white/5 transition"
              >
                <MessageCircle className="w-4 h-4 text-emerald-500" />
                <span className="text-[11px] font-medium">WhatsApp</span>
              </button>

              <button
                type="button"
                onClick={handleEmailShare}
                className="flex flex-col items-center justify-center gap-1.5 p-2.5 rounded-xl border border-[#E7DFD7] dark:border-[#382F34] hover:bg-black/5 dark:hover:bg-white/5 transition"
              >
                <Mail className="w-4 h-4 text-blue-500" />
                <span className="text-[11px] font-medium">Email</span>
              </button>
            </div>

            {/* Link input with copy */}
            <div className="flex items-center gap-2 p-1.5 bg-[#FAF7F2] dark:bg-[#161214] border border-[#E7DFD7] dark:border-[#382F34] rounded-xl">
              <input
                type="text"
                readOnly
                value={shareUrl}
                className="flex-1 bg-transparent px-2 text-xs text-text-secondary-light dark:text-text-secondary-dark outline-none select-all font-mono text-[11px]"
              />
              <button
                onClick={handleCopy}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-accent-500 hover:bg-accent-600 text-white rounded-lg text-xs font-medium transition"
              >
                {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                <span>{copied ? 'Copied' : 'Copy'}</span>
              </button>
            </div>

            {/* Revoke link button */}
            <div className="flex items-center justify-between pt-1 text-[11px] text-text-muted-light">
              <div className="flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5 text-accent-500" />
                <span>Read-only snapshot</span>
              </div>
              <button
                type="button"
                onClick={handleRevoke}
                className="text-red-500 hover:underline"
              >
                Revoke Link
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
