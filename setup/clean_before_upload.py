# Save steam_data.csv under "data" folder, because it is too big to upload to GitHub.

import os
import pandas as pd

# Change working directory to the current .py file
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
# Change working directory to "data"
os.chdir("../data")

# Read csv + Select columns + Write csv
pd.read_csv("steam_data.csv")[
    [
        "Title",
        "Original Price",
        "Release Date",
        "Game Description",
        "All Reviews Summary",
        "Developer",
        "Supported Languages",
        "Popular Tags",
        "Game Features",
    ]
].to_csv("steam_clean_no_header.csv", header=False, index=False)
