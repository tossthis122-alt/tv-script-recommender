"""API route handlers."""

from fastapi import APIRouter, HTTPException

from backend.models.schemas import RecommendationRequest, RecommendationResponse, RecommendationResult, ShowInfo
from backend.recommender.engine import recommend_by_text

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/recommend", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):
    """Get TV show recommendations based on a query or liked shows."""
    if not request.query and not request.liked_shows:
        raise HTTPException(status_code=400, detail="Provide a query or liked shows")

    query_text = request.query or f"Shows similar to {', '.join(request.liked_shows)}"
    raw_results = recommend_by_text(query_text, top_k=request.top_k)

    results = []
    if raw_results and raw_results.get("ids"):
        for i, show_id in enumerate(raw_results["ids"][0]):
            metadata = raw_results["metadatas"][0][i] if raw_results.get("metadatas") else {}
            distance = raw_results["distances"][0][i] if raw_results.get("distances") else 0.0
            results.append(
                RecommendationResult(
                    show=ShowInfo(
                        id=show_id,
                        title=metadata.get("title", show_id),
                        year=metadata.get("year"),
                        network=metadata.get("network", ""),
                    ),
                    similarity_score=1 - distance,  # cosine distance to similarity
                    explanation=metadata.get("style_summary", ""),
                )
            )

    return RecommendationResponse(results=results, query_interpretation=query_text)
