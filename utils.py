import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from collections import Counter
from nltk.corpus import stopwords
import string
from deep_translator import GoogleTranslator
from gtts import gTTS
from datetime import datetime
import re

# Download required NLTK resources
nltk.download("vader_lexicon")
nltk.download("stopwords")

# Initialize sentiment analyzer & translator
sia = SentimentIntensityAnalyzer()
translator = GoogleTranslator(source="en", target="hi")

def analyze_sentiment(text):
    """Analyzes sentiment using VADER."""
    score = sia.polarity_scores(text)["compound"]
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    return "Neutral"

def fetch_news(company_name, num_articles=10):
    """Scrapes Bing News for articles about a company."""
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
            summary = summary_tag.text.strip() if summary_tag else "No summary available."
            first_sentence = re.split(r"(?<=\.)\s", summary)[0]

            sentiment = analyze_sentiment(first_sentence)

            articles.append(
                {
                    "title": title,
                    "link": link,
                    "summary": first_sentence,
                    "sentiment": sentiment,
                    "date": datetime.now().strftime("%Y-%m-%d")
                }
            )

    return articles

def sentiment_analysis_summary(articles):
    """Enhances sentiment analysis with deeper insights."""
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment_counts[article["sentiment"]] += 1

    total_articles = len(articles)
    overall_trend = (
        "Mostly Positive" if sentiment_counts["Positive"] > sentiment_counts["Negative"]
        else "Mostly Negative" if sentiment_counts["Negative"] > sentiment_counts["Positive"]
        else "Neutral"
    )

    return {
        "total_articles": total_articles,
        "sentiment_counts": sentiment_counts,
        "overall_trend": overall_trend,
    }

def extract_trending_words(news_articles, top_n=10):
    """Extracts the most frequent words from news summaries."""
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

def generate_hindi_summary(sentiment_summary, news_articles, filename="hindi_news_summary.mp3"):
    """Generates a concise and natural Hindi summary and saves it as an audio file."""
    # Map English sentiment trends to Hindi for natural phrasing
    trend_map = {
        "Mostly Positive": "ज्यादातर सकारात्मक",
        "Mostly Negative": "ज्यादातर नकारात्मक",
        "Neutral": "तटस्थ"
    }
    
    # Create a concise summary directly in Hindi
    hindi_summary = (
        f"इस कंपनी की खबरों का आज का रुझान {trend_map[sentiment_summary['overall_trend']]} है। "
        f"कुल {sentiment_summary['total_articles']} लेखों में से, "
        f"{sentiment_summary['sentiment_counts']['Positive']} सकारात्मक, "
        f"{sentiment_summary['sentiment_counts']['Negative']} नकारात्मक, "
        f"और {sentiment_summary['sentiment_counts']['Neutral']} तटस्थ हैं। "
        f"यहाँ कुछ मुख्य समाचार हैं: "
    )

    # Add top 2 article summaries (translated to Hindi)
    for i, article in enumerate(news_articles[:5], 1):
        translated_summary = translator.translate(article["summary"])
        hindi_summary += f"{i}. {translated_summary} "

    # Generate audio using gTTS
    try:
        tts = gTTS(text=hindi_summary, lang="hi", slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None