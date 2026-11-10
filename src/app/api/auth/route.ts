import { NextResponse } from 'next/server';
import { getSupabaseClient, isSupabaseConfigured } from '@/lib/supabase';

export async function GET() {
  return NextResponse.json({
    supabaseConfigured: isSupabaseConfigured(),
    message: isSupabaseConfigured()
      ? 'Supabase Auth is configured and active.'
      : 'Supabase credentials missing. Authentication is disabled.'
  });
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { action } = body;
    const supabase = getSupabaseClient();

    // Disable authentication instead of using an insecure local demo fallback.
    if (!supabase) {
      return NextResponse.json({ error: 'Authentication is not configured.' }, { status: 503 });
    }

    if (action === 'send-otp') {
      const { identifier, type = 'email' } = body;
      if (!identifier) {
        return NextResponse.json({ error: 'Email or phone number is required.' }, { status: 400 });
      }
      if (type !== 'email') {
        return NextResponse.json({ error: 'OTP sign-in is available for email only.' }, { status: 400 });
      }

      const { error } = await supabase.auth.signInWithOtp({
        email: identifier.trim(),
        options: { shouldCreateUser: true }
      });
      if (error) {
        return NextResponse.json({ error: error.message }, { status: 400 });
      }
      return NextResponse.json({
        success: true,
        provider: 'supabase',
        message: `Verification code dispatched to ${identifier} via Supabase Auth.`
      });
    }

    if (action === 'verify-otp') {
      const { identifier, otp, name } = body;
      if (!identifier || !otp) {
        return NextResponse.json({ error: 'Identifier and OTP code are required.' }, { status: 400 });
      }
      if (!identifier.includes('@')) {
        return NextResponse.json({ error: 'Email verification is required.' }, { status: 400 });
      }

      const { data, error } = await supabase.auth.verifyOtp({
        email: identifier.trim(),
        token: otp.trim(),
        type: 'email'
      });
      if (error) {
        return NextResponse.json({ error: error.message }, { status: 400 });
      }
      const sbUser = data.user;
      const user = {
        id: sbUser?.id || `usr_${Date.now()}`,
        name: name || sbUser?.user_metadata?.name || identifier.split('@')[0],
        username: identifier.split('@')[0],
        email: identifier.toLowerCase(),
        plan: 'free',
        createdAt: sbUser?.created_at || new Date().toISOString()
      };
      return NextResponse.json({
        success: true,
        provider: 'supabase',
        user,
        token: data.session?.access_token || `token_${Date.now()}`
      });
    }

    if (action === 'login-password') {
      const { email, password } = body;
      if (!email || !password) {
        return NextResponse.json({ error: 'Email and password are required.' }, { status: 400 });
      }

      const { data, error } = await supabase.auth.signInWithPassword({ email: email.trim(), password });
      if (error) {
        return NextResponse.json({ error: error.message }, { status: 401 });
      }
      const sbUser = data.user;
      return NextResponse.json({
        success: true,
        provider: 'supabase',
        user: {
          id: sbUser?.id,
          name: sbUser?.user_metadata?.name || email.split('@')[0],
          username: email.split('@')[0],
          email: sbUser?.email || email,
          plan: 'free',
          createdAt: sbUser?.created_at
        },
        token: data.session?.access_token
      });
    }

    if (action === 'register-password') {
      const { email, password, name } = body;
      if (!email || !password || !name) {
        return NextResponse.json({ error: 'Name, email, and password are required.' }, { status: 400 });
      }
      if (password.length < 6) {
        return NextResponse.json({ error: 'Password must be at least 6 characters long.' }, { status: 400 });
      }

      const { data, error } = await supabase.auth.signUp({
        email: email.trim(),
        password,
        options: { data: { name: name.trim() } }
      });
      if (error) {
        return NextResponse.json({ error: error.message }, { status: 400 });
      }
      return NextResponse.json({
        success: true,
        provider: 'supabase',
        user: {
          id: data.user?.id,
          name: name.trim(),
          username: email.split('@')[0],
          email: email.toLowerCase(),
          plan: 'free',
          createdAt: data.user?.created_at || new Date().toISOString()
        },
        token: data.session?.access_token || `token_${Date.now()}`
      });
    }

    if (action === 'oauth') {
      const { provider } = body;
      const { data, error } = await supabase.auth.signInWithOAuth({
        provider: provider as any,
        options: {
          redirectTo: `${process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'}/api/auth/callback`
        }
      });
      if (error) {
        return NextResponse.json({ error: error.message }, { status: 400 });
      }
      return NextResponse.json({ success: true, provider: 'supabase', url: data.url });
    }

    return NextResponse.json({ error: 'Invalid authentication action specified.' }, { status: 400 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
