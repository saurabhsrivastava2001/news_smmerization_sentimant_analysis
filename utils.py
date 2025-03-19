import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from collections import Counter
from nltk.corpus import stopwords
import string
from googletrans import Translator
from gtts import gTTS
import os
import re
from datetime import datetime

# Download required NLTK resources
nltk.download("vader_lexicon")
nltk.download("stopwords")

# Initialize sentiment analyzer & translator
sia = SentimentIntensityAnalyzer()
translator = Translator()

def analyze_sentiment(text):
    """
    Analyzes sentiment using VADER.
    Returns 'Positive', 'Negative', or 'Neutral'.
    """
    score = sia.polarity_scores(text)["compound"]
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    return "Neutral"

def fetch_news(company_name, num_articles=10):
    """
    Scrapes Bing News for articles about a company.
    Returns a list of dictionaries with title, link, summary, and sentiment.
    """
    base_url = f"https://www.bing.com/news/search?q={company_name.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch news"}

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for item in soup.select("div.news-card")[:num_articles]:
        title_tag = item.select_one("a.title")
        link_tag = item.select_one("a.title")
        summary_tag = item.select_one(".snippet")

        if title_tag and link_tag:
            title = title_tag.text.strip()
            link = link_tag["href"]
            
            # Extract summary (first sentence only)
            summary = summary_tag.text.strip() if summary_tag else "No summary available."
            first_sentence = re.split(r"(?<=\.)\s", summary)[0]  # Splitting at the first full stop

            sentiment = analyze_sentiment(first_sentence)

            articles.append(
                {
                    "title": title,
                    "link": link,
                    "summary": first_sentence,  # Only first sentence
                    "sentiment": sentiment,
                    "date": datetime.now().strftime("%Y-%m-%d")  # Add date for trend analysis
                }
            )

    return articles

def sentiment_analysis_summary(articles):
    """
    Enhances sentiment analysis with deeper insights.
    """
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    sentiment_trend = []
    source_sentiment = {}  # Track sentiment per source
    positive_keywords = Counter()
    negative_keywords = Counter()

    for article in articles:
        sentiment_counts[article["sentiment"]] += 1
        sentiment_trend.append((article["sentiment"], article["date"]))  # Store with date
        
        # Extract source domain from link
        source_domain = re.findall(r"https?://([^/]+)", article["link"])
        if source_domain:
            source = source_domain[0]
            if source not in source_sentiment:
                source_sentiment[source] = {"Positive": 0, "Negative": 0, "Neutral": 0}
            source_sentiment[source][article["sentiment"]] += 1

        # Extract keywords
        words = re.findall(r"\b\w+\b", article["summary"].lower())
        if article["sentiment"] == "Positive":
            positive_keywords.update(words)
        elif article["sentiment"] == "Negative":
            negative_keywords.update(words)

    total_articles = len(articles)
    
    # Determine overall sentiment trend
    if sentiment_counts["Positive"] > sentiment_counts["Negative"]:
        overall_trend = "Mostly Positive"
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"]:
        overall_trend = "Mostly Negative"
    else:
        overall_trend = "Neutral"

    return {
        "total_articles": total_articles,
        "sentiment_counts": sentiment_counts,
        "overall_trend": overall_trend,
        "sentiment_trend": sentiment_trend,
        "source_sentiment": source_sentiment,
        "top_positive_keywords": positive_keywords.most_common(5),
        "top_negative_keywords": negative_keywords.most_common(5),
    }

def extract_trending_words(news_articles, top_n=10):
    """
    Extracts the most frequent words from news summaries.
    Returns the top N words.
    """
    if "error" in news_articles:
        return news_articles

    stop_words = set(stopwords.words("english"))
    all_words = []

    for article in news_articles:
        text = article["summary"].lower()
        words = text.translate(str.maketrans("", "", string.punctuation)).split()
        words = [word for word in words if word.isalnum() and word not in stop_words]
        all_words.extend(words)

    word_counts = Counter(all_words)
    return word_counts.most_common(top_n)

import asyncio
from googletrans import Translator
from gtts import gTTS
import os

translator = Translator()

async def generate_hindi_speech(sentiment_summary, news_articles, filename="news_summary.mp3"):
    """
    Generates a concise Hindi speech and returns the filename.
    """
    print("🟡 Preparing Hindi summary...")

    hindi_summary = f"{sentiment_summary['overall_trend']}।\n"
    hindi_summary += "aaj ke mukhya 5 samachar :\n"
    for i, article in enumerate(news_articles[:5]):
        hindi_summary += f"{i+1}. {article['summary']}।\n"

    try:
        print("🟡 Translating to Hindi...")
        translated_text = await translator.translate(hindi_summary, src="en", dest="hi")
        print("✅ Translation done!")

        print("🟡 Generating speech...")
        tts = gTTS(text=translated_text.text, lang="hi")
        tts.save(filename)
        print(f"✅ Speech saved as {filename}")
        
        return filename  # ✅ Return the generated file path

    except Exception as e:
        print(f"❌ Error in generating speech: {e}")
        return None  # Return None on error
