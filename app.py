import streamlit as st

st.set_page_config(
    page_title="AI Fake News Detector",
    page_icon="📰",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #1f4e79;
}
.sub-text {
    text-align: center;
    font-size: 18px;
    color: gray;
}
.feature-box {
    padding: 20px;
    border-radius: 10px;
    background-color: #f0f2f6;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Title Section
st.markdown('<p class="main-title">AI-Powered Fake News Detector for Students</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Analyze articles, assess credibility, and get concise trustworthy summaries.</p>', unsafe_allow_html=True)

st.write("")

# Navigation instruction
st.info("Use the sidebar to navigate to 'Scan Article' page.")

st.write("---")

# Features Section
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="feature-box">🤖<h4>AI-Powered Analysis</h4><p>Advanced ML model identifies fake patterns.</p></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="feature-box">⚡ Real-time Results</h4><p>Instant feedback on news credibility.</p></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="feature-box">📊 Credibility Score</h4><p>Visual score indicating reliability.</p></div>', unsafe_allow_html=True)

st.write("---")

st.subheader("How It Works")

st.write("""
1. User pastes article text or link  
2. System extracts and cleans text  
3. TF-IDF converts text into numbers  
4. Logistic Regression predicts Fake or Real
5. Use API key for real time facts checking  
6. Summary + credibility score displayed
7. Shows Analytic Dashboard  
""")

st.write("---")

st.success("Go to the 'Scan Article' page from the sidebar to analyze news.")
