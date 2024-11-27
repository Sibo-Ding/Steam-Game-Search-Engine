# Adapted from Google Cloud pgvector demo
# https://cloud.google.com/blog/products/databases/using-pgvector-llms-and-langchain-with-google-cloud-databases
# https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/main/cloud-sql/postgres/pgvector/notebooks/pgvector_gen_ai_demo.ipynb#scrollTo=_zRBR9YJoENp
# https://cloud.google.com/blog/products/databases/faster-similarity-search-performance-with-pgvector-indexes

from database import engine

# Create vector indexes for faster similarity search
# @markdown Create an HNSW index on the `steam` table:
m = 16  # @param {type:"integer"}
ef_construction = 100  # @param {type:"integer"}
operator = "vector_cosine_ops"  # @param ["vector_cosine_ops", "vector_l2_ops", "vector_ip_ops"]

with engine.begin() as conn:
    conn.exec_driver_sql(
        f"""CREATE INDEX ON steam
            USING hnsw(embeddings {operator})
            WITH (m = {m}, ef_construction = {ef_construction})
            """
    )
