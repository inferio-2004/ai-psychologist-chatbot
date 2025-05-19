import os
import torch  # GPU acceleration
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotly.express as px
import nltk
from nltk.corpus import stopwords
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from bertopic import BERTopic
from umap import UMAP
from wordcloud import WordCloud

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords')

# Check if GPU is available
DEVICE = 0 if torch.cuda.is_available() else -1
print(f"Using device: {'GPU' if DEVICE == 0 else 'CPU'}")

############################################
# 1. Emotion Analysis
############################################

def run_emotion_analysis(user_messages, patient, session, threshold=0.0):
    """
    Uses GPU-accelerated emotion analysis.
    """
    emotion_classifier = pipeline(
        "text-classification",
        model="joeddav/distilbert-base-uncased-go-emotions-student",
        return_all_scores=True,
        device=DEVICE  
    )

    emotion_results = {}
    emotion_counts = {}

    for msg in user_messages:
        scores = emotion_classifier(msg)[0]
        filtered_scores = {e["label"]: round(e["score"], 4) for e in scores if e["score"] > threshold}
        emotion_results[msg] = filtered_scores

        for label, score in filtered_scores.items():
            emotion_counts[label] = emotion_counts.get(label, 0) + score  

    total_emotion_score = sum(emotion_counts.values())  

    emotion_distribution = {
        k: round((v / total_emotion_score) * 100, 2) for k, v in emotion_counts.items()
    } if total_emotion_score > 0 else {}

    top_3_emotions_per_msg = {
        msg: sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]
        for msg, emotions in emotion_results.items()
    }

    filename_ed = f"{patient}_{session}_emotion_distribution.png"
    plt.figure(figsize=(10, 6))
    plt.bar(emotion_distribution.keys(), emotion_distribution.values(), color="royalblue")
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Emotions")
    plt.ylabel("Percentage (%)")
    plt.title("Emotion Distribution Over Conversation")
    plt.tight_layout()
    plt.savefig(filename_ed)
    plt.close()

    return emotion_distribution, top_3_emotions_per_msg, filename_ed

############################################
# 2. Sentiment Analysis
############################################

def run_sentiment_analysis(user_messages, patient, session):
    """
    Uses VADER sentiment analysis.
    """
    analyzer = SentimentIntensityAnalyzer()
    sentiments = np.array([analyzer.polarity_scores(msg)["compound"] for msg in user_messages])
    sentiment_trend = sentiments.mean() if len(sentiments) > 0 else 0
    sentiment_category = "Positive" if sentiment_trend > 0.05 else "Negative" if sentiment_trend < -0.05 else "Neutral"

    filename_st = f"{patient}_{session}_sentiment_trend.png"
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(sentiments) + 1), sentiments, marker='o', linestyle='-', color='b')
    plt.axhline(y=0.05, color='g', linestyle='--')
    plt.axhline(y=-0.05, color='r', linestyle='--')
    plt.xlabel("Message Index")
    plt.ylabel("Sentiment Score")
    plt.title("Sentiment Trend Over Conversation")
    plt.grid()
    plt.tight_layout()
    plt.savefig(filename_st)
    plt.close()

    return sentiment_category, round(sentiment_trend, 4), sentiments.tolist(), filename_st  # Convert to list

############################################
# 3. Concerning Topics Detection
############################################

def run_concern_detection(user_messages):
    """
    Uses zero-shot classification to detect key concerns.
    """
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    concern_labels = [
        "Anxiety & Stress", "Self-Doubt & Low Confidence",
        "Sleep Problems", "Social Isolation",
        "Depression", "Anger Issues",
        "Relationship Problems", "Work/Study Pressure"
    ]

    key_concerns = {}
    threshold = 0.9
    for msg in user_messages:
        result = classifier(msg, concern_labels, multi_label=True)
        detected_labels = {label: round(score, 4)
                           for label, score in zip(result["labels"], result["scores"])
                           if score > threshold}
        if detected_labels:
            key_concerns[msg] = detected_labels

    return key_concerns

############################################
# 4. Topic Modeling & Theme Extraction
############################################

# def run_topic_modeling(user_messages):
#     """
#     Performs topic modeling using BERTopic.
#     Returns the topic names instead of numeric indexes.
#     """
#     topics, probs = [], []
#     topic_descriptions = {}

#     if len(user_messages) >= 3:
#         try:
#             topic_model = BERTopic(
#                 min_topic_size=2,
#                 nr_topics="auto",
#                 umap_model=UMAP(n_components=2, n_neighbors=2, min_dist=0.3)
#             )
            
#             topics, probs = topic_model.fit_transform(user_messages)
            
#             # Extract human-readable topic descriptions
#             topic_info = topic_model.get_topic_info()
#             topic_descriptions = {
#                 row["Topic"]: row["Name"] for _, row in topic_info.iterrows()
#             }

#             # Replace topic indexes with actual topic names
#             topics = [topic_descriptions.get(t, "Unknown Topic") for t in topics]

#             if all(t == "Unknown Topic" for t in topics):
#                 topics, probs = [], []

#         except Exception as e:
#             topics, probs = [], []

#     return topics, probs


############################################
# 5. Interactive Sentiment Analysis
############################################

def run_interactive_sentiment_analysis(sentiments, user_messages, patient, session):
    """
    Generates an interactive sentiment trend plot using Plotly.
    """
    df = pd.DataFrame({'Message': user_messages, 'Sentiment Score': sentiments})
    df['Message Short'] = df['Message'].apply(lambda x: x[:50] + '...' if len(x) > 50 else x)
    df['Index'] = df.index + 1

    fig = px.line(df, x='Index', y='Sentiment Score', title='Interactive Sentiment Trend', markers=True, hover_data={'Message': True})
    filename = f"{patient}_{session}_interactive_sentiment.html"
    fig.write_html(filename)
    
    return filename

############################################
# 6. NLP Summarization
############################################

from transformers import pipeline

from transformers import pipeline, BartTokenizer

from transformers import BartTokenizer, pipeline

def run_nlp_summarization(user_messages):
    """
    Summarizes the conversation using a transformer-based summarizer.
    Handles long inputs by chunking based on token count.
    Returns a summary text.
    """
    if not user_messages:
        return "No messages available for summarization."
    
    # Combine the messages into one conversation text
    conversation_text = " ".join(user_messages)
    
    # Load the tokenizer and summarizer for BART
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
    
    max_input_tokens = 1024  # BART's approximate max tokens per input
    
    # Encode the conversation to get token IDs
    token_ids = tokenizer.encode(conversation_text, add_special_tokens=True)
    num_tokens = len(token_ids)
    
    # If text is short enough, summarize directly
    if num_tokens <= max_input_tokens:
        summary = summarizer(conversation_text, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    
    # Otherwise, split the tokens into chunks that do not exceed max_input_tokens
    chunks = []
    for i in range(0, num_tokens, max_input_tokens):
        chunk_token_ids = token_ids[i:i+max_input_tokens]
        # Decode tokens back to string (skip special tokens)
        chunk_text = tokenizer.decode(chunk_token_ids, skip_special_tokens=True)
        chunks.append(chunk_text)
    
    # Summarize each chunk separately
    chunk_summaries = []
    for chunk in chunks:
        if chunk.strip():
            summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
            chunk_summaries.append(summary[0]['summary_text'])
    
    # Combine chunk summaries into a final summary
    final_summary = " ".join(chunk_summaries)
    return final_summary




############################################
# 7. Lexical Analysis (Word Cloud)
############################################

def run_lexical_analysis(user_messages, patient, session):
    """
    Generates a word cloud from the conversation text.
    """
    text = " ".join(user_messages)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    filename_wc = f"{patient}_{session}_wordcloud.png"
    wordcloud.to_file(filename_wc)
    return filename_wc

############################################
# 8. Main Function: Run Full Analysis
############################################

# Define static directory
STATIC_DIR = os.path.join(os.getcwd(), "static")
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

def run_analysis(patient, session, user_messages):
    """
    Runs all AI-based analytics on conversation data.
    Converts NumPy arrays to lists for JSON serialization.
    """
    emotion_distribution, top_3_emotions_per_msg, filename_ed = run_emotion_analysis(user_messages, patient, session)
    sentiment_category, sentiment_score, sentiments, filename_st = run_sentiment_analysis(user_messages, patient, session)
    interactive_plot_filename = run_interactive_sentiment_analysis(sentiments, user_messages, patient, session)
    key_concerns = run_concern_detection(user_messages)
    #topics, probs = run_topic_modeling(user_messages)
    conversation_summary = run_nlp_summarization(user_messages)
    wordcloud_filename = run_lexical_analysis(user_messages, patient, session)

    # Convert NumPy arrays to Python lists
    # if isinstance(sentiments, np.ndarray):
    #     sentiments = sentiments.tolist()
    # if isinstance(probs, np.ndarray):
    #     probs = probs.tolist()

    return {
        "emotion_analysis": {
            "distribution": emotion_distribution,
            "top_3_emotions_per_message": top_3_emotions_per_msg,
            "image": filename_ed
        },
        "sentiment_analysis": {
            "trend": sentiment_category,
            "score": sentiment_score,
            "sentiments": sentiments,  # Now a Python list
            "image": filename_st
        },
        "interactive_sentiment_analysis": interactive_plot_filename,
        "concern_detection": key_concerns,
        # "topic_modeling": {
        #     "topics": topics,
        #     "probabilities": probs  # Now a Python list
        # },
        "nlp_summarization": conversation_summary,
        "wordcloud": wordcloud_filename
    }
