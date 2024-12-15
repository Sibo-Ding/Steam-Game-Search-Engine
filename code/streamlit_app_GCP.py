import streamlit as st
import requests

# Define the FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000/search/"

# Streamlit interface for user input
st.title("Steam Games Search Engine")

search_input = st.text_input("Search Input")
similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.1)
num_matches = st.slider("Number of Matches", 1, 20, 10)
min_price = st.number_input("Minimum Price", 0, 1000, 0)
max_price = st.number_input("Maximum Price", 0, 1000, 100)

if st.button("Search"):
    if search_input:
        payload = {
            "search_input": search_input,
            "similarity_threshold": similarity_threshold,
            "num_matches": num_matches,
            "min_price": min_price,
            "max_price": max_price,
        }

        # Send the request to the FastAPI backend
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            results = response.json()
            for result in results:
                st.write(f"**{result['name']}**")
                st.write(f"Description: {result['description']}")
                st.write(f"Original Price: ${result['original_price']}")
                st.write("---")
        else:
            st.error("Did not find any results. Adjust the query parameters.")
    else:
        st.warning("Please enter a search query.")
