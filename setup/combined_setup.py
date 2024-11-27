from create_table import create_table
from clean_before_upload_local import clean_embedding
from create_vector_indexes import create_vector_indexes
from database import engine

if __name__ == "__main__":

    import os
    # Change working directory to the current .py file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_directory)

    create_table()

    IN_PATH = "../data/steam_data.csv"
    OUT_TABLE = "steam"

    df = clean_embedding(IN_PATH)
    df.to_sql(OUT_TABLE, engine, if_exists="append", index=False)

    # @markdown Create an HNSW index on the `steam` table:
    m = 16  # @param {type:"integer"}
    ef_construction = 100  # @param {type:"integer"}
    operator = "vector_cosine_ops"  # @param ["vector_cosine_ops", "vector_l2_ops", "vector_ip_ops"]

    create_vector_indexes(m, ef_construction, operator)
