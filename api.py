from utils import fetch_news, sentiment_analysis_summary, extract_trending_words, generate_hindi_speech
import asyncio

def main():
    company = input("Enter company name: ").strip()

    news = fetch_news(company)

    if not news or "error" in news:
        print("\n❌ Error: Failed to fetch news. Please check your internet connection or try again.")
        return  # Stop execution if no articles are found

    summary = sentiment_analysis_summary(news)
    trending_words = extract_trending_words(news, top_n=5)

    print("\n🔹 Sentiment Analysis Summary 🔹")
    print(f"Total Articles: {summary['total_articles']}")
    print(f"Sentiment Counts: {summary['sentiment_counts']}")
    print(f"Overall Sentiment Trend: {summary['overall_trend']}\n")

    print("\n🔹 Top Trending Words 🔹")
    if trending_words:
        for word, count in trending_words:
            print(f"{word.capitalize()}: {count} times")
    else:
        print("No significant trending words found.")

    print("\n🔹 Article Details 🔹")
    for article in news:
        print(f"🔹 **Title:** {article['title']}")
        print(f"🔗 **Source:** {article['link']}")
        print(f"📝 **Summary:** {article['summary']}")
        print(f"📊 **Sentiment:** {article['sentiment']}")
        print("-" * 80)

    # ✅ Run async function correctly
    print("\n🔹 Generating Hindi News Summary... 🎙")
    try:
        asyncio.run(generate_hindi_speech(summary, news))  # ✅ Fix: Now properly awaits async function
    except Exception as e:
        print(f"❌ Error in generating Hindi summary: {e}")

if __name__ == "__main__":
    main()

