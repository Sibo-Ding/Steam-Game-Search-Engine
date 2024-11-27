#==========Load environment==========
# Save steam_data.csv under "data" folder

import os
# Change working directory to the current .py file
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

IN_PATH = "../data/steam_data.csv"
OUT_PATH = "../data/steam_clean_no_header.csv"

#====================
from tqdm import tqdm
import pandas as pd
from sentence_transformers import SentenceTransformer

def clean_embedding(IN_PATH):
#==========Clean data==========
    tqdm.pandas()  # Progress bar

    # Read csv + Drop NA Title
    # Clean price: Replace "Free" with "0" + Remove "$" and "," + Convert to float
    # Clean date: coerce: If a date is not in "Jan 1, 2000" format, set it to NaT/NaN
    # Combine Title, Description, Tags, and Features to one column "search_text"
    # Remane + Select columns
    df = (
        pd.read_csv(IN_PATH)
        .dropna(subset=["Title"])
        .assign(
            original_price=lambda df_: df_["Original Price"]
                .replace("Free", "0")
                .str.replace(r"[$,]", "", regex=True)
                .astype(float),
            release_date=lambda df_: pd.to_datetime(
                df_["Release Date"], format="%d %b, %Y", errors="coerce"
            ),
            search_text=lambda df_: df_["Title"]
                + " " + df_["Game Description"].fillna("")
                + " " + df_["Popular Tags"].fillna("")
                + " " + df_["Game Features"].fillna(""),
        )
        .rename(
            columns={
                "Title": "name",
                "Game Description": "description",
                "All Reviews Summary": "all_reviews_summary",
                "Developer": "developer",
                "Supported Languages": "supported_languages",
                "Popular Tags": "tags",
                "Game Features": "features",
            }
        )
    )[
        [
            "name",
            "original_price",
            "release_date",
            "description",
            "all_reviews_summary",
            "developer",
            "supported_languages",
            "tags",
            "features",
            "search_text",
        ]
    ]

#==========Sentence transformer==========
    # Initialize Sentence Transformer model
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    # Other more computationally complex models
    # model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
    # model = SentenceTransformer("xlm-r-bert-base-nli-stsb-mean-tokens")
    # model = SentenceTransformer("LaBSE")

    # Add embedding column with progress bar
    df["embedding"] = df["search_text"].progress_apply(
        lambda text: model.encode(text).tolist()
    )
    
    df = df.drop(columns=["search_text"])

    return df


if __name__ == "__main__":

    df = clean_embedding(IN_PATH)
#==========Write csv==========
    df.to_csv(OUT_PATH, header=False, index=False)
