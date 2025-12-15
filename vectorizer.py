import numpy as np
from collections import Counter

class TFIDF:
    def __init__(self):
        self.vocab = {}

    def fit(self, corpus, max_features=12000):
        counter = Counter()
        for text in corpus:
            counter.update(text.split())
        most_common = counter.most_common(max_features)
        self.vocab = {word: idx for idx, (word, _) in enumerate(most_common)}

    def transform(self, corpus):
        X = np.zeros((len(corpus), len(self.vocab)), dtype=np.float32)
        for i, text in enumerate(corpus):
            for word in text.split():
                if word in self.vocab:
                    X[i][self.vocab[word]] += 1
        return X
