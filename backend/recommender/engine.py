"""Recommendation engine: combines vector similarity with optional user preferences."""

from backend.db.vector_store import query_similar
from backend.pipeline.embed import embed_text, features_to_text


def recommend_by_text(query: str, top_k: int = 10) -> dict:
    """Get recommendations from a natural language query.

    The query is embedded directly and compared against show embeddings.
    """
    embedding = embed_text(query)
    return query_similar(embedding, top_k=top_k)


def recommend_by_features(features: dict, top_k: int = 10) -> dict:
    """Get recommendations from extracted feature dict (e.g. from a liked show)."""
    text = features_to_text(features)
    embedding = embed_text(text)
    return query_similar(embedding, top_k=top_k)
