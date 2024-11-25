# eco395m-final-project

1. Download data from [Kaggle](https://www.kaggle.com/datasets/nikatomashvili/steam-games-dataset), save as `data/steam_data.csv`.
2. Clean data by running `setup/clean_before_upload.py`, output `data/steam_clean_no_header.csv`.
3. Copy the code in `setup/create_tables.sql` into SQL editor and execute it to create the tables.
4. Upload `steam_clean_no_header.csv` into GCP bucket, import into GCP SQL.

