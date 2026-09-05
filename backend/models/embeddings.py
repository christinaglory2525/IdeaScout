from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the AI model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_similarity(user_idea, existing_texts):
    """
    Compare the user's idea with existing papers/projects.
    Returns similarity scores between 0 and 1.
    """

    if not existing_texts:
        return []

    user_embedding = model.encode([user_idea])
    existing_embeddings = model.encode(existing_texts)

    scores = cosine_similarity(
        user_embedding,
        existing_embeddings
    )[0]

    return scores.tolist()