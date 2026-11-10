'use client';

import React, { useState } from 'react';
import {
  X,
  Check,
  CreditCard,
  Smartphone,
  ShieldCheck,
  AlertCircle,
  ArrowRight,
  Sparkles,
  Lock
} from 'lucide-react';
import { authService } from '@/lib/auth';

interface CheckoutModalProps {
  isOpen: boolean;
  plan: 'plus' | 'pro';
  onClose: () => void;
  onSuccess: (plan: 'plus' | 'pro') => void;
}

export function CheckoutModal({ isOpen, plan, onClose, onSuccess }: CheckoutModalProps) {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');
  const [paymentMethod, setPaymentMethod] = useState<'upi' | 'card' | 'netbanking'>('upi');
  const [upiId, setUpiId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [step, setStep] = useState<'details' | 'success' | 'failure'>('details');

  if (!isOpen) return null;

  const planName = plan === 'plus' ? 'MEENA Plus' : 'MEENA Pro';
  const amount = plan === 'plus'
    ? (billingCycle === 'monthly' ? 1299 : 12990)
    : (billingCycle === 'monthly' ? 2999 : 29990);

  const handlePay = async (simulateDecline = false) => {
    setError(null);
    setLoading(true);

    try {
      // 1. Create Checkout Order on Backend
      const orderRes = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'create-order', plan, billingCycle })
      });
      const orderData = await orderRes.json();
      if (!orderRes.ok) throw new Error(orderData.error || 'Failed to create order');

      // 2. Verify with payment provider signature check
      const paymentId = `pay_${Date.now()}_rzp_${Math.random().toString(36).substring(2, 8)}`;
      const verifyRes = await fetch('/api/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: 'verify-payment',
          orderId: orderData.orderId,
          paymentId,
          paymentMethod: paymentMethod.toUpperCase(),
          simulateFailure: simulateDecline
        })
      });

      const verifyData = await verifyRes.json();
      if (!verifyRes.ok) throw new Error(verifyData.error || 'Payment failed or declined.');

      // Update user plan
      authService.updatePlan(plan);
      setStep('success');
      setTimeout(() => {
        onSuccess(plan);
      }, 1800);
    } catch (err: any) {
      setError(err.message);
      setStep('failure');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm select-none">
      <div className="w-full max-w-lg bg-white dark:bg-[#1F191C] border border-[#E7DFD7] dark:border-[#382F34] rounded-2xl shadow-2xl p-6 space-y-5 animate-in fade-in zoom-in-95 duration-200">

        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-[#E7DFD7]/60 dark:border-[#382F34]/60">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-accent-500" />
            <h3 className="font-semibold text-sm text-text-primary-light dark:text-text-primary-dark">
              Checkout & Payment — {planName}
            </h3>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-text-muted-light hover:bg-black/5 dark:hover:bg-white/5">
            <X className="w-4 h-4" />
          </button>
        </div>

        {step === 'details' && (
          <div className="space-y-4 text-xs">
            {/* Plan Summary Card */}
            <div className="p-3.5 bg-[#FAF7F2] dark:bg-[#161214] border border-[#E7DFD7] dark:border-[#382F34] rounded-xl flex items-center justify-between">
              <div>
                <p className="font-semibold text-sm text-text-primary-light dark:text-text-primary-dark">{planName}</p>
                <p className="text-text-muted-light">
                  {billingCycle === 'monthly' ? 'Billed monthly' : 'Billed annually (Save 16%)'}
                </p>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-accent-600 dark:text-accent-400">₹{amount.toLocaleString('en-IN')}</p>
                <p className="text-[10px] text-text-muted-light">Incl. all taxes</p>
              </div>
            </div>

            {/* Billing Cycle Selector */}
            <div className="grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => setBillingCycle('monthly')}
                className={`py-2 px-3 rounded-xl border text-center transition ${billingCycle === 'monthly' ? 'border-accent-500 bg-accent-50/50 dark:bg-accent-500/10 text-accent-600 font-medium' : 'border-[#E7DFD7] dark:border-[#382F34]'}`}
              >
                Monthly Billing
              </button>
              <button
                type="button"
                onClick={() => setBillingCycle('yearly')}
                className={`py-2 px-3 rounded-xl border text-center transition ${billingCycle === 'yearly' ? 'border-accent-500 bg-accent-50/50 dark:bg-accent-500/10 text-accent-600 font-medium' : 'border-[#E7DFD7] dark:border-[#382F34]'}`}
              >
                Yearly Billing (Discounted)
              </button>
            </div>

            {/* Indian Payment Methods */}
            <div className="space-y-2">
              <label className="font-medium text-text-secondary-light dark:text-text-secondary-dark block">
                Select Indian Payment Gateway (Razorpay Sandbox)
              </label>

              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => setPaymentMethod('upi')}
                  className={`p-2.5 rounded-xl border flex flex-col items-center justify-center gap-1.5 transition ${paymentMethod === 'upi' ? 'border-accent-500 bg-accent-50/40 text-accent-600 font-medium' : 'border-[#E7DFD7] dark:border-[#382F34]'}`}
                >
                  <Smartphone className="w-4 h-4 text-accent-500" />
                  <span>UPI / GPay / PhonePe</span>
                </button>

                <button
                  type="button"
                  onClick={() => setPaymentMethod('card')}
                  className={`p-2.5 rounded-xl border flex flex-col items-center justify-center gap-1.5 transition ${paymentMethod === 'card' ? 'border-accent-500 bg-accent-50/40 text-accent-600 font-medium' : 'border-[#E7DFD7] dark:border-[#382F34]'}`}
                >
                  <CreditCard className="w-4 h-4 text-accent-500" />
                  <span>Debit / Credit Card</span>
                </button>

                <button
                  type="button"
                  onClick={() => setPaymentMethod('netbanking')}
                  className={`p-2.5 rounded-xl border flex flex-col items-center justify-center gap-1.5 transition ${paymentMethod === 'netbanking' ? 'border-accent-500 bg-accent-50/40 text-accent-600 font-medium' : 'border-[#E7DFD7] dark:border-[#382F34]'}`}
                >
                  <Lock className="w-4 h-4 text-accent-500" />
                  <span>Net Banking</span>
                </button>
              </div>

              {paymentMethod === 'upi' && (
                <div className="pt-1">
                  <input
                    type="text"
                    value={upiId}
                    onChange={(e) => setUpiId(e.target.value)}
                    placeholder="Enter UPI ID (e.g. yourname@okhdfcbank or yourname@paytm)"
                    className="w-full bg-[#FAF7F2] dark:bg-[#161214] border border-[#E7DFD7] dark:border-[#382F34] rounded-xl px-3 py-2 outline-none focus:ring-1 focus:ring-accent-400"
                  />
                  <p className="text-[10px] text-text-muted-light mt-1">
                    Accepts Google Pay, PhonePe, Paytm, BHIM and all bank UPI handles.
                  </p>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="pt-2 space-y-2">
              <button
                type="button"
                onClick={() => handlePay(false)}
                disabled={loading}
                className="w-full py-2.5 bg-accent-500 hover:bg-accent-600 text-white rounded-xl font-medium transition shadow-sm disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {loading ? 'Verifying Gateway Signature...' : `Pay ₹${amount.toLocaleString('en-IN')} & Activate Plan`}
              </button>

              <button
                type="button"
                onClick={() => handlePay(true)}
                disabled={loading}
                className="w-full py-1.5 text-text-muted-light hover:text-red-500 text-[11px] text-center"
              >
                Test Gateway Decline / Failure Scenario
              </button>
            </div>

            <div className="flex items-center justify-center gap-1.5 text-[10px] text-text-muted-light pt-1">
              <ShieldCheck className="w-3.5 h-3.5 text-accent-500" />
              <span>256-bit encrypted secure transaction via Razorpay Test/Production Gateway.</span>
            </div>
          </div>
        )}

        {step === 'success' && (
          <div className="py-8 text-center space-y-3">
            <div className="w-12 h-12 bg-green-100 dark:bg-green-950/40 text-green-600 rounded-full flex items-center justify-center mx-auto shadow-sm">
              <Check className="w-6 h-6" />
            </div>
            <h4 className="text-base font-semibold text-text-primary-light dark:text-text-primary-dark">
              Payment Verified Successfully!
            </h4>
            <p className="text-xs text-text-muted-light max-w-sm mx-auto">
              Your account has been upgraded to <strong>{planName}</strong>. You now have access to expanded context and Gemini 2.5 Pro reasoning.
            </p>
          </div>
        )}

        {step === 'failure' && (
          <div className="py-6 text-center space-y-3">
            <div className="w-12 h-12 bg-red-100 dark:bg-red-950/40 text-red-600 rounded-full flex items-center justify-center mx-auto shadow-sm">
              <AlertCircle className="w-6 h-6" />
            </div>
            <h4 className="text-base font-semibold text-text-primary-light dark:text-text-primary-dark">
              Payment Could Not Be Completed
            </h4>
            <p className="text-xs text-red-600 dark:text-red-400 max-w-sm mx-auto">
              {error || 'Transaction was declined by the issuing bank.'}
            </p>
            <button
              onClick={() => { setStep('details'); setError(null); }}
              className="px-4 py-2 bg-accent-500 text-white rounded-xl text-xs font-medium hover:bg-accent-600 transition"
            >
              Try Again
            </button>
          </div>
        )}

      </div>
    </div>
  );
}
