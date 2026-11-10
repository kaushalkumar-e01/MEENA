'use client';

import React, { useState } from 'react';
import { X, Check, Zap, Sparkles } from 'lucide-react';
import { CheckoutModal } from './CheckoutModal';
import { authService } from '@/lib/auth';

export function UpgradeModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const [selectedPlanForCheckout, setSelectedPlanForCheckout] = useState<'plus' | 'pro' | null>(null);
  const session = authService.getSession();
  const currentPlan = session.user?.plan || 'free';

  if (!isOpen) return null;

  return (
    <>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm select-none">
        <div className="w-full max-w-2xl bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] rounded-2xl shadow-2xl p-6 space-y-6 animate-in fade-in zoom-in-95 duration-200">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-semibold text-base text-text-primary-light dark:text-text-primary-dark">
                Upgrade Subscription Plan
              </h3>
              <p className="text-xs text-text-muted-light dark:text-text-muted-dark mt-0.5">
                Unlock extended context, Gemini 2.5 Pro reasoning, and priority RAG memory with Indian UPI & Card billing.
              </p>
            </div>
            <button onClick={onClose} className="p-1 rounded-lg text-text-muted-light hover:bg-black/5 dark:hover:bg-white/5">
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Tiers Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            {/* Free Tier */}
            <div className={`p-4 border rounded-2xl flex flex-col justify-between space-y-4 ${currentPlan === 'free' ? 'border-accent-400 bg-accent-50/10' : 'border-[#E7DFD7] dark:border-[#382F34]'}`}>
              <div>
                <p className="font-semibold text-sm">Free</p>
                <p className="text-2xl font-bold mt-2">₹0<span className="text-xs font-normal text-text-muted-light">/mo</span></p>
                <ul className="mt-4 space-y-2 text-text-secondary-light dark:text-text-secondary-dark">
                  <li className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-accent-500" /> 50 messages / day</li>
                  <li className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-accent-500" /> Gemini 2.0 Flash</li>
                  <li className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-accent-500" /> Basic memory</li>
                </ul>
              </div>
              <button
                disabled={currentPlan === 'free'}
                className="w-full py-2 bg-black/5 dark:bg-white/5 rounded-xl text-text-muted-light font-medium cursor-default"
              >
                {currentPlan === 'free' ? 'Current Plan' : 'Downgrade'}
              </button>
            </div>

            {/* Plus Tier */}
            <div className={`p-4 border-2 rounded-2xl flex flex-col justify-between space-y-4 shadow-sm relative ${currentPlan === 'plus' ? 'border-green-500 bg-green-50/10' : 'border-accent-400 bg-accent-50/20 dark:bg-accent-500/5'}`}>
              <span className="absolute -top-2.5 right-4 px-2 py-0.5 bg-accent-500 text-white text-[10px] font-semibold rounded-full uppercase tracking-wider">
                Popular
              </span>
              <div>
                <p className="font-semibold text-sm text-accent-600 dark:text-accent-400">Plus</p>
                <p className="text-2xl font-bold mt-2">₹1,299<span className="text-xs font-normal text-text-muted-light">/mo</span></p>
                <ul className="mt-4 space-y-2 text-text-secondary-light dark:text-text-secondary-dark">
                  <li className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-accent-500" /> 500 messages / day</li>
                  <li className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-accent-500" /> Gemini 2.5 Pro reasoning</li>
                  <li className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-accent-500" /> 50 file uploads / day</li>
                  <li className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-accent-500" /> Indian UPI & Net Banking</li>
                </ul>
              </div>
              <button
                onClick={() => setSelectedPlanForCheckout('plus')}
                disabled={currentPlan === 'plus'}
                className="w-full py-2 bg-accent-500 hover:bg-accent-600 disabled:bg-green-600 text-white rounded-xl font-medium transition shadow-sm"
              >
                {currentPlan === 'plus' ? 'Active Plan' : 'Purchase Plus'}
              </button>
            </div>

            {/* Pro Tier */}
            <div className={`p-4 border rounded-2xl flex flex-col justify-between space-y-4 ${currentPlan === 'pro' ? 'border-green-500 bg-green-50/10' : 'border-[#E7DFD7] dark:border-[#382F34]'}`}>
              <div>
                <p className="font-semibold text-sm">Pro</p>
                <p className="text-2xl font-bold mt-2">₹2,999<span className="text-xs font-normal text-text-muted-light">/mo</span></p>
                <ul className="mt-4 space-y-2 text-text-secondary-light dark:text-text-secondary-dark">
                  <li className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-accent-500" /> Unlimited messages</li>
                  <li className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-accent-500" /> Deep reasoning priority</li>
                  <li className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-accent-500" /> 200 file uploads / day</li>
                  <li className="flex items-center gap-1.5"><Check className="w-3.5 h-3.5 text-accent-500" /> Priority 3072-dim pgvector</li>
                </ul>
              </div>
              <button
                onClick={() => setSelectedPlanForCheckout('pro')}
                disabled={currentPlan === 'pro'}
                className="w-full py-2 border border-accent-400 text-accent-600 dark:text-accent-400 hover:bg-accent-50 dark:hover:bg-accent-500/10 rounded-xl font-medium transition"
              >
                {currentPlan === 'pro' ? 'Active Plan' : 'Purchase Pro'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Checkout Screen Modal */}
      {selectedPlanForCheckout && (
        <CheckoutModal
          isOpen={true}
          plan={selectedPlanForCheckout}
          onClose={() => setSelectedPlanForCheckout(null)}
          onSuccess={(plan) => {
            setSelectedPlanForCheckout(null);
            onClose();
          }}
        />
      )}
    </>
  );
}
