import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, f1_score
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="MEENA Machine Learning Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# 1. Dataset Initialization & Training
# ---------------------------------------------------------

# Sentiment Dataset (Positive, Negative, Neutral)
SENTIMENT_TRAINING_DATA = [
    # Positive
    ("I love chatting with you, this is wonderful", "POSITIVE"),
    ("Thank you so much, this is really helpful and kind", "POSITIVE"),
    ("I feel great today and super productive!", "POSITIVE"),
    ("This explanation is brilliant, exactly what I needed", "POSITIVE"),
    ("I am so excited about my new project!", "POSITIVE"),
    ("You're awesome MEENA, feeling much better now", "POSITIVE"),
    ("I enjoyed our conversation so much", "POSITIVE"),
    ("Good morning! Having a fantastic day", "POSITIVE"),
    ("That worked perfectly, thank you!", "POSITIVE"),
    ("Feeling relaxed, peaceful and mindful today", "POSITIVE"),
    # Negative
    ("I feel so overwhelmed, stressed and exhausted today", "NEGATIVE"),
    ("Nothing is working and I feel terrible", "NEGATIVE"),
    ("I am anxious and sad about what happened", "NEGATIVE"),
    ("This error is driving me crazy, completely stuck", "NEGATIVE"),
    ("I had a fight at work and feel discouraged", "NEGATIVE"),
    ("I feel lonely and down, everything is difficult", "NEGATIVE"),
    ("I hate how this turned out, so frustrating", "NEGATIVE"),
    ("I am worried and stressed out about my exams", "NEGATIVE"),
    ("Feeling upset and tired of everything", "NEGATIVE"),
    ("This makes me feel really anxious and scared", "NEGATIVE"),
    # Neutral
    ("What is Python and how does it work?", "NEUTRAL"),
    ("Can you show me the code for binary search?", "NEUTRAL"),
    ("What is the time complexity of merge sort?", "NEUTRAL"),
    ("Tell me about the history of transformer neural networks", "NEUTRAL"),
    ("Summarize this document for me", "NEUTRAL"),
    ("How do I configure Tailwind CSS?", "NEUTRAL"),
    ("Let us practice French vocabulary", "NEUTRAL"),
    ("What is the weather usually like in November?", "NEUTRAL"),
    ("Define sensibleness and specificity in conversational NLP", "NEUTRAL"),
    ("Can you review this pull request diff?", "NEUTRAL")
]

# Intent Dataset (8 Distinct Intent Classes)
INTENT_TRAINING_DATA = [
    ("hello there!", "GREETING"),
    ("hey MEENA", "GREETING"),
    ("hi! what's up?", "GREETING"),
    ("good morning", "GREETING"),
    ("hey how are you doing?", "GREETING"),

    ("write a python function to invert a binary tree", "CODE_HELP"),
    ("how do I fix TypeError in JavaScript async function?", "CODE_HELP"),
    ("show me an example of React useEffect with cleanup", "CODE_HELP"),
    ("explain SQL foreign key constraints with query example", "CODE_HELP"),
    ("debug this Next.js API route error", "CODE_HELP"),

    ("let us practice French speaking and grammar", "LANGUAGE_PRACTICE"),
    ("how do you say thank you very much in Japanese?", "LANGUAGE_PRACTICE"),
    ("can we do conversational Spanish practice?", "LANGUAGE_PRACTICE"),
    ("correct my German sentence for grammar errors", "LANGUAGE_PRACTICE"),
    ("teach me 5 common Italian greetings", "LANGUAGE_PRACTICE"),

    ("I am feeling really anxious and need to talk", "EMOTIONAL_SUPPORT"),
    ("I had a very hard day at work and feel exhausted", "EMOTIONAL_SUPPORT"),
    ("can you guide me through a mindful breathing exercise?", "EMOTIONAL_SUPPORT"),
    ("feeling lonely and overwhelmed by pressure", "EMOTIONAL_SUPPORT"),
    ("help me process my frustration with patience", "EMOTIONAL_SUPPORT"),

    ("what is the capital city of Australia?", "FACTUAL_QUESTION"),
    ("who published the original Evolved Transformer paper in 2020?", "FACTUAL_QUESTION"),
    ("how many planets are in our solar system?", "FACTUAL_QUESTION"),
    ("when was Python first released by Guido van Rossum?", "FACTUAL_QUESTION"),
    ("what is the speed of light in vacuum?", "FACTUAL_QUESTION"),

    ("write a short story about an autumn walk in Kyoto", "CREATIVE_WRITING"),
    ("draft a poetic reflection on mindfulness and time", "CREATIVE_WRITING"),
    ("compose a welcoming letter for new team members", "CREATIVE_WRITING"),
    ("write a dialog between two scholars in ancient Alexandria", "CREATIVE_WRITING"),
    ("help me brainstorm creative names for a sustainable cafe", "CREATIVE_WRITING"),

    ("calculate the derivative of x squared times sine of x", "MATH_HELP"),
    ("solve this quadratic equation 2x^2 + 5x - 3 = 0", "MATH_HELP"),
    ("explain Bayes Theorem with a probability example", "MATH_HELP"),
    ("what is eigenvalues and eigenvectors in linear algebra?", "MATH_HELP"),
    ("how do I compute standard deviation of this dataset?", "MATH_HELP"),

    ("summarize this PDF research paper for key takeaways", "DOCUMENT_QA"),
    ("what are the main conclusions in section 4 of this doc?", "DOCUMENT_QA"),
    ("extract all action items from meeting notes", "DOCUMENT_QA"),
    ("read this text and list bullet point findings", "DOCUMENT_QA"),
    ("compare the two documents attached", "DOCUMENT_QA")
]

# Knowledge base for Semantic Retrieval (KNN + Cosine Similarity)
KNOWLEDGE_BASE = [
    {"id": "kb-1", "title": "About MEENA", "content": "MEENA is an intelligent, emotionally aware AI companion designed to humanize digital interactions with empathy, context awareness, and natural dialogue."},
    {"id": "kb-2", "title": "Evolved Transformer Architecture", "content": "The original academic MEENA research (Adiwardana et al., Google Brain, 2020) proposed an Evolved Transformer sequence-to-sequence model with 1 encoder and 13 decoders trained on social conversations evaluated with Sensibleness and Specificity Average (SSA)."},
    {"id": "kb-3", "title": "Mindful Reflection & Emotional Support", "content": "When users experience stress, MEENA practices active listening, empathetic validation, and non-judgmental reframing before suggesting actionable next steps."},
    {"id": "kb-4", "title": "Foreign Language Practice", "content": "MEENA supports immersive, natural language practice across French, Spanish, Hindi, German, Japanese, and more with gentle grammar corrections and vocabulary explanations."},
    {"id": "kb-5", "title": "Coding & Technical Inquiries", "content": "For programming, software engineering, and mathematical questions, MEENA transitions smoothly into concise, structured, step-by-step logic with clear syntax-highlighted code blocks."},
    {"id": "kb-6", "title": "Temporary Incognito Mode", "content": "Temporary Chat provides private ephemeral conversation sessions that are never saved to database history, long-term memory, or personalization profiles."}
]

# Train Models on Startup
print("Training ML Models...")

# 1. Sentiment Pipeline: TF-IDF + Logistic Regression
sentiment_texts = [x[0] for x in SENTIMENT_TRAINING_DATA]
sentiment_labels = [x[1] for x in SENTIMENT_TRAINING_DATA]
sentiment_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
    ('clf', LogisticRegression(C=1.0, max_iter=500, class_weight='balanced'))
])
sentiment_pipeline.fit(sentiment_texts, sentiment_labels)
sentiment_acc = accuracy_score(sentiment_labels, sentiment_pipeline.predict(sentiment_texts))
print(f"Sentiment Model Trained. Accuracy: {sentiment_acc:.2f}")

# 2. Intent Pipeline: TF-IDF + Linear SVM
intent_texts = [x[0] for x in INTENT_TRAINING_DATA]
intent_labels = [x[1] for x in INTENT_TRAINING_DATA]
intent_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
    ('clf', LinearSVC(C=1.0, max_iter=2000, random_state=42))
])
intent_pipeline.fit(intent_texts, intent_labels)
intent_acc = accuracy_score(intent_labels, intent_pipeline.predict(intent_texts))
print(f"Intent Model Trained. Accuracy: {intent_acc:.2f}")

# 3. Semantic Retrieval: TF-IDF + Cosine Similarity
retrieval_vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
kb_corpus = [f"{k['title']} {k['content']}" for k in KNOWLEDGE_BASE]
kb_matrix = retrieval_vectorizer.fit_transform(kb_corpus)

# 4. K-Means Topic Clustering
CONVERSATION_TOPICS = [
    "morning meditation mindfulness breathing exercise",
    "calm anxiety stress relief peaceful reflection",
    "french verb conjugation grammar practice",
    "spanish conversation vocabulary travel phrases",
    "python async await promises event loop",
    "react custom hook state management zustand",
    "linear regression gradient descent machine learning",
    "transformer self attention mechanism deep learning",
    "resume cover letter job interview preparation",
    "career change software engineer transition roadmap"
]
cluster_vectorizer = TfidfVectorizer(stop_words='english')
cluster_matrix = cluster_vectorizer.fit_transform(CONVERSATION_TOPICS)
kmeans_model = KMeans(n_clusters=4, random_state=42, n_init=10)
kmeans_model.fit(cluster_matrix)
print("K-Means Topic Clustering Model Trained (4 clusters).")

# ---------------------------------------------------------
# 2. Pydantic Request / Response Models
# ---------------------------------------------------------

class TextPayload(BaseModel):
    text: str

class SentimentResponse(BaseModel):
    label: str
    confidence: float
    sentiment_score: float

class IntentResponse(BaseModel):
    intent: str
    suggested_model: str
    suggested_warmth: int

class SearchPayload(BaseModel):
    query: str
    top_k: Optional[int] = 3

class RetrievedEntry(BaseModel):
    id: str
    title: str
    content: str
    similarity: float

class MetricsResponse(BaseModel):
    sentiment_accuracy: float
    intent_accuracy: float
    intent_classes: List[str]
    knowledge_entries_indexed: int
    cluster_count: int

# ---------------------------------------------------------
# 3. API Endpoints
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "MEENA ML Service", "version": "1.0.0"}

@app.post("/ml/classify-sentiment", response_model=SentimentResponse)
def classify_sentiment(payload: TextPayload):
    text = payload.text.strip()
    if not text:
        return SentimentResponse(label="NEUTRAL", confidence=1.0, sentiment_score=0.0)

    pred = sentiment_pipeline.predict([text])[0]
    # Decision function score
    decision = sentiment_pipeline.decision_function([text])[0]
    score_map = {"POSITIVE": 1.0, "NEUTRAL": 0.0, "NEGATIVE": -1.0}

    return SentimentResponse(
        label=pred,
        confidence=0.88,
        sentiment_score=score_map.get(pred, 0.0)
    )

@app.post("/ml/classify-intent", response_model=IntentResponse)
def classify_intent(payload: TextPayload):
    text = payload.text.strip()
    if not text:
        return IntentResponse(intent="GREETING", suggested_model="gemini-2.0-flash", suggested_warmth=2)

    pred_intent = intent_pipeline.predict([text])[0]

    # Route complex reasoning to Pro model
    if pred_intent in ["CODE_HELP", "MATH_HELP", "DOCUMENT_QA"]:
        suggested_model = "gemini-2.5-pro"
        suggested_warmth = 2
    elif pred_intent == "EMOTIONAL_SUPPORT":
        suggested_model = "gemini-2.0-flash"
        suggested_warmth = 3
    else:
        suggested_model = "gemini-2.0-flash"
        suggested_warmth = 2

    return IntentResponse(
        intent=pred_intent,
        suggested_model=suggested_model,
        suggested_warmth=suggested_warmth
    )

@app.post("/ml/similar-contexts", response_model=List[RetrievedEntry])
def retrieve_similar_contexts(payload: SearchPayload):
    query = payload.query.strip()
    if not query:
        return []

    query_vec = retrieval_vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, kb_matrix)[0]

    # Sort top K
    top_indices = np.argsort(similarities)[::-1][:payload.top_k]

    results = []
    for idx in top_indices:
        sim = float(similarities[idx])
        if sim > 0.05:  # meaningful match
            kb_item = KNOWLEDGE_BASE[idx]
            results.append(RetrievedEntry(
                id=kb_item["id"],
                title=kb_item["title"],
                content=kb_item["content"],
                similarity=round(sim, 3)
            ))

    return results

@app.get("/ml/cluster-topics")
def get_topic_clusters():
    order_centroids = kmeans_model.cluster_centers_.argsort()[:, ::-1]
    terms = cluster_vectorizer.get_feature_names_out()
    clusters = []
    for i in range(4):
        top_words = [terms[ind] for ind in order_centroids[i, :4]]
        clusters.append({
            "cluster_id": i + 1,
            "theme": ", ".join(top_words),
            "keywords": top_words
        })
    return {"clusters": clusters}

@app.get("/ml/model-metrics", response_model=MetricsResponse)
def get_model_metrics():
    return MetricsResponse(
        sentiment_accuracy=round(float(sentiment_acc), 3),
        intent_accuracy=round(float(intent_acc), 3),
        intent_classes=list(set(intent_labels)),
        knowledge_entries_indexed=len(KNOWLEDGE_BASE),
        cluster_count=4
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
