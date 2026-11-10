'use client';

import React, { useState } from 'react';
import { X, User, Mail, Calendar, Sparkles, Check } from 'lucide-react';

export function ProfileModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const [name, setName] = useState('');
  const [username, setUsername] = useState('');
  const [email] = useState('');
  const [saved, setSaved] = useState(false);

  if (!isOpen) return null;

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => {
      setSaved(false);
      onClose();
    }, 1000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/30 backdrop-blur-sm select-none">
      <div className="w-full max-w-md bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] rounded-2xl shadow-2xl p-6 space-y-5">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-sm text-text-primary-light dark:text-text-primary-dark">
            My Profile
          </h3>
          <button onClick={onClose} className="p-1 rounded-lg text-text-muted-light hover:bg-black/5 dark:hover:bg-white/5">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Avatar Section */}
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-full bg-accent-100 dark:bg-accent-500/20 text-accent-500 font-bold flex items-center justify-center text-lg ring-2 ring-accent-300 dark:ring-accent-400/40">
            {name.trim().charAt(0).toUpperCase() || <User className="w-5 h-5" />}
          </div>
          <div>
            <p className="text-xs font-semibold text-text-primary-light dark:text-text-primary-dark">{name}</p>
            <p className="text-[11px] text-text-muted-light dark:text-text-muted-dark">MEENA account</p>
          </div>
        </div>

        {/* Inputs */}
        <div className="space-y-3 text-xs">
          <div>
            <label className="block text-text-secondary-light dark:text-text-secondary-dark font-medium mb-1">Full Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full bg-[#FAF7F2] dark:bg-[#161214] border border-[#E7DFD7] dark:border-[#382F34] rounded-xl px-3 py-2 outline-none focus:ring-1 focus:ring-accent-400"
            />
          </div>

          <div>
            <label className="block text-text-secondary-light dark:text-text-secondary-dark font-medium mb-1">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full bg-[#FAF7F2] dark:bg-[#161214] border border-[#E7DFD7] dark:border-[#382F34] rounded-xl px-3 py-2 outline-none focus:ring-1 focus:ring-accent-400"
            />
          </div>

          <div>
            <label className="block text-text-secondary-light dark:text-text-secondary-dark font-medium mb-1">Email</label>
            <input
              type="email"
              disabled
              value={email}
              className="w-full bg-[#FAF7F2]/60 dark:bg-[#161214]/60 border border-[#E7DFD7] dark:border-[#382F34] rounded-xl px-3 py-2 text-text-muted-light dark:text-text-muted-dark cursor-not-allowed"
            />
          </div>
        </div>

        {/* Action Button */}
        <div className="flex justify-end gap-2 pt-2">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-xs text-text-secondary-light hover:bg-black/5"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="flex items-center gap-1.5 px-4 py-2 bg-accent-500 hover:bg-accent-600 text-white rounded-xl text-xs font-medium transition shadow-sm"
          >
            {saved ? <Check className="w-4 h-4" /> : null}
            <span>{saved ? 'Saved!' : 'Save Changes'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
