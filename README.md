🧠 AI-Powered Fake News Detector for Students

A Hybrid AI-based web application that analyzes news articles and estimates their credibility using Machine Learning, source verification, heuristic analysis, and real-time cross-checking.

📌 Problem Statement

Misinformation spreads rapidly through online platforms, making it difficult for students to differentiate between reliable and fake information. This project aims to provide an AI-powered system that evaluates news credibility and promotes digital literacy.

🚀 Features

🔎 Analyze news via URL or pasted article text

🤖 Machine Learning-based fake news classification

🌐 Source credibility verification

📊 Real-time cross-verification using NewsAPI

🧠 Hybrid credibility scoring system

📈 Interactive analytics dashboard

📝 Automatic article summary generation

☁️ Deployed on Streamlit Cloud

🏗️ System Architecture

Input (URL / Text)
→ Text Extraction (Newspaper3k)
→ TF-IDF Vectorization
→ Logistic Regression Model
→ Source Credibility Scoring
→ Heuristic Fact Signal Analysis
→ Real-Time NewsAPI Verification
→ Hybrid Weighted Scoring
→ Final Classification (TRUE / UNCERTAIN / FAKE)

🧠 AI & ML Techniques Used

Supervised Machine Learning (Binary Classification)

TF-IDF Feature Extraction

Logistic Regression Classifier

Hybrid Weighted Scoring System

Heuristic-Based Fact Detection

API-based Real-Time Cross Verification

📊 Model Evaluation

Train-Test Split Validation

Accuracy Measurement

Precision & Recall

F1-Score

Confusion Matrix Analysis

🛠️ Technologies Used

Python

Streamlit

Scikit-learn

Newspaper3k

NewsAPI

Matplotlib

GitHub

Streamlit Cloud

🔐 Environment Variables

This project uses a NewsAPI key stored securely via environment variables.

For local setup:

Create a .env file:

NEWS_API_KEY = your_api_key_here

For Streamlit Cloud:

Add the key in App Settings → Secrets:

NEWS_API_KEY = "your_api_key_here"

💻 Installation & Local Setup

Clone the repository:

git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py
🌐 Live Deployment

⚠️ Limitations

Trained mainly on limited news datasets

Performance may vary on global news

Heuristic rules may not generalize universally

Dependent on NewsAPI rate limits

Deep learning models not yet integrated

🔮 Future Scope

Integration with BERT / Transformer models

Multilingual news detection

Browser extension for real-time scanning

Mobile application deployment

Expanded dataset training

🎓 Academic Context

Capstone Project
Department of Computer Science & Engineering
JIS University

