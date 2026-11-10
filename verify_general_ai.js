const http = require('http');

function post(path, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = http.request({
      hostname: '127.0.0.1',
      port: 3000,
      path: path,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    }, (res) => {
      let chunks = '';
      res.on('data', d => chunks += d);
      res.on('end', () => resolve({ status: res.statusCode, body: chunks }));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

function parseSSE(body) {
  return body.split('\n')
    .filter(line => line.startsWith('data: '))
    .map(line => line.slice(6))
    .filter(text => text !== '[DONE]')
    .map(t => { try { return JSON.parse(t).text || ''; } catch { return ''; } })
    .join('');
}

async function runRealGeneralAiTests() {
  console.log('================================================================');
  console.log('TESTING TRUE GENERAL-PURPOSE AI CONVERSATION (UNRESTRICTED)');
  console.log('================================================================');

  const history = [];
  async function ask(prompt) {
    history.push({ role: 'user', content: prompt });
    const res = await post('/api/chat', { messages: history, userName: 'Ananya' });
    const reply = parseSSE(res.body);
    history.push({ role: 'assistant', content: reply });
    return reply;
  }

  const testPrompts = [
    'Hey',
    'What is a database?',
    'What does DBMS stand for?',
    'What is a hypocrite?',
    'Explain quantum physics.',
    'What is aeronautical engineering?',
    'Write a Python program to reverse a string.',
    'What did I ask you first?'
  ];

  for (const p of testPrompts) {
    console.log(`\n>>> USER: "${p}"`);
    const ans = await ask(p);
    console.log(`<<< MEENA:\n${ans}\n------------------------------------------------`);
  }

  console.log('\n================================================================');
  console.log('NEW ISOLATED CONVERSATION: "What is photosynthesis?"');
  console.log('================================================================');
  const newRes = await post('/api/chat', {
    messages: [{ role: 'user', content: 'What is photosynthesis?' }],
    userName: 'Ananya'
  });
  console.log(`<<< MEENA (NEW CONVERSATION):\n${parseSSE(newRes.body)}`);
}

runRealGeneralAiTests().catch(console.error);
