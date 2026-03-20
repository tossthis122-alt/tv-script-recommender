# Project: TV Show Recommender with Script Analysis

I want to build a web app that recommends TV shows based on analysis of their actual scripts/transcripts — not just metadata and ratings. The recommender should understand themes, tone, and writing style to make deeper matches.

## Goals
- Personal project that doubles as a portfolio piece
- Web app interface
- Large catalog (hundreds/thousands of shows)

## Core concept
- Ingest TV show scripts/transcripts and extract features like themes, tone, dialogue style, pacing, humor type, emotional register, genre blends, narrative structure
- Build embeddings or feature vectors from script analysis that capture writing style, not just plot summaries
- Recommend shows based on similarity in these deeper dimensions — e.g. "shows with similar dialogue rhythm to Succession" or "dark comedy tone like Fleabag"
- Users can describe what they're looking for in natural language, or get recommendations based on shows they already like

## Tech direction
- Python backend (FastAPI or similar)
- React frontend
- Vector database for script embeddings (Pinecone, Qdrant, or Chroma)
- LLM-based feature extraction pipeline to analyze scripts and tag themes/tone/style
- Semantic search + collaborative filtering hybrid

## Key questions to figure out
1. Best sources for TV scripts at scale (legal/ethical approaches)
2. Data pipeline architecture — ingestion, chunking strategy for scripts, embedding model selection
3. Feature extraction schema — what dimensions to extract from scripts (tone, themes, dialogue density, vocabulary complexity, etc.)
4. Database schema and vector store design
5. Recommendation algorithm — how to blend semantic similarity with user preferences
6. Frontend UX — how users interact with recommendations

## My background
I'm a data scientist with 10+ years of experience in statistical modeling, multivariate analysis, and machine learning. My career spans the United States Mint (demand/sales forecasting, Power BI dashboards, 80% accuracy improvement) and the DoD Office of Inspector General (network analysis, anomaly detection, anti-trust analysis recovering $200M). I'm proficient in Python, R, Spark, and have extensive experience with Hadoop/Spark distributed environments, hierarchical time series, and building end-to-end data products. I'm based in Dublin, Ireland. This is a side project for personal use and portfolio.

Please start by proposing a system architecture and project structure, then we'll iterate from there.
