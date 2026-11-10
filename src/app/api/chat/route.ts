import { NextResponse } from 'next/server';
import { getGeminiClient, MEENA_SYSTEM_PROMPT } from '@/lib/gemini';
import { queryAgyEngine } from '@/lib/agyBridge';
import { generateIntelligentReply } from '@/lib/intelligentEngine';

export async function POST(req: Request) {
  try {
    const {
      messages,
      model = 'gemini-2.0-flash',
      customInstructions = '',
      userName = 'Friend',
      isTemporary = false
    } = await req.json();

    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return NextResponse.json({ error: 'Messages array is required' }, { status: 400 });
    }

    const lastUserMessage = messages[messages.length - 1]?.content || '';

    const fullSystemInstruction = `
${MEENA_SYSTEM_PROMPT}

User Profile:
- Name: ${userName}
${customInstructions ? `User Custom Instructions:\n${customInstructions}` : ''}
${isTemporary ? 'Notice: Temporary Session. Do not save long-term memory.' : ''}
`;

    // 1. Check for genuine Google Gemini API configuration in process.env.GEMINI_API_KEY
    const ai = getGeminiClient();

    if (ai) {
      try {
        const chatContents = messages.map((m: any) => ({
          role: m.role === 'user' ? 'user' : 'model',
          parts: [{ text: m.content }]
        }));

        const responseStream = await (ai.models as any).generateContentStream({
          model: model || 'gemini-2.0-flash',
          contents: chatContents,
          config: {
            systemInstruction: fullSystemInstruction,
            temperature: 0.7,
          }
        });

        const encoder = new TextEncoder();
        const readable = new ReadableStream({
          async start(controller) {
            try {
              for await (const chunk of responseStream) {
                const text = chunk.text;
                if (text) {
                  controller.enqueue(encoder.encode(`data: ${JSON.stringify({ text })}\n\n`));
                }
              }
              controller.enqueue(encoder.encode(`data: [DONE]\n\n`));
              controller.close();
            } catch (err: any) {
              controller.error(err);
            }
          }
        });

        return new Response(readable, {
          headers: {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
          }
        });
      } catch (geminiError: any) {
        console.error('[GEMINI API STREAM ERROR]', geminiError);
        // Fall through to bridge if cloud key quota exceeded
      }
    }

    // 2. Local Google Gemini / Antigravity Model Bridge
    // Runs genuine general-purpose Gemini models for ANY topic in the world:
    // quantum physics, birthdays, stories, recipes, history, sports, coding, translations, etc.
    let generatedReply: string;
    try {
      generatedReply = await queryAgyEngine(lastUserMessage, messages, fullSystemInstruction);
    } catch (agyError: any) {
      console.warn('[AGY BRIDGE UNAVAILABLE, USING HIGH-PRECISION ENGINE]', agyError.message);
      generatedReply = await generateIntelligentReply(lastUserMessage, messages, userName);
    }

    // Progressive real-time streaming response
    const encoder = new TextEncoder();
    const words = generatedReply.split(' ');

    const readable = new ReadableStream({
      async start(controller) {
        for (let i = 0; i < words.length; i++) {
          const chunk = words[i] + (i === words.length - 1 ? '' : ' ');
          controller.enqueue(encoder.encode(`data: ${JSON.stringify({ text: chunk })}\n\n`));
          await new Promise(r => setTimeout(r, 18));
        }
        controller.enqueue(encoder.encode(`data: [DONE]\n\n`));
        controller.close();
      }
    });

    return new Response(readable, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      }
    });

  } catch (error: any) {
    console.error('Chat API Error:', error);
    return NextResponse.json({ error: 'MEENA encountered an issue generating a response. Please try again.' }, { status: 500 });
  }
}
