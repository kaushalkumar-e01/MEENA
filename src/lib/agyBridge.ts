import { execFile } from 'child_process';
import path from 'path';
import fs from 'fs';

const AGY_EXE_PATH = path.join(
  process.env.USERPROFILE || 'C:\\Users\\Ananya Kola',
  '.gemini',
  'bin',
  'agy.exe'
);

/**
 * Executes a conversational request against the local Google Antigravity LLM engine.
 * This runs genuine Gemini models (such as gemini-2.0-flash / gemini-2.5-pro) without
 * needing an external API key to be manually set in .env.local.
 */
export async function queryAgyEngine(
  prompt: string,
  history: { role: string; content: string }[] = [],
  systemInstruction?: string
): Promise<string> {
  if (!fs.existsSync(AGY_EXE_PATH)) {
    throw new Error(`Antigravity binary not found at ${AGY_EXE_PATH}`);
  }

  // Format conversational context cleanly for the general-purpose model
  let fullPrompt = '';
  if (systemInstruction) {
    fullPrompt += `[System Instruction]\n${systemInstruction}\n\n`;
  }

  if (history && history.length > 1) {
    fullPrompt += `[Conversation History]\n`;
    for (const msg of history.slice(-6)) {
      const speaker = msg.role === 'user' ? 'User' : 'MEENA';
      fullPrompt += `${speaker}: ${msg.content}\n`;
    }
    fullPrompt += `\n[Current User Message]\n${prompt}\n\nPlease respond as MEENA directly, helpfully, and conversationally:`;
  } else {
    fullPrompt += prompt;
  }

  return new Promise((resolve, reject) => {
    execFile(
      AGY_EXE_PATH,
      ['--disable-slash-commands', '--print', fullPrompt],
      {
        windowsHide: true,
        maxBuffer: 10 * 1024 * 1024,
        timeout: 45000
      },
      (err, stdout, stderr) => {
        if (err) {
          console.error('[AGY EXEC ERROR]', err, stderr);
          return reject(err);
        }
        const cleaned = stdout.trim();
        resolve(cleaned);
      }
    );
  });
}
