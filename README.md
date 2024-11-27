# eco395m-final-project

## Datebase setup
1. Go to GCP SQL and create a PostgreSQL database instance.
2. Use GCP SQL to create a database called `steam`. You can do this in the "Databases" tab.
3. Create a `.env` file saving database credentials, similar to [demo.env](demo.env). You can use the default postgres username, `postgres`, and the password you set. Your host can be found in GCP SQL on the "Overview" tab. The port will be the default Postgres port: `5432`. Connect with database as `steam`.

## Setup
1. Install packages in [requirements.txt](requirements.txt).
2. Download data from [Kaggle](https://www.kaggle.com/datasets/nikatomashvili/steam-games-dataset), save as [data/steam_data.csv](data/steam_data.csv).
3. Create a SQL table by running [create_table.py](setup/create_table.py).
4. Clean data and use sentence transformer to create a column with vectors/embeddings by running [clean_embedding_local.py](setup/clean_embedding_local.py), output `data/steam_clean_no_header.csv`.
    - To load `sentence_transformers` package locally, it requires `numpy` version < 2, `keras` version < 3.
    - Alternatively, run [clean_embedding_GCP_Vertex.ipynb](setup/clean_embedding_GCP_Vertex.ipynb) on GCP Vertex AI for about 1.5 hours; run [clean_embedding_Google_Drive.ipynb](setup/clean_embedding_Google_Drive.ipynb) on Google Drive for about 3.5 hours. Detailed instructions about loading data are in those files.
5. Upload `steam_clean_no_header.csv` into GCP bucket. Load it into `steam` table with the "Import" option in GCP SQL instance's console.
6. Create vector indexes by running [create_vector_indexes.py](setup/create_vector_indexes.py).

Steps 3 to 6 can be combined and automated by running [combined_setup.py](setup/combined_setup.py). However, this is not recommended because it is not efficient and hard to debug.  

## Vector search
In [vector_search.py](code/vector_search.py), modify search criteria and run.  
You can add more search criteria to this code:
- Add filter criteria `AND column_you_choose = $6` after the `results` query; add parameters to `results`.
- Add parameters to the `main()` function (both define and call).
- Assign values to parameters in the main program.

## Notes
1. When cleaning "Release Date", if a date is not in "Jan 1, 2000" format, set it to NaT/NaN. This includes "Apr 2019", "Apr-2019", "Coming soon", etc.
2. Game name has non-English (e.g. French), non-alphabetical (e.g. Chinese), and non-character (e.g. emoji) words.

## Remember to format code (black)
## Remember to update requirements.txt