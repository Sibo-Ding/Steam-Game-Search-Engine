# eco395m-final-project

1. Download data from [Kaggle](https://www.kaggle.com/datasets/nikatomashvili/steam-games-dataset), save as `data/steam_data.csv`.
2. Clean data by running `setup/clean_before_upload.py`, output `data/steam_clean_no_header.csv`.
3. Copy the code in `setup/create_tables.sql` into SQL editor and execute it to create the tables.
4. Upload `steam_clean_no_header.csv` into GCP bucket, import into GCP SQL.

## Notes
1. When cleaning "Release Date", if a date is not in "Jan 1, 2000" format, set it to NaT/NaN. This includes "Apr 2019", "Apr-2019", "Coming soon", etc.
2. Game name has non-English (e.g. French), non-alphabetical (e.g. Chinese), and non-character (e.g. emoji) words.
