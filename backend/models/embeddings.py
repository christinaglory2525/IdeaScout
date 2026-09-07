from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(user_idea, texts):

    if not texts:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        [user_idea] + texts
    )

    scores = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    return scores