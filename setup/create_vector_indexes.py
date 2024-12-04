# Adapted from Google Cloud pgvector demo
# https://cloud.google.com/blog/products/databases/faster-similarity-search-performance-with-pgvector-indexes
# https://colab.research.google.com/github/GoogleCloudPlatform/python-docs-samples/blob/main/cloud-sql/postgres/pgvector/notebooks/pgvector_gen_ai_demo.ipynb#scrollTo=_zRBR9YJoENp

from database import engine

def create_vector_indexes(m, ef_construction, operator):
    """Create vector indexes for faster similarity search"""
    with engine.begin() as conn:
        conn.exec_driver_sql(
            f"""CREATE INDEX ON steam
                USING hnsw(embedding {operator})
                WITH (m = {m}, ef_construction = {ef_construction})
                """
        )


if __name__ == "__main__":
    # Create an HNSW index on the `steam` table:
    m = 16  # type: integer
    ef_construction = 100  # type: integer
    operator = "vector_cosine_ops"  # ["vector_cosine_ops", "vector_l2_ops", "vector_ip_ops"]

    # Quick input validations.
    assert type(m) == int, "⚠️ Please input a valid value for m."
    assert type(ef_construction) == int, "⚠️ Please input a valid value for ef_construction."
    assert operator in ["vector_cosine_ops", "vector_l2_ops", "vector_ip_ops"], "⚠️ Please input a valid value for operator."
    
    create_vector_indexes(m, ef_construction, operator)
