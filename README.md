# eco395m-final-project

## Datebase setup
1. Create a PostgreSQL database instance in GCP SQL.
2. Create a database called `steam` in GCP SQL in the "Databases" tab.
3. Create a `.env` file at the top of the repo saving database credentials, following the format in [demo.env](demo.env). You can use the default postgres username, `postgres`, and the password you set. Your host can be found in GCP SQL on the "Overview" tab. The port will be the default Postgres port: `5432`. Connect with database as `steam`.

## Setup
1. Install packages in [requirements.txt](requirements.txt).
2. Download data from [Kaggle](https://www.kaggle.com/datasets/nikatomashvili/steam-games-dataset), save as [data/steam_data.csv](data/steam_data.csv).
3. Create a SQL table by running [create_table.py](setup/create_table.py).
4. Clean data and use sentence transformer to create a column with vector embeddings by running [clean_embedding_local.py](setup/clean_embedding_local.py) for about 1.5 hours on my computer, output `data/steam_clean_no_header.csv`.
    - Loading `sentence_transformers` package locally requires `numpy.__version__` < 2 and `keras.__version__` < 3.
    - Alternatively, run [clean_embedding_GCP_Vertex.ipynb](setup/clean_embedding_GCP_Vertex.ipynb) on GCP Vertex AI for about 1.5 hours; run [clean_embedding_Google_Drive.ipynb](setup/clean_embedding_Google_Drive.ipynb) on Google Drive for about 3.5 hours. Detailed instructions about loading data are in those files.
5. Upload `steam_clean_no_header.csv` into GCP bucket. Load it into `steam` table with the "Import" option in GCP SQL instance's console.
6. Create vector indexes by running [create_vector_indexes.py](setup/create_vector_indexes.py).

Steps 3 to 6 can be combined and automated by running [combined_setup.py](setup/combined_setup.py). However, this is not recommended because it is not efficient and hard to debug.  

## Vector search
In [vector_search.py](code/vector_search.py), modify search criteria and run.  
You can add more search criteria to this code, by doing:
- Add filter criteria `AND column_you_choose = $6` after the `results` query; add parameters to `results`.
- Add parameters to the `vector_search()` function (both define and call).
- Assign values to parameters in the main program.

## FastAPI
1. Start your API server: In your terminal, change working directory to [code](code), run `py -m uvicorn api_search:app --reload` on Windows or `python3 -m uvicorn api_search:app --reload` on Mac.
2. Open Swagger UI: Go to your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
3. Submit the request:
    - Find the endpoint (`/search/`) in the Swagger UI.
    - Click **Try it out**.
    - Modify the JSON request.

## Notes
1. When cleaning "Release Date", if a date is not in "Jan 1, 2000" format, set it to NaT/NaN. This includes "Apr 2019", "Apr-2019", "Coming soon", etc.
2. Game name has non-English (e.g. French), non-alphabetical (e.g. Chinese), and non-character (e.g. emoji) words.

## Remember to format code (black)
## Remember to update requirements.txt