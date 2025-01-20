# Adapted from Google Cloud pgvector demo
# https://cloud.google.com/blog/products/databases/using-pgvector-llms-and-langchain-with-google-cloud-databases
# https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/main/cloud-sql/postgres/pgvector/notebooks/pgvector_gen_ai_demo.ipynb#scrollTo=_zRBR9YJoENp

#%%========== Input ==========
# Enter a short description of the game to search for within a specified price range:
search_input = "A game similar to Warhammer."  # type: string
min_price = 0  # type: integer
max_price = 100  # type: integer

similarity_threshold = 0.1  # type: float
num_matches = 10  # type: integer

# Quick input validations.
assert type(search_input) == str, "⚠️ Please input a valid input search text"

#%%========== Encode the query into a vector ==========
from sentence_transformers import SentenceTransformer, CrossEncoder

embeddings_service = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
qe = embeddings_service.encode(search_input).tolist()  # qe = Query Embedding

#%%========== Vector search ==========
from pgvector.asyncpg import register_vector
import asyncio
import asyncpg
from database_config import ASYNCPG_DATABASE_CONFIG

import pandas as pd

candidates = []  # A list storing search results


async def vector_search():
    """
    Find similar games to users' query using `pgvector` cosine similarity search
    over all vector embeddings.
    """
    
    # Connect to the database
    conn = await asyncpg.connect(**ASYNCPG_DATABASE_CONFIG)

    # Map the PostgreSQL vector type to a specific Python type (e.g. list)
    await register_vector(conn)

    # $1, $2 etc. are placeholders in `asyncpg` package,
    #   corresponding to parameters after the query. E.g. $1 = qe
    # 1 - (embedding <=> $1):
    #   Calculates cosine similarity between the query embedding ($1)
    #       and each game embedding (embedding column).
    #   <=>: Cosine distance provided by pgvector; <-> for Euclidean distance.
    #   1 - ... converts distance into similarity.
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
        similarity_threshold,
        num_matches,
        min_price,
        max_price,
    )

    if len(results) == 0:
        raise Exception("Did not find any results. Adjust the query parameters.")

    for r in results:
        # Collect the description for all the matched similar games.
        candidates.append(
            {
                "name": r["name"],
                "description": r["description"],
                "original_price": r["original_price"],
            }
        )

    await conn.close()


# Run the SQL commands now.
asyncio.run(vector_search())

#%%========== Rerank results with a cross-encoder ==========
# Prepare query-result pairs for reranking
query_description_pairs = [
    (search_input, candidate["description"])
    for candidate in candidates
]

# Load cross-encoder model
cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
# Other more computationally complex models
# cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-12-v2")
# cross_encoder = CrossEncoder("cross-encoder/ms-marco-electra-base")
# cross_encoder = CrossEncoder("cross-encoder/ms-marco-TinyBERT-L-6")
# cross_encoder = CrossEncoder("cross-encoder/ms-marco-BERT-base")

# Rerank results using the cross-encoder
scores = cross_encoder.predict(query_description_pairs)
for i, score in enumerate(scores):
    candidates[i]["relevance_score"] = score

# Sort candidates by relevance score in descending order
reranked_results = sorted(candidates, key=lambda x: x["relevance_score"], reverse=True)

#%%====================
# Show the results for similar games that matched the user query.
matches = pd.DataFrame(reranked_results)
print(matches)
