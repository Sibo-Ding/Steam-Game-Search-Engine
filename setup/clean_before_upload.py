# Save steam_data.csv under "data" folder, because it is too big to upload to GitHub.

import os
import pandas as pd

# Change working directory to the current .py file
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)
# Change working directory to "data"
os.chdir("../data")

# Read csv + Drop NA Title + Clean price + Clean date + Select columns + Write csv
df = pd.read_csv("steam_data.csv")
df.dropna(subset=["Title"]).assign(
    original_price=df["Original Price"]
    .replace("Free", "0")  # Replace "Free" with "0"
    .str.replace(r"[$,]", "", regex=True)  # Remove "$" and ","
    .astype(float)  # Convert to float
).assign(
    # If a date is not in "Jan 1, 2000" format, set it to NaT/NaN
    release_date=pd.to_datetime(df["Release Date"], format="%d %b, %Y", errors="coerce")
)[
    [
        "Title",
        "original_price",
        "release_date",
        "Game Description",
        "All Reviews Summary",
        "Developer",
        "Supported Languages",
        "Popular Tags",
        "Game Features",
    ]
].to_csv(
    "steam_clean_no_header.csv", header=False, index=False
)
