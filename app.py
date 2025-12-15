from data_preprocessing import clean_text
from vectorizer import TFIDF
from model import LogisticRegressionScratch
from translator import detect_language, translate
import numpy as np

reviews = ["this movie is great", "worst movie ever"]
labels = np.array([1, 0])

cleaned = [clean_text(r) for r in reviews]

vectorizer = TFIDF()
vectorizer.fit(cleaned)
X = vectorizer.transform(cleaned)

model = LogisticRegressionScratch()
model.fit(X, labels)

def predict_sentiment(text):
    lang = detect_language(text)
    if lang != "en":
        text = translate(text, lang, "en")
    cleaned_text = clean_text(text)
    vec = vectorizer.transform([cleaned_text])
    score = model.predict(vec)
    sentiment = "Positive" if score >= 0.5 else "Negative"
    feedback = "People liked this movie" if sentiment == "Positive" else "People disliked this movie"
    if lang != "en":
        feedback = translate(feedback, "en", lang)
    return sentiment, feedback