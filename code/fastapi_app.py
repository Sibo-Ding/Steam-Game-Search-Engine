from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import os
import uvicorn

from sentence_transformers import SentenceTransformer, CrossEncoder
from pgvector.asyncpg import register_vector
import asyncpg
from database_config import ASYNCPG_DATABASE_CONFIG

# Initialize FastAPI app
app = FastAPI()

# Define input and output models for the API
class SearchRequest(BaseModel):
    search_input: str
    similarity_threshold: float = 0.1
    num_matches: int = 10
    min_price: int
    max_price: int


class SearchResult(BaseModel):
    name: str
    description: str
    original_price: float


# Load the SentenceTransformer and CrossEncoder models globally
embeddings_service = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# API Endpoint for Vector Search
@app.post("/search/", response_model=list[SearchResult])
async def search_games(request: SearchRequest):
    """
    Handles the API request to search for similar games and rerank results.
    """

    # Encode the query into a vector
    qe = embeddings_service.encode(request.search_input).tolist()  # qe = Query Embedding

    # Connect to the database
    conn = await asyncpg.connect(**ASYNCPG_DATABASE_CONFIG)

    # Map the PostgreSQL vector type to a specific Python type (e.g. list)
    await register_vector(conn)

    try:
        # Perform the query
        results = await conn.fetch(
            """
            WITH vector_matches AS (
                SELECT name, 1 - (embedding <=> $1) AS similarity
                FROM steam
                WHERE 1 - (embedding <=> $1) > $2
                ORDER BY similarity DESC
                LIMIT $3
            )
            SELECT name, original_price, description FROM steam
            WHERE name IN (SELECT name FROM vector_matches)
            AND original_price >= $4 AND original_price <= $5
            """,
            qe,
            request.similarity_threshold,
            request.num_matches,
            request.min_price,
            request.max_price,
        )

        if not results:
            raise HTTPException(status_code=404, detail="Did not find any results. Adjust the query parameters.")

        # Collect the description for all the matched similar games.
        candidates = [
            {
                "name": r["name"],
                "description": r["description"],
                "original_price": r["original_price"],
            }
            for r in results
        ]

        # Prepare query-result pairs for reranking
        query_description_pairs = [
            (request.search_input, candidate["description"]) for candidate in candidates
        ]

        # Rerank results using the cross-encoder
        scores = cross_encoder.predict(query_description_pairs)
        for i, candidate in enumerate(candidates):
            candidate["relevance_score"] = scores[i]

        # Sort candidates by relevance score in descending order
        reranked_results = sorted(
            candidates, key=lambda x: x["relevance_score"], reverse=True
        )

    finally:
        await conn.close()

    return reranked_results


if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8080))  # Default to 8080 if PORT is not set
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=PORT)
