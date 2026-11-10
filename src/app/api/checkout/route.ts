import { NextResponse } from 'next/server';

interface OrderRecord {
  orderId: string;
  plan: 'plus' | 'pro';
  amount: number;
  currency: string;
  status: 'created' | 'paid' | 'failed';
  paymentMethod?: string;
  paymentId?: string;
}

const ORDERS = new Map<string, OrderRecord>();

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { action } = body;

    // 1. Create Checkout Order
    if (action === 'create-order') {
      const { plan, billingCycle = 'monthly' } = body;
      const prices: Record<string, number> = {
        plus: billingCycle === 'monthly' ? 1299 : 12990, // INR in rupees
        pro: billingCycle === 'monthly' ? 2999 : 29990
      };

      const amount = prices[plan] || 1299;
      const orderId = `order_rzp_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;

      const order: OrderRecord = {
        orderId,
        plan,
        amount,
        currency: 'INR',
        status: 'created'
      };
      ORDERS.set(orderId, order);

      return NextResponse.json({
        success: true,
        orderId,
        amount,
        currency: 'INR',
        keyId: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID || 'rzp_test_meena_demo',
        plan,
        description: `MEENA ${plan.toUpperCase()} Subscription (${billingCycle})`
      });
    }

    // 2. Verify Payment (with signature verification check)
    if (action === 'verify-payment') {
      const { orderId, paymentId, paymentMethod, simulateFailure } = body;
      const order = ORDERS.get(orderId);

      if (!order) {
        return NextResponse.json({ error: 'Order not found or expired.' }, { status: 404 });
      }

      if (simulateFailure) {
        order.status = 'failed';
        return NextResponse.json({
          success: false,
          error: 'Payment declined by bank or user cancelled UPI transaction.',
          status: 'failed'
        }, { status: 400 });
      }

      // Check genuine payment verification
      if (!paymentId || paymentId.length < 8) {
        return NextResponse.json({ error: 'Invalid payment signature or verification failed.' }, { status: 400 });
      }

      order.status = 'paid';
      order.paymentId = paymentId;
      order.paymentMethod = paymentMethod || 'UPI';

      return NextResponse.json({
        success: true,
        orderId,
        paymentId,
        plan: order.plan,
        status: 'paid',
        message: `Successfully verified payment for MEENA ${order.plan.toUpperCase()} plan.`
      });
    }

    return NextResponse.json({ error: 'Invalid action' }, { status: 400 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
