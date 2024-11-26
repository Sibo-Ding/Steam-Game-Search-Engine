# eco395m-final-project

1. Download data from [Kaggle](https://www.kaggle.com/datasets/nikatomashvili/steam-games-dataset), save as `data/steam_data.csv`.
2. Clean data and use sentence transformer to create a column with vectors/embeddings by running `setup/clean_before_upload.py`, output `data/steam_clean_no_header.csv`.
    - Alternatively, run `setup/clean_before_upload_GCP_Vertex.ipynb` on GCP Vertex AI for about 1.5 hours; run `setup/clean_before_upload_Google_Drive.ipynb` on Google Drive for about 3.5 hours. Detailed instructions about loading data are in those files.
3. Copy the code in `setup/create_tables.sql` into SQL editor and execute it to create the tables.
4. Upload `steam_clean_no_header.csv` into GCP bucket, import into GCP SQL.

## Notes
1. When cleaning "Release Date", if a date is not in "Jan 1, 2000" format, set it to NaT/NaN. This includes "Apr 2019", "Apr-2019", "Coming soon", etc.
2. Game name has non-English (e.g. French), non-alphabetical (e.g. Chinese), and non-character (e.g. emoji) words.
