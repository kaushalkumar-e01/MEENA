'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Bot, MessageSquare, ArrowLeft, Shield } from 'lucide-react';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function SharedConversationPage() {
  const params = useParams();
  const shareId = params?.shareId as string;
  const [data, setData] = useState<{ title: string; messages: any[]; createdAt: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!shareId) return;
    fetch(`/api/share?id=${shareId}`)
      .then(async (res) => {
        const json = await res.json();
        if (!res.ok) throw new Error(json.error || 'Failed to load conversation');
        setData(json);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [shareId]);

  return (
    <div className="min-h-screen bg-[#FAF7F2] dark:bg-[#161214] text-[#2A2325] dark:text-[#F5ECEF] flex flex-col">
      {/* Top Bar */}
      <header className="h-14 px-6 border-b border-[#E7DFD7] dark:border-[#382F34] bg-white/70 dark:bg-[#1F191C]/70 backdrop-blur-md flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link href="/" className="flex items-center gap-2 text-xs font-medium text-text-secondary-light hover:text-accent-500 transition">
            <ArrowLeft className="w-4 h-4" />
            <span>Open MEENA</span>
          </Link>
          <div className="h-4 w-px bg-[#E7DFD7] dark:bg-[#382F34]" />
          <h1 className="font-semibold text-sm truncate max-w-md">
            {data?.title || 'Shared Conversation'}
          </h1>
        </div>
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-accent-50 dark:bg-accent-500/10 text-accent-600 dark:text-accent-400 text-[11px] font-medium">
          <Shield className="w-3.5 h-3.5" />
          <span>Read-Only Snapshot</span>
        </div>
      </header>

      {/* Main Conversation Stream */}
      <main className="flex-1 max-w-3xl w-full mx-auto px-4 py-8">
        {loading ? (
          <div className="py-20 text-center text-xs text-text-muted-light animate-pulse">
            Loading shared conversation...
          </div>
        ) : error ? (
          <div className="py-20 text-center space-y-3">
            <p className="text-base font-semibold text-text-primary-light dark:text-text-primary-dark">
              Conversation Unavailable
            </p>
            <p className="text-xs text-text-muted-light max-w-sm mx-auto">{error}</p>
            <Link href="/" className="inline-block mt-4 px-4 py-2 bg-accent-500 text-white rounded-xl text-xs font-medium hover:bg-accent-600">
              Go to MEENA Home
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            {data?.messages?.map((msg) => {
              const isUser = msg.role === 'user';
              return (
                <div key={msg.id} className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
                  <div className={`flex gap-3 max-w-[85%] ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
                    {!isUser && (
                      <div className="w-7 h-7 rounded-full bg-accent-100 dark:bg-accent-500/20 text-accent-500 flex items-center justify-center shrink-0 mt-0.5 text-xs font-semibold shadow-sm">
                        M
                      </div>
                    )}
                    <div className={`
                      px-4 py-3 rounded-2xl text-[14.5px] leading-relaxed shadow-sm
                      ${isUser
                        ? 'bg-[#F9E4E8] dark:bg-[#2D1F24] border border-[#F4CAD2] dark:border-[#4A303A] text-text-primary-light dark:text-text-primary-dark rounded-br-sm'
                        : 'bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] text-text-primary-light dark:text-text-primary-dark rounded-tl-sm'}
                    `}>
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>
                        {msg.content}
                      </ReactMarkdown>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </main>
    </div>
  );
}
