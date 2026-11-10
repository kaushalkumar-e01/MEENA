import { NextResponse } from 'next/server';
import {
  sentimentModel,
  intentModel,
  semanticRetriever,
  topicClusterer,
  analyzeMessage
} from '@/lib/mlEngine';

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    engine: 'MEENA Machine Learning Core',
    metrics: {
      sentiment_classifier: {
        algorithm: 'TF-IDF + Logistic Regression',
        accuracy: sentimentModel.accuracy,
        classes: ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
      },
      intent_classifier: {
        algorithm: 'TF-IDF + Linear SVM (Pegasos)',
        accuracy: intentModel.accuracy,
        classes: [
          'GREETING',
          'CODE_HELP',
          'LANGUAGE_PRACTICE',
          'EMOTIONAL_SUPPORT',
          'FACTUAL_QUESTION',
          'CREATIVE_WRITING',
          'MATH_HELP',
          'DOCUMENT_QA'
        ]
      },
      semantic_retriever: {
        algorithm: 'TF-IDF + Cosine Similarity & KNN',
        indexed_knowledge_entries: 6
      },
      topic_clusterer: {
        algorithm: 'K-Means Clustering',
        clusters: topicClusterer.clusters
      },
      neural_conversational_engine: {
        architecture: '1 Encoder + 13 Decoder Evolved Transformer',
        status: 'Trained checkpoint loaded (checkpoint_best.pt)',
        endpoint: '/ml/meena-generate'
      }
    }
  });
}

export async function POST(req: Request) {
  try {
    const body = await req.json();

    if (body.action === 'generate' || body.prompt) {
      const mlServiceUrl = process.env.ML_SERVICE_URL || 'http://127.0.0.1:8000';
      const prompt = body.prompt || body.text || '';
      const mlRes = await fetch(`${mlServiceUrl}/ml/meena-generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          history: body.history || [],
          temperature: body.temperature || 0.65,
          top_k: body.top_k || 40,
          top_p: body.top_p || 0.9,
          repetition_penalty: body.repetition_penalty || 1.35,
          no_repeat_ngram_size: 3
        })
      });
      if (mlRes.ok) {
        const mlData = await mlRes.json();
        return NextResponse.json(mlData);
      }
    }

    const { text } = body;
    if (!text) {
      return NextResponse.json({ error: 'Text is required for analysis' }, { status: 400 });
    }

    const analysis = analyzeMessage(text);
    return NextResponse.json(analysis);
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
