import streamlit as st
import pickle
from data_preprocessing import clean_text
from translator import (
    detect_language,
    translate_online,
    translate_offline,
    LANGUAGE_MAP
)

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="NLP Sentiment Analysis & Language Translator",
    page_icon="🧠",
    layout="centered"
)

# =================================================
# PREMIUM UI + FIXED BACKGROUND
# =================================================
st.markdown("""
<style>

/* IMPORTANT: use .stApp not body */
.stApp {
    background-image:
        linear-gradient(rgba(2, 6, 23, 0.92), rgba(2, 6, 23, 0.92)),
        url("background.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #e5e7eb;
}

/* HERO HEADER */
.hero {
    text-align: center;
    padding: 45px 10px 30px 10px;
}

.hero-title {
    font-size: 44px;
    font-weight: 800;
    background: linear-gradient(90deg, #22d3ee, #4ade80);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #c7d2fe;
    font-size: 16px;
    margin-top: 10px;
}

/* GREEN ANIMATED AI LINE */
.ai-lines {
    height: 6px;
    width: 100%;
    margin: 25px auto 40px auto;
    background: linear-gradient(
        90deg,
        transparent,
        #22c55e,
        #4ade80,
        #22c55e,
        transparent
    );
    background-size: 200% 100%;
    animation: flow 2.5s linear infinite;
    border-radius: 6px;
}

@keyframes flow {
    from { background-position: 200% 0; }
    to   { background-position: -200% 0; }
}

/* GLASS CARD */
.section {
    background: rgba(2, 6, 23, 0.78);
    backdrop-filter: blur(16px);
    padding: 34px;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.10);
    margin-bottom: 50px;
}

/* INPUTS */
.stTextArea textarea {
    background-color: rgba(2,6,23,0.95);
    color: #e5e7eb;
    border-radius: 14px;
    border: 1px solid #1e293b;
}

/* BUTTONS */
.stButton button {
    background: linear-gradient(90deg, #22d3ee, #4ade80);
    color: black;
    font-weight: bold;
    border-radius: 18px;
    padding: 12px 36px;
}

/* INFO BOX */
.info-box {
    background: rgba(15, 23, 42, 0.85);
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #1e293b;
    margin-top: 16px;
}

</style>
""", unsafe_allow_html=True)

# =================================================
# 🔝 HERO HEADER (NO EMPTY BOX)
# =================================================
st.markdown("""
<div class="hero">
    <div class="hero-title">🧠 NLP Sentiment Analysis & Language Translator</div>
    <div class="hero-subtitle">
        Movie Review Sentiment Analysis • Tyrex Translator • Online & Offline AI
    </div>
</div>

<div class="ai-lines"></div>
""", unsafe_allow_html=True)

# =================================================
# 🎬 MOVIE SENTIMENT ANALYZER
# =================================================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🎬 Movie Review Sentiment Analyzer")
st.caption("Multilingual • Trained from Scratch • Production Ready")

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

review = st.text_area(
    "Enter a movie review (any language)",
    placeholder="Example: Yeh movie bahut hi zabardast thi..."
)

sentiment_mode = st.radio(
    "Translation Mode for Sentiment",
    ["Online (Internet)", "Offline (No Internet)"],
    horizontal=True
)

if st.button("Analyze Movie Review"):
    if review.strip():
        src_lang = detect_language(review)

        review_en = (
            translate_online(review, src_lang, "en")
            if sentiment_mode == "Online (Internet)"
            else translate_offline(review, src_lang, "en")
        )

        cleaned = clean_text(review_en)
        vec = vectorizer.transform([cleaned])
        score = model.predict(vec)[0]

        sentiment = "Positive 😊" if score >= 0.5 else "Negative 😞"

        feedback_en = (
            "The audience responded positively to the movie, appreciating its overall experience."
            if score >= 0.5
            else "The audience did not respond well to the movie due to weak storytelling or execution."
        )

        feedback = (
            translate_online(feedback_en, "en", src_lang)
            if sentiment_mode == "Online (Internet)"
            else translate_offline(feedback_en, "en", src_lang)
        )

        st.success(f"Sentiment: {sentiment}")
        st.markdown(f"<div class='info-box'>{feedback}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a movie review.")

st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# 🌍 TYREX LANGUAGE TRANSLATOR
# =================================================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🌍 Tyrex Language Translator")
st.caption("Professional AI Translator • Online + Offline • Transformer-based")

input_text = st.text_area(
    "Enter text to translate",
    placeholder="Example: Artificial Intelligence will change the world"
)

translator_mode = st.radio(
    "Translation Mode",
    ["Online (Internet)", "Offline (No Internet)"],
    horizontal=True,
    key="translator_mode"
)

language_names = ["Auto Detect"] + list(LANGUAGE_MAP.values())
col1, col2 = st.columns(2)

with col1:
    from_lang_name = st.selectbox("From Language", language_names)

with col2:
    to_lang_name = st.selectbox("To Language", list(LANGUAGE_MAP.values()))

st.markdown("""
<div class="info-box">
<b>Offline Translation Supported Languages:</b><br>
English, Hindi, Spanish, French, German, Italian, Portuguese,
Russian, Arabic, Chinese, Japanese, Korean
</div>
""", unsafe_allow_html=True)

if st.button("Translate"):
    if input_text.strip():
        src_lang = (
            detect_language(input_text)
            if from_lang_name == "Auto Detect"
            else [c for c, n in LANGUAGE_MAP.items() if n == from_lang_name][0]
        )

        tgt_lang = [c for c, n in LANGUAGE_MAP.items() if n == to_lang_name][0]

        translated_text = (
            translate_online(input_text, src_lang, tgt_lang)
            if translator_mode == "Online (Internet)"
            else translate_offline(input_text, src_lang, tgt_lang)
        )

        st.subheader("Translated Output")
        st.success(translated_text)
    else:
        st.warning("Please enter text to translate.")

st.markdown("</div>", unsafe_allow_html=True)
