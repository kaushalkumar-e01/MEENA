'use client';

import React, { useState } from 'react';
import {
  X,
  Palette,
  Brain,
  Volume2,
  Globe,
  Shield,
  Database,
  Sparkles,
  Moon,
  Sun,
  Laptop
} from 'lucide-react';
import { useMeenaStore, ACCENT_PALETTES } from '@/stores/meenaStore';
import { AccentColor } from '@/types';

export function SettingsModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const { preferences, setPreference } = useMeenaStore();
  const [activeTab, setActiveTab] = useState<'appearance' | 'intelligence' | 'voice' | 'personalization' | 'privacy'>('appearance');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/30 backdrop-blur-sm select-none">
      <div className="w-full max-w-2xl bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] rounded-2xl shadow-2xl flex flex-col max-h-[85vh] overflow-hidden">
        {/* Header */}
        <div className="px-6 py-4 border-b border-[#E7DFD7] dark:border-[#382F34] flex items-center justify-between">
          <h2 className="text-base font-semibold text-text-primary-light dark:text-text-primary-dark">
            Application Settings
          </h2>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-text-muted-light dark:text-text-muted-dark hover:bg-black/5 dark:hover:bg-white/5 transition"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <div className="flex-1 flex overflow-hidden">
          {/* Navigation Tabs */}
          <div className="w-48 border-r border-[#E7DFD7] dark:border-[#382F34] p-2 space-y-1 bg-[#FAF7F2]/50 dark:bg-[#161214]/50">
            <button
              onClick={() => setActiveTab('appearance')}
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium transition ${activeTab === 'appearance' ? 'bg-accent-50 dark:bg-accent-500/20 text-accent-600 dark:text-accent-400' : 'text-text-secondary-light dark:text-text-secondary-dark hover:bg-black/5'}`}
            >
              <Palette className="w-4 h-4" />
              <span>Appearance</span>
            </button>
            <button
              onClick={() => setActiveTab('intelligence')}
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium transition ${activeTab === 'intelligence' ? 'bg-accent-50 dark:bg-accent-500/20 text-accent-600 dark:text-accent-400' : 'text-text-secondary-light dark:text-text-secondary-dark hover:bg-black/5'}`}
            >
              <Brain className="w-4 h-4" />
              <span>Intelligence</span>
            </button>
            <button
              onClick={() => setActiveTab('voice')}
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium transition ${activeTab === 'voice' ? 'bg-accent-50 dark:bg-accent-500/20 text-accent-600 dark:text-accent-400' : 'text-text-secondary-light dark:text-text-secondary-dark hover:bg-black/5'}`}
            >
              <Volume2 className="w-4 h-4" />
              <span>Voice & Audio</span>
            </button>
            <button
              onClick={() => setActiveTab('personalization')}
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium transition ${activeTab === 'personalization' ? 'bg-accent-50 dark:bg-accent-500/20 text-accent-600 dark:text-accent-400' : 'text-text-secondary-light dark:text-text-secondary-dark hover:bg-black/5'}`}
            >
              <Sparkles className="w-4 h-4" />
              <span>Personalization</span>
            </button>
            <button
              onClick={() => setActiveTab('privacy')}
              className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-medium transition ${activeTab === 'privacy' ? 'bg-accent-50 dark:bg-accent-500/20 text-accent-600 dark:text-accent-400' : 'text-text-secondary-light dark:text-text-secondary-dark hover:bg-black/5'}`}
            >
              <Shield className="w-4 h-4" />
              <span>Privacy & Data</span>
            </button>
          </div>

          {/* Details Pane */}
          <div className="flex-1 p-6 overflow-y-auto space-y-6 text-xs text-text-primary-light dark:text-text-primary-dark">
            {activeTab === 'appearance' && (
              <div className="space-y-6">
                {/* Theme Mode */}
                <div>
                  <h3 className="font-semibold text-sm mb-2">Theme Mode</h3>
                  <div className="grid grid-cols-3 gap-3">
                    {[
                      { id: 'light', label: 'Light', icon: Sun },
                      { id: 'dark', label: 'Dark', icon: Moon },
                      { id: 'system', label: 'System', icon: Laptop }
                    ].map(t => {
                      const Icon = t.icon;
                      const isSelected = preferences.theme === t.id;
                      return (
                        <button
                          key={t.id}
                          onClick={() => setPreference('theme', t.id as any)}
                          className={`flex flex-col items-center justify-center gap-2 p-3 rounded-xl border transition ${isSelected ? 'border-accent-500 bg-accent-50/50 dark:bg-accent-500/10 text-accent-600 dark:text-accent-400 font-medium' : 'border-[#E7DFD7] dark:border-[#382F34] hover:bg-black/5'}`}
                        >
                          <Icon className="w-5 h-5" />
                          <span>{t.label}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Accent Colors */}
                <div>
                  <h3 className="font-semibold text-sm mb-2">Accent Color</h3>
                  <div className="flex flex-wrap gap-2.5">
                    {(Object.keys(ACCENT_PALETTES) as AccentColor[]).map((colorKey) => {
                      const isSelected = preferences.accentColor === colorKey;
                      const hex = ACCENT_PALETTES[colorKey]['--accent-500'];
                      return (
                        <button
                          key={colorKey}
                          onClick={() => setPreference('accentColor', colorKey)}
                          className={`flex items-center gap-2 px-3 py-2 rounded-xl border capitalize transition ${isSelected ? 'border-accent-500 bg-accent-50/50 dark:bg-accent-500/10 font-medium' : 'border-[#E7DFD7] dark:border-[#382F34] hover:bg-black/5'}`}
                        >
                          <span className="w-3.5 h-3.5 rounded-full shadow-sm" style={{ backgroundColor: hex }} />
                          <span>{colorKey}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Font Size */}
                <div>
                  <h3 className="font-semibold text-sm mb-2">Font Size</h3>
                  <div className="grid grid-cols-3 gap-3">
                    {['small', 'default', 'large'].map((size) => (
                      <button
                        key={size}
                        onClick={() => setPreference('fontSize', size as any)}
                        className={`p-2.5 rounded-xl border capitalize transition ${preferences.fontSize === size ? 'border-accent-500 bg-accent-50/50 dark:bg-accent-500/10 text-accent-600 dark:text-accent-400 font-medium' : 'border-[#E7DFD7] dark:border-[#382F34] hover:bg-black/5'}`}
                      >
                        {size}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'intelligence' && (
              <div className="space-y-4">
                <h3 className="font-semibold text-sm">Reasoning & Intelligence Engine</h3>
                <div className="space-y-2">
                  {[
                    { id: 'fast', title: 'Fast Answers', desc: 'Lower latency token streaming with gemini-2.0-flash.' },
                    { id: 'balanced', title: 'Balanced Companion (Default)', desc: 'Natural warmth and thoughtful insight for general dialogue.' },
                    { id: 'detailed', title: 'Detailed Answers', desc: 'Extended reasoning budget with gemini-2.5-pro for deep technical or academic topics.' },
                    { id: 'context-aware', title: 'Context-Aware RAG', desc: 'Synthesizes long-term episodic memories for deeply personalized assistance.' }
                  ].map(mode => (
                    <div
                      key={mode.id}
                      onClick={() => setPreference('intelligenceMode', mode.id as any)}
                      className={`p-3.5 rounded-xl border cursor-pointer transition ${preferences.intelligenceMode === mode.id ? 'border-accent-500 bg-accent-50/30 dark:bg-accent-500/10 ring-1 ring-accent-400' : 'border-[#E7DFD7] dark:border-[#382F34] hover:bg-black/5'}`}
                    >
                      <p className="font-medium">{mode.title}</p>
                      <p className="text-text-muted-light dark:text-text-muted-dark mt-0.5">{mode.desc}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {activeTab === 'voice' && (
              <div className="space-y-4">
                <h3 className="font-semibold text-sm">Voice Dictation & Speech</h3>
                <div className="space-y-3">
                  <div>
                    <label className="block text-text-secondary-light dark:text-text-secondary-dark mb-1 font-medium">Spoken Response Speed</label>
                    <input
                      type="range"
                      min="0.75"
                      max="1.5"
                      step="0.05"
                      value={preferences.speechSpeed}
                      onChange={(e) => setPreference('speechSpeed', parseFloat(e.target.value))}
                      className="w-full accent-accent-500"
                    />
                    <div className="flex justify-between text-[11px] text-text-muted-light">
                      <span>0.75x</span>
                      <span>{preferences.speechSpeed}x</span>
                      <span>1.5x</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'personalization' && (
              <div className="space-y-4">
                <h3 className="font-semibold text-sm">Custom Instructions</h3>
                <p className="text-text-muted-light dark:text-text-muted-dark text-[11px]">
                  Tell MEENA how she should respond to you and what tone or perspective you prefer.
                </p>
                <textarea
                  value={preferences.customInstructions}
                  onChange={(e) => setPreference('customInstructions', e.target.value)}
                  placeholder="e.g., Speak with quiet warmth, prioritize concise step-by-step logic, and ask clarifying questions..."
                  className="w-full h-28 bg-white dark:bg-[#161214] border border-[#E7DFD7] dark:border-[#382F34] rounded-xl p-3 outline-none focus:ring-1 focus:ring-accent-400 text-xs"
                />
              </div>
            )}

            {activeTab === 'privacy' && (
              <div className="space-y-4">
                <h3 className="font-semibold text-sm">Continuous Memory & Privacy Sovereignty</h3>
                <div className="flex items-center justify-between p-3.5 border border-[#E7DFD7] dark:border-[#382F34] rounded-xl">
                  <div>
                    <p className="font-medium">Enable Long-Term Memory</p>
                    <p className="text-[11px] text-text-muted-light dark:text-text-muted-dark">Allow MEENA to remember your preferences and facts across sessions.</p>
                  </div>
                  <input
                    type="checkbox"
                    checked={preferences.enableMemory}
                    onChange={(e) => setPreference('enableMemory', e.target.checked)}
                    className="w-4 h-4 accent-accent-500 cursor-pointer"
                  />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
