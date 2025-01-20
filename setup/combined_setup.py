from create_table import create_table
from clean_embedding_local import clean_embedding
from create_vector_indexes import create_vector_indexes
from database import engine
import os

# Change working directory to the current .py file
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

create_table()

IN_PATH = "../data/steam_data.csv"
OUT_TABLE = "steam"

df = clean_embedding(IN_PATH)
df.to_sql(OUT_TABLE, engine, if_exists="replace", index=False)

# Create an HNSW index on the `steam` table:
m = 16  # type: integer
ef_construction = 100  # type: integer
operator = "vector_cosine_ops"  # ["vector_cosine_ops", "vector_l2_ops", "vector_ip_ops"]

# Quick input validations.
assert type(m) == int, "⚠️ Please input a valid value for m."
assert type(ef_construction) == int, "⚠️ Please input a valid value for ef_construction."
assert operator in ["vector_cosine_ops", "vector_l2_ops", "vector_ip_ops"], "⚠️ Please input a valid value for operator."
    
create_vector_indexes(m, ef_construction, operator)
