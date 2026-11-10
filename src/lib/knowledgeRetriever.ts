/**
 * Knowledge and Semantic Retrieval Engine for MEENA
 * Dynamically retrieves factual, technical, and domain knowledge from open web encyclopedia APIs
 * when the external LLM key is waiting to be configured.
 */

interface KnowledgeResult {
  title: string;
  extract: string;
}

/**
 * Clean user query to extract the real topic entity, handling conversational modifiers like:
 * "I meant neurology in shorter terms" -> "neurology"
 * "Explain neurology in simpler terms" -> "neurology"
 * "What is photosynthesis?" -> "photosynthesis"
 * "Explain it in simple words" -> "photosynthesis"
 * "Give me an example" -> "photosynthesis"
 */
export function extractTopicEntity(
  query: string,
  history: { role: string; content: string }[] = []
): { topic: string; isSimplerRequested: boolean; isExampleRequested: boolean; isDetailRequested: boolean } {
  const lower = query.toLowerCase().trim();

  const isSimplerRequested = /\b(shorter|simpler|simple|brief|plain|concise)\b/i.test(lower);
  const isExampleRequested = /\b(example|sample|instance|illustrate)\b/i.test(lower);
  const isDetailRequested = /\b(more detail|detailed|in-depth|deep dive|elaborate|expand)\b/i.test(lower);

  // If the query is an elliptical or contextual follow-up request like "give me an example", "explain it", "more", "why?"
  const isContextualFollowUp =
    /^(give me an example|an example|example|give an example|explain it|tell me more|more|why|how)\b/i.test(lower) ||
    /\b(it|that|this|the first topic|first topic|that topic|previous topic)\b/i.test(lower);

  let clean = query
    .replace(/^(what is|what are|explain|tell me about|define|who is|meaning of|whats the meaning of|what's the meaning of)\s+/i, '')
    .replace(/^(i meant|i mean|what about|how about|can you explain|give me|give)\s+/i, '')
    .replace(/\b(an example of|an example|example|sample|instance)\b/gi, '')
    .replace(/\b(in (shorter|simpler|simple|brief|plain|concise|detail|more detail) (terms|words)?)\b/gi, '')
    .replace(/\b(in (simple|plain) words)\b/gi, '')
    .replace(/\b(in detail)\b/gi, '')
    .replace(/\b(shorter|simpler|simple words|simple terms)\b/gi, '')
    .replace(/[?!.,;:"'()]+$/g, '')
    .trim();

  // If clean is empty or the user made an elliptical follow-up, inherit topic from prior turn!
  if ((!clean || isContextualFollowUp || clean === 'it' || clean === 'that') && history.length > 0) {
    const userMsgs = history.filter(m => m.role === 'user');
    for (let i = userMsgs.length - 1; i >= 0; i--) {
      const prevText = userMsgs[i].content;
      if (prevText !== query) {
        const prevClean = prevText
          .replace(/^(what is|what are|explain|tell me about|define|who is|meaning of|whats the meaning of|what's the meaning of)\s+/i, '')
          .replace(/^(i meant|i mean|what about|how about|can you explain|give me|give)\s+/i, '')
          .replace(/\b(an example of|an example|example|sample)\b/gi, '')
          .replace(/\b(in (shorter|simpler|simple|brief|plain|concise|detail|more detail) (terms|words)?)\b/gi, '')
          .replace(/\b(in (simple|plain) words)\b/gi, '')
          .replace(/[?!.,;:"'()]+$/g, '')
          .trim();
        if (prevClean && prevClean.length > 2 && !/^(it|that|more|why|how)$/i.test(prevClean)) {
          clean = prevClean;
          break;
        }
      }
    }
  }

  return {
    topic: clean,
    isSimplerRequested,
    isExampleRequested,
    isDetailRequested
  };
}

export async function fetchLiveKnowledge(
  query: string,
  history: { role: string; content: string }[] = []
): Promise<KnowledgeResult | null> {
  const { topic } = extractTopicEntity(query, history);
  if (!topic || topic.length < 2) return null;

  try {
    // 1. Direct page summary check (exact title match first)
    const directUrl = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(topic.replace(/\s+/g, '_'))}`;
    const directRes = await fetch(directUrl, {
      headers: { 'User-Agent': 'MEENA-Assistant/1.0 (academic-companion)' }
    });
    if (directRes.ok) {
      const directData = await directRes.json();
      if (directData.extract && directData.type === 'standard' && directData.extract.length > 30) {
        return {
          title: directData.title,
          extract: directData.extract.trim()
        };
      }
    }

    // 2. Search Wikipedia with clean entity
    const searchUrl = `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(topic)}&format=json&utf8=1`;
    const searchRes = await fetch(searchUrl, {
      headers: { 'User-Agent': 'MEENA-Assistant/1.0 (academic-companion)' }
    });
    if (!searchRes.ok) return null;

    const searchData = await searchRes.json();
    const results = searchData.query?.search || [];
    if (!results.length) return null;

    // Filter to find the best title that actually shares semantic similarity with our topic
    let chosenTitle = results[0].title;
    const lowerTopic = topic.toLowerCase();
    for (const r of results.slice(0, 3)) {
      if (r.title.toLowerCase().includes(lowerTopic) || lowerTopic.includes(r.title.toLowerCase())) {
        chosenTitle = r.title;
        break;
      }
    }

    // 3. Fetch introductory extract
    const extractUrl = `https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=1&explaintext=1&titles=${encodeURIComponent(chosenTitle)}&format=json`;
    const extractRes = await fetch(extractUrl, {
      headers: { 'User-Agent': 'MEENA-Assistant/1.0 (academic-companion)' }
    });
    if (!extractRes.ok) return null;

    const extractData = await extractRes.json();
    const pages = extractData.query?.pages || {};
    const firstKey = Object.keys(pages)[0];
    const rawExtract = pages[firstKey]?.extract;

    if (!rawExtract || rawExtract.length < 30) return null;

    return {
      title: chosenTitle,
      extract: rawExtract.trim()
    };
  } catch (err) {
    console.warn('[KNOWLEDGE_FETCH_ERROR]', err);
    return null;
  }
}
