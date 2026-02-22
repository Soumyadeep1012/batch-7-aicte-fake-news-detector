import streamlit as st
import pickle
from urllib.parse import urlparse
from newspaper import Article
import requests
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
from newspaper import Config


load_dotenv()
API_KEY = st.secrets.get("NEWS_API_KEY") # Add your own newsletter api key here, for the program to run in real-time fact checking.
                                    # or it will return to neutral score.
# -----------------------------
# Load ML Model
# -----------------------------
with open("fake_news_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# -----------------------------
# Trusted & Satire Domains
# -----------------------------
TRUSTED_DOMAINS = [
    "bbc.com",
    "reuters.com",
    "thehindu.com",
    "timesofindia.indiatimes.com",
    "ndtv.com",
    "indianexpress.com",
    "hindustantimes.com",
    "pib.gov.in"
]
TRUSTED_SOURCES = [
    "bbc",
    "reuters",
    "ndtv",
    "the hindu",
    "times of india",
    "indian express",
    "hindustan times",
    "press information bureau"
]


SATIRE_DOMAINS = [
    "theonion.com",
    "worldnewsdailyreport.com"
]

# -----------------------------
# Source Credibility Score
# -----------------------------
def source_score(url):
    if not url:
        return None  # No URL provided

    domain = urlparse(url).netloc.lower()

    for trusted in TRUSTED_DOMAINS:
        if trusted in domain:
            return 1.0

    for satire in SATIRE_DOMAINS:
        if satire in domain:
            return 0.0

    return 0.4  # unknown source slightly suspicious

# -----------------------------
# Fact-check Heuristic Score
# -----------------------------
def fact_check_score(text):

    positive_signals = [
        "official gazette",
        "press release",
        "ministry said",
        "spokesperson said",
        "government statement",
        "according to data"
    ]

    negative_signals = [
        "sources said",
        "reports claim",
        "insiders revealed",
        "viral message",
        "whatsapp forward",
        "no official gazette",
        "not yet clarified",
        "not yet published",
        "sources indicated",
        "reportedly",
        "closed-door meeting"

    ]

    score = 0.5
    text_lower = text.lower()

    for phrase in positive_signals:
        if phrase in text_lower:
            score += 0.1

    for phrase in negative_signals:
        if phrase in text_lower:
            score -= 0.15

    if "nationwide policy" in text_lower:
            score -= 0.1

    if "effective immediately" in text_lower:
            score -= 0.1
    return max(0, min(score, 1))

# -----------------------------
# Real-time Cross Verification
# -----------------------------
def realtime_source_check(text):
    
    if not API_KEY:
        return 0.5  # if No API key → neutral score
    

    try:
        claim = text.split(".")[0]
        claim = claim[:100]

        url = (
            f"https://newsapi.org/v2/everything?"
            f"q={claim}&"
            f"language=en&"
            f"apiKey={API_KEY}"
        )

        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("status") != "ok":
            return 0.5
        if "articles" not in data:
            return 0.5

        articles = data["articles"]

        trusted_matches = 0

        for article in articles:
            source_name = article["source"]["name"].lower()
            article_url = article["url"].lower()

            matched = False

    # Check by readable source name
            for trusted in TRUSTED_SOURCES:
                if trusted in source_name:
                   matched = True
                   break

    # If not matched by name, check by domain
            if not matched:
                for trusted_domain in TRUSTED_DOMAINS:
                   if trusted_domain in article_url:
                      matched = True
                      break

            if matched:
               trusted_matches += 1


        if trusted_matches >= 3:
           return 0.8
        elif trusted_matches == 2:
           return 0.6
        elif trusted_matches == 1:
           return 0.4
        else:
           return 0.2

        

    except:
        return 0.5

# -----------------------------
# Simple Summarization
# -----------------------------
def summarize_text(text):
    sentences = text.split(". ")
    return ". ".join(sentences[:3]) + "."

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🧠 AI-Powered Fake News Detector")
if "history" not in st.session_state:
    st.session_state.history = []
st.write("Paste article text OR provide a direct news link.")

url = st.text_input("Enter News URL (Optional)")
text_input = st.text_area("Or Paste News Article Text Here. Following complete proper format with heading of the News Article Text.")

if st.button("Analyze Article"):

    # Extract text
    if url:
        try:
            config = Config()
            config.browser_user_agent = "Mozilla/5.0"
            config.request_timeout = 10

            article = Article(url, config=config)
            article.download()
            article.parse()
            text = article.text.strip()

            if not text:
               st.error("Article content is empty or blocked by website.")
               st.stop()

        except Exception as e:
            st.warning("URL extraction blocked. Please paste article text manually.")
            st.stop()

    elif text_input.strip():
        text = text_input.strip()

    else:
        st.warning("Please provide article text or URL.")
        st.stop()

    # -----------------------------
    # 1️⃣ ML Prediction
    # -----------------------------
    vectorized = vectorizer.transform([text])
    ml_prob = model.predict_proba(vectorized)[0][1]

    # -----------------------------
    # 2️⃣ Source Score
    # -----------------------------
    src_score = source_score(url)

    # -----------------------------
    # 3️⃣ Fact-check Score
    # -----------------------------
    fact_score = fact_check_score(text)

    # -----------------------------
    # 4️⃣ Real-time Score
    # -----------------------------
    realtime_score = realtime_source_check(text)

    # -----------------------------
    # Final Hybrid Score
    # -----------------------------
    if src_score is None:
        final_score = (
            (ml_prob * 0.5) +
            (fact_score * 0.25) +
            (realtime_score * 0.25)
        )
    else:
        final_score = (
            (ml_prob * 0.4) +
            (src_score * 0.2) +
            (fact_score * 0.2) +
            (realtime_score * 0.2)
        )

    final_score = max(0, min(final_score, 1))

    st.session_state.history.append({
    "ml_score": ml_prob,
    "fact_score": fact_score,
    "realtime_score": realtime_score,
    "final_score": final_score
})

    # -----------------------------
    # Display Results
    # -----------------------------
    st.subheader("🔎 Analysis Results")

    st.write(f"ML Probability Score: {round(ml_prob,2)}")
    st.write(f"Source Credibility Score: {src_score if src_score is not None else 'N/A'}")
    st.write(f"Fact-check Score: {round(fact_score,2)}")
    st.write(f"Realtime Verification Score: {round(realtime_score,2)}")
    st.write(f"Final Credibility Score: {round(final_score,2)}")

    if final_score >= 0.65:
       st.success("✅ Classified as TRUE / CREDIBLE")
       st.subheader("📝 Summary")
       st.write(summarize_text(text))

    elif 0.45 <= final_score < 0.65:
       st.warning("⚠️ Classified as UNCERTAIN / NEEDS VERIFICATION")
       st.subheader("📝 Summary")
       st.write(summarize_text(text))

    else:
       st.error("❌ Classified as FAKE / LOW CREDIBILITY")

# -----------------------------
# 📊 Professional Analytics Dashboard
# -----------------------------
if st.session_state.history:

    st.markdown("---")
    st.header("📊 Analytics Dashboard")

    if st.button("Reset Analytics Data"):
       st.session_state.history = []
       st.success("Analytics data reset.")
       st.rerun()

    history = st.session_state.history
    total_articles = len(history)

    if total_articles > 0:
       avg_score = sum(item["final_score"] for item in history) / total_articles
    else:
       avg_score = 0

    true_count = sum(1 for item in history if item["final_score"] >= 0.65)
    uncertain_count = sum(1 for item in history if 0.45 <= item["final_score"] < 0.65)
    fake_count = sum(1 for item in history if item["final_score"] < 0.45)

    # Metric Cards
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Articles", total_articles)
    col2.metric("Average Score", round(avg_score, 2))
    col3.metric("True Articles", true_count)
    col4.metric("Fake Articles", fake_count)
    
    # Pie Chart
    st.subheader("Article Classification Distribution")

    labels = ["True", "Uncertain", "Fake"]
    sizes = [true_count, uncertain_count, fake_count]

    # Remove zero values for clean visualization
    filtered_labels = []
    filtered_sizes = []

    for label, size in zip(labels, sizes):
        if size > 0:
           filtered_labels.append(label)
           filtered_sizes.append(size)

    fig1, ax1 = plt.subplots()
    ax1.pie(filtered_sizes, labels=filtered_labels, autopct='%1.1f%%')
    ax1.axis("equal")
    st.pyplot(fig1)
    plt.close(fig1)

    # Trend Line
    st.subheader("Credibility Score Trend")

    scores = [item["final_score"] for item in history]

    fig2, ax2 = plt.subplots()

    if len(scores) == 1:
       ax2.scatter([1], scores)  # force visible point
    else:
       ax2.plot(range(1, total_articles + 1), scores, marker="o")

    ax2.set_xlabel("Analysis Number")
    ax2.set_ylabel("Credibility Score")
    ax2.set_ylim(0, 1)
    ax2.grid(True)
    st.pyplot(fig2)
    plt.close(fig2)       
st.markdown("---")
st.caption("⚠️ This tool provides AI-assisted credibility estimation and should not be treated as definitive fact-checking.")
