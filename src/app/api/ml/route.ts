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
      }
    }
  });
}

export async function POST(req: Request) {
  try {
    const { text } = await req.json();
    if (!text) {
      return NextResponse.json({ error: 'Text is required for analysis' }, { status: 400 });
    }

    const analysis = analyzeMessage(text);
    return NextResponse.json(analysis);
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
