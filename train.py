import pandas as pd
import pickle
from data_preprocessing import clean_text
from vectorizer import TFIDF
from model import LogisticRegressionScratch

data = pd.read_csv("imdb_reviews_clean.csv")

data = data.dropna()
data = data.sample(8000, random_state=42)

texts = data["review"].astype(str).tolist()
labels = data["sentiment"].str.strip().map({"positive": 1, "negative": 0}).values

cleaned_texts = [clean_text(text) for text in texts]

vectorizer = TFIDF()
vectorizer.fit(cleaned_texts, max_features=12000)
X = vectorizer.transform(cleaned_texts)

model = LogisticRegressionScratch(lr=0.05, epochs=1500)
model.fit(X, labels)

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Training complete. Model saved.")
