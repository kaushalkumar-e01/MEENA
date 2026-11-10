import { NextResponse } from 'next/server';

interface SharedLinkRecord {
  shareId: string;
  conversationId: string;
  title: string;
  messages: any[];
  createdAt: string;
  isRevoked: boolean;
}

const SHARED_STORE = new Map<string, SharedLinkRecord>();

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { action, conversationId, title, messages, shareId } = body;

    // 1. Create or Share
    if (action === 'create') {
      const generatedId = `share_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
      // Sanitize messages so internal account or system data is never leaked
      const sanitizedMessages = (messages || []).map((m: any) => ({
        id: m.id,
        role: m.role,
        content: m.content,
        createdAt: m.createdAt
      }));

      SHARED_STORE.set(generatedId, {
        shareId: generatedId,
        conversationId,
        title: title || 'Shared Conversation',
        messages: sanitizedMessages,
        createdAt: new Date().toISOString(),
        isRevoked: false
      });

      return NextResponse.json({
        success: true,
        shareId: generatedId,
        url: `/share/${generatedId}`
      });
    }

    // 2. Revoke Sharing
    if (action === 'revoke') {
      if (!shareId || !SHARED_STORE.has(shareId)) {
        return NextResponse.json({ error: 'Share link not found' }, { status: 404 });
      }
      const record = SHARED_STORE.get(shareId)!;
      record.isRevoked = true;
      return NextResponse.json({ success: true, message: 'Share link has been revoked.' });
    }

    return NextResponse.json({ error: 'Invalid action' }, { status: 400 });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

export async function GET(req: Request) {
  const { searchParams } = new URL(req.url);
  const shareId = searchParams.get('id');

  if (!shareId || !SHARED_STORE.has(shareId)) {
    return NextResponse.json({ error: 'Shared conversation not found or expired.' }, { status: 404 });
  }

  const record = SHARED_STORE.get(shareId)!;
  if (record.isRevoked) {
    return NextResponse.json({ error: 'This conversation link has been revoked by the author.' }, { status: 410 });
  }

  return NextResponse.json({
    title: record.title,
    messages: record.messages,
    createdAt: record.createdAt
  });
}
