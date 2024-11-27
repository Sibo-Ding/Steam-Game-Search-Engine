from database import engine

def create_table():
    with engine.begin() as conn:
        # Activate vector data type
        conn.exec_driver_sql("CREATE EXTENSION IF NOT EXISTS vector;")

        conn.exec_driver_sql(
            """CREATE TABLE steam (
                    name VARCHAR(250) PRIMARY KEY,
                    original_price NUMERIC(10, 2),
                    release_date DATE,
                    description VARCHAR(500),
                    all_reviews_summary VARCHAR(30),
                    developer VARCHAR(1000),
                    supported_languages VARCHAR(1500),
                    tags VARCHAR(500),
                    features VARCHAR(500),
                    embedding VECTOR(384)
                );
            """
        )


if __name__ == "__main__":
    create_table()
