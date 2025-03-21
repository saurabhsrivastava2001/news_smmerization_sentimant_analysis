import streamlit as st
import os
from utils import fetch_news, sentiment_analysis_summary, extract_trending_words, generate_hindi_summary

st.title("📰 News Summarization & Sentiment Analysis")

# Initialize session state variables
if "news_data" not in st.session_state:
    st.session_state.news_data = None
if "summary_data" not in st.session_state:
    st.session_state.summary_data = None
if "hindi_audio_path" not in st.session_state:
    st.session_state.hindi_audio_path = None

# User input for company name
company = st.text_input("Enter a company name:")

# Fetch and analyze news
if st.button("Analyze News"):
    if not company:
        st.warning("⚠️ Please enter a company name.")
    else:
        with st.spinner("Fetching news..."):
            news = fetch_news(company)

        if not news or "error" in news:
            st.error("❌ Failed to fetch news. Please check your internet connection or try again.")
        else:
            st.session_state.news_data = news
            st.session_state.summary_data = sentiment_analysis_summary(news)

# Display news if available
if st.session_state.news_data:
    summary = st.session_state.summary_data
    news = st.session_state.news_data

    # Sentiment Analysis Summary
    st.subheader("📊 Sentiment Analysis Summary")
    st.write(f"**Total Articles:** {summary['total_articles']}")
    st.write(f"**Sentiment Counts:** {summary['sentiment_counts']}")  
    st.write(f"**Overall Sentiment Trend:** {summary['overall_trend']}")

    # Trending Words
    st.subheader("🔥 Trending Words")
    trending_words = extract_trending_words(news, top_n=5)
    if trending_words:
        st.write(", ".join([f"{word[0]} ({word[1]})" for word in trending_words]))
    else:
        st.write("No significant trending words found.")

    # Display Articles
    st.subheader("📰 News Articles")
    for article in news:
        st.markdown(f"**🔹 {article['title']}**")
        st.markdown(f"🔗 [Read more]({article['link']})")
        st.markdown(f"📝 {article['summary']}")
        st.markdown(f"📊 Sentiment: **{article['sentiment']}**")
        st.write("---")

    # Hindi Summary Button
    if st.button("🎙 Generate Hindi Summary"):
        with st.spinner("Generating Hindi summary..."):
            try:
                hindi_audio_path = generate_hindi_summary(summary, news)

                if hindi_audio_path and os.path.exists(hindi_audio_path):
                    st.session_state.hindi_audio_path = hindi_audio_path
                    st.success("✅ Hindi summary generated successfully!")
                else:
                    st.error("❌ Failed to generate Hindi summary.")

            except Exception as e:
                st.error(f"❌ Error in generating Hindi summary: {e}")

# Show audio only after generation
if st.session_state.hindi_audio_path:
    st.subheader("🔊 Listen to Hindi Summary")
    st.audio(st.session_state.hindi_audio_path, format="audio/mp3")