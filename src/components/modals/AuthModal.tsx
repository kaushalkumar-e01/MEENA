'use client';

import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Mail,
  Lock,
  User,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  Phone,
  KeyRound,
  ShieldCheck
} from 'lucide-react';
import { authService, UserProfile } from '@/lib/auth';

interface AuthModalProps {
  isOpen: boolean;
  onSuccess: (user: UserProfile) => void;
  onClose?: () => void;
}

export function AuthModal({ isOpen, onSuccess, onClose }: AuthModalProps) {
  const [tab, setTab] = useState<'login' | 'signup' | 'otp'>('login');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [otp, setOtp] = useState('');
  const [otpTarget, setOtpTarget] = useState('');
  const [otpType, setOtpType] = useState<'email' | 'phone'>('email');

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  const handlePasswordLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await fetch('/api/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'login-password',
          email: email.trim(),
          password
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Login failed');

      authService.setSession(data.user, data.token);
      onSuccess(data.user);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePasswordSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await fetch('/api/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'register-password',
          name: name.trim(),
          email: email.trim(),
          password
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Registration failed');

      if (data.requiresEmailConfirmation) {
        setSuccessMsg(data.message || 'Please check your email to confirm your account.');
        setTab('login');
        return;
      }

      if (data.user && data.token) {
        authService.setSession(data.user, data.token);
        onSuccess(data.user);
      } else {
        throw new Error('Supabase session could not be established.');
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSendOtp = async (target: string, type: 'email' | 'phone') => {
    if (!target) {
      setError(`Please enter your ${type}.`);
      return;
    }
    setError(null);
    setLoading(true);

    try {
      const res = await fetch('/api/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'send-otp',
          identifier: target.trim(),
          type
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to send OTP');

      setOtpTarget(target.trim());
      setOtpType(type);
      setTab('otp');
      setSuccessMsg(`Verification code sent to ${target.trim()}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await fetch('/api/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'verify-otp',
          identifier: otpTarget,
          otp: otp.trim(),
          name: name.trim() || undefined
        })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Verification failed');

      authService.setSession(data.user, data.token);
      onSuccess(data.user);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleOAuth = async (provider: 'google' | 'apple') => {
    setError(null);
    setLoading(true);
    try {
      const res = await fetch('/api/auth', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'oauth', provider })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'OAuth failed');

      authService.setSession(data.user, data.token);
      onSuccess(data.user);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm select-none">
      <div className="w-full max-w-md bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] rounded-2xl shadow-2xl p-6 sm:p-8 space-y-5 animate-in fade-in zoom-in-95 duration-200">
        {/* Brand Header */}
        <div className="text-center space-y-1.5">
          <div className="w-10 h-10 rounded-2xl bg-accent-100 dark:bg-accent-500/20 text-accent-500 flex items-center justify-center font-bold text-lg mx-auto shadow-sm">
            M
          </div>
          <h2 className="text-lg font-semibold text-text-primary-light dark:text-text-primary-dark">
            {tab === 'login' ? 'Welcome back to MEENA' : tab === 'signup' ? 'Create your MEENA account' : 'Verify Code'}
          </h2>
          <p className="text-xs text-text-muted-light dark:text-text-muted-dark">
            {tab === 'otp'
              ? `Enter the 6-digit verification code sent to ${otpTarget}`
              : 'Sign in to access your mindful conversations, memory, and settings.'}
          </p>
        </div>

        {/* Error / Success Notifications */}
        {error && (
          <div className="flex items-center gap-2 p-3 bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-900 rounded-xl text-xs text-red-600 dark:text-red-400">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}
        {successMsg && !error && (
          <div className="flex items-center gap-2 p-3 bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-900 rounded-xl text-xs text-green-700 dark:text-green-400">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        {/* OTP Screen */}
        {tab === 'otp' ? (
          <form onSubmit={handleVerifyOtp} className="space-y-4">
            <div>
              <label className="block text-xs font-medium text-text-secondary-light dark:text-text-secondary-dark mb-1">
                6-Digit Verification Code
              </label>
              <input
                type="text"
                required
                maxLength={6}
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                placeholder="123456"
                autoFocus
                className="w-full text-center tracking-[0.3em] font-mono text-lg bg-[#FAF7F2] dark:bg-[#161214] border border-[#E7DFD7] dark:border-[#382F34] rounded-xl px-3 py-2.5 outline-none focus:ring-2 focus:ring-accent-400"
              />
            </div>

            <button
              type="submit"
              disabled={loading || otp.length < 6}
              className="w-full py-2.5 bg-accent-500 hover:bg-accent-600 text-white rounded-xl text-xs font-medium transition shadow-sm disabled:opacity-50"
            >
              {loading ? 'Verifying...' : 'Verify & Continue'}
            </button>

            <div className="flex justify-between items-center text-xs pt-1">
              <button
                type="button"
                onClick={() => handleSendOtp(otpTarget, otpType)}
                className="text-accent-600 hover:underline"
              >
                Resend Code
              </button>
              <button
                type="button"
                onClick={() => { setTab('login'); setError(null); }}
                className="text-text-muted-light hover:underline"
              >
                Change identifier
              </button>
            </div>
          </form>
        ) : (
          <div className="space-y-4">
            {/* OAuth Quick Options */}
            <div className="grid grid-cols-2 gap-2.5">
              <button
                type="button"
                onClick={() => handleOAuth('google')}
                disabled={loading}
                className="flex items-center justify-center gap-2 py-2 px-3 border border-[#E7DFD7] dark:border-[#382F34] hover:bg-black/5 dark:hover:bg-white/5 rounded-xl text-xs font-medium text-text-primary-light dark:text-text-primary-dark transition"
              >
                <svg className="w-3.5 h-3.5" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
                </svg>
                <span>Google</span>
              </button>

              <button
                type="button"
                onClick={() => handleOAuth('apple')}
                disabled={loading}
                className="flex items-center justify-center gap-2 py-2 px-3 border border-[#E7DFD7] dark:border-[#382F34] hover:bg-black/5 dark:hover:bg-white/5 rounded-xl text-xs font-medium text-text-primary-light dark:text-text-primary-dark transition"
              >
                <svg className="w-3.5 h-3.5 fill-current" viewBox="0 0 170 170">
                  <path d="M150.37 130.25c-2.45 5.66-5.35 10.87-8.71 15.66-4.58 6.53-8.33 11.05-11.22 13.56-4.48 4.12-9.28 6.23-14.42 6.35-3.69 0-8.14-1.05-13.32-3.18-5.19-2.12-9.97-3.17-14.34-3.17-4.58 0-9.49 1.05-14.75 3.17-5.26 2.13-9.5 3.24-12.74 3.35-4.35.13-9.16-1.9-14.42-6.08-3.69-3.08-7.73-7.94-12.13-14.59-6.3-9.52-11.05-20.2-14.25-32.06-3.2-11.85-4.81-23.2-4.81-34.05 0-14.07 3.51-25.9 10.53-35.48 7.02-9.58 16.03-14.48 27.03-14.71 4.7 0 10.15 1.34 16.34 4.02 6.19 2.68 10.05 4.08 11.58 4.2 1.35-.12 5.56-1.63 12.63-4.53 7.07-2.9 13.06-4.04 17.97-3.41 13.62 1.35 24.16 6.53 31.62 15.54-12.01 7.27-17.9 17.47-17.67 30.61.23 10.3 4.19 19.01 11.87 26.13 7.68 7.12 16.92 11.13 27.72 12.03-2.34 7.28-5.46 14.71-9.35 22.28zM119.22 33.11c0-7.39 2.65-14.37 7.95-20.94 5.3-6.57 11.97-10.73 20.02-12.48.23 1.25.35 2.39.35 3.42 0 7.39-2.82 14.59-8.46 21.6-5.64 7.01-12.44 11.06-20.4 12.15-.36-1.14-.54-2.39-.54-3.75z" />
                </svg>
                <span>Apple</span>
              </button>
            </div>

            <div className="relative flex items-center justify-center">
              <div className="border-t border-[#E7DFD7] dark:border-[#382F34] w-full" />
              <span className="bg-white dark:bg-[#1F191C] px-2 text-[10px] text-text-muted-light dark:text-text-muted-dark uppercase tracking-wider">
                Or with credentials
              </span>
            </div>

            {/* Email / Password Form */}
            <form onSubmit={tab === 'login' ? handlePasswordLogin : handlePasswordSignup} className="space-y-3">
              {tab === 'signup' && (
                <div>
                  <label className="block text-xs font-medium text-text-secondary-light dark:text-text-secondary-dark mb-1">
                    Your Name
                  </label>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Your name"
                    className="w-full text-xs bg-[#FAF7F2] dark:bg-[#161214] border border-[#E7DFD7] dark:border-[#382F34] rounded-xl px-3 py-2 outline-none focus:ring-1 focus:ring-accent-400"
                  />
                </div>
              )}

              <div>
                <label className="block text-xs font-medium text-text-secondary-light dark:text-text-secondary-dark mb-1">
                  Email Address
                </label>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@example.com"
                  className="w-full text-xs bg-[#FAF7F2] dark:bg-[#161214] border border-[#E7DFD7] dark:border-[#382F34] rounded-xl px-3 py-2 outline-none focus:ring-1 focus:ring-accent-400"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-text-secondary-light dark:text-text-secondary-dark mb-1">
                  Password
                </label>
                <input
                  type="password"
                  required
                  minLength={6}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full text-xs bg-[#FAF7F2] dark:bg-[#161214] border border-[#E7DFD7] dark:border-[#382F34] rounded-xl px-3 py-2 outline-none focus:ring-1 focus:ring-accent-400"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 bg-accent-500 hover:bg-accent-600 text-white rounded-xl text-xs font-medium transition shadow-sm disabled:opacity-50 mt-1"
              >
                {loading ? 'Please wait...' : tab === 'login' ? 'Sign In' : 'Sign Up'}
              </button>
            </form>

            {/* Quick OTP Login Option */}
            <div className="pt-2 border-t border-[#E7DFD7]/60 dark:border-[#382F34]/60 text-center space-y-2">
              <button
                type="button"
                onClick={() => handleSendOtp(email, 'email')}
                className="text-xs text-accent-600 dark:text-accent-400 hover:underline inline-flex items-center gap-1 font-medium"
              >
                <Mail className="w-3.5 h-3.5" />
                <span>Sign in with Email OTP / Magic Link instead</span>
              </button>

              <div className="text-xs text-text-muted-light">
                {tab === 'login' ? (
                  <span>Don&apos;t have an account? <button onClick={() => { setTab('signup'); setError(null); }} className="text-accent-600 font-medium hover:underline">Sign up</button></span>
                ) : (
                  <span>Already have an account? <button onClick={() => { setTab('login'); setError(null); }} className="text-accent-600 font-medium hover:underline">Sign in</button></span>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
