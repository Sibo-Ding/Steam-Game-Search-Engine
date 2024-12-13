# eco395m-final-project

## Introduction
We use vector search

## Methodology
### Intuition of vector search
Imagine you are in a grocery store trying to find a fruit most similar to an orange. But how to compare an apple to an orange?

First, you assign numerical values to the fruits: a lemon is 1, an orange is 2, and a watermelon is 10. These numbers can represent attributes such as size, price, etc. Next, you use the difference between these numbers as a proxy for the difference between the fruits. This way, compared to a lemon, a watermelon differs more from an orange. In other words, the lemon is more similar to the orange.

In our case, the fruits represent the games in our database, and the orange represents a user's search input. We use a [sentence transformer](https://sbert.net) (or use [LangChain](https://python.langchain.com/docs) if you like) to convert them into vectors (i.e. lists of numbers) and use [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) to measure the similarities between these vectors. Finally, we find the games most similar to the user's search input.

### Intuition of reranking with cross-encoder
After retrieving the initial search results, reranking use a more computationally expensive model to better rank them.  

A cross-encoder is a model used in the reranking process. It considers both the query and each initial search result **together** to evaluate how well they match. Unlike an encoder-decoder model where the query and the initial search result are processed independently, a cross-encoder processes them together in a single pass.

### Intuition of API
An API (Application Programming Interface) is like a factory or a math function. A factory takes specific inputs ($x$) and produces predictable outputs ($y$)—without requiring people to understand the internal workings of the factory.  

Similarly, an API takes a request, processes it according to predefined rules, and returns a response. In our case, the API takes a user's search input and returns the most similar games.

### Intuition of Docker and Deploying on GCP
When you write a program on your computer. Normally, it might not work on someone else's computer because their system could be different (different operating system, different libraries, etc.).  

Docker creates "containers", holding your program and all its dependencies (everything it needs to run like libraries, configurations, etc.) in a consistent way, no matter where it runs. Whether on your computer, a server, or the cloud, the program will always run the same.  

We then deploy Docker on GCP to allow users to access our API publicly.

## Instructions to reproduce
### Datebase setup
1. Create a PostgreSQL database instance in GCP SQL.
2. Create a database called `steam` in GCP SQL in the "Databases" tab.
3. Create a `.env` file at the top of the repo saving database credentials, following the format in [demo.env](demo.env). You can use the default username `postgres` and the password you set. Your host can be found on the GCP SQL "Overview" tab. The default Postgres port is `5432`. Connect to the database `steam`.

### Setup
1. Install packages in [requirements.txt](requirements.txt).
2. Download data from [Kaggle](https://www.kaggle.com/datasets/nikatomashvili/steam-games-dataset), save as [data/steam_data.csv](data/steam_data.csv).
3. Create a SQL table by running [create_table.py](setup/create_table.py).
4. Clean data and use a sentence transformer to create a column with vector embeddings by running [clean_embedding_local.py](setup/clean_embedding_local.py) for about 1.5 hours on my computer (Microsoft Surface Laptop 2), output `data/steam_clean_no_header.csv`.
    - Loading `sentence_transformers` package locally requires `numpy.__version__` < 2 and `keras.__version__` < 3.
    - Alternatively, run [clean_embedding_GCP_Vertex.ipynb](setup/clean_embedding_GCP_Vertex.ipynb) on GCP Vertex AI about 1.5 hours or [clean_embedding_Google_Drive.ipynb](setup/clean_embedding_Google_Drive.ipynb) on Google Drive for about 3.5 hours. Detailed instructions for loading data are in these files.
5. Upload `steam_clean_no_header.csv` into GCP bucket. Load it into `steam` table using the "Import" option in GCP SQL instance's console.
6. Create vector indexes by running [create_vector_indexes.py](setup/create_vector_indexes.py).

Steps 3 to 6 can be combined and automated by running [combined_setup.py](setup/combined_setup.py), but this is not recommended because it is hard to debug.  

### Vector search and rerank with cross-encoder
In [vector_search.py](code/vector_search.py), modify search criteria and run.  
To add more search criteria:
- Add filter conditions like `AND column_you_choose = $6` after the `results` query, and add corresponding parameters to `results`.
- Assign values to parameters at the top of the program.

### FastAPI
1. Start API server by running [fastapi_app.py](code/fastapi_app.py).
2. Open Swagger UI on a browser by navigating to [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) or [http://localhost:8080/docs](http://localhost:8080/docs).
3. Submit the request:
    - Find the endpoint (`/search/`) in the Swagger UI.
    - Click **Try it out**.
    - Modify the JSON request.

### Docker
1. Install Docker Desktop for [Windows](https://docs.docker.com/docker-for-windows/install/), [MacOS](https://docs.docker.com/docker-for-mac/install/), or [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/). Windows users may need to connect Docker Desktop to WSL.
2. Build a Docker image: In your terminal (or Docker Desktop terminal), change the working directory to this repo, run `docker build -t <your-image-name> .`. From now on, replace `<your-image-name>` with the image name you choose.
3. Run a Docker container by running `docker run -p 8080:8080 <your-image-name>`.
4. Same as [FastAPI](#fastapi) step 2.
5. Same as [FastAPI](#fastapi) step 3.

### Deploy Docker on GCP
1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) and authenticate (follow the instructions on the website). Authenticate Docker by running `gcloud auth configure-docker` in your terminal.
2. For M1/M2 Mac users, redo [Docker](#docker) step 2 by running `docker buildx build --platform linux/amd64 -t <your-image-name> .`, because Google Cloud Run does not support arm64. You can use a new image name to distinguish from the local one.
3. Push the Docker image to Google Cloud Registry by running `docker tag <your-image-name> gcr.io/<your-project-id>/<your-image-name>` and `docker push gcr.io/<your-project-id>/<your-image-name>`. From now on, replace `<your-project-id>` with your GCP project ID.
4. Deploy the image on Google Cloud Run by running `gcloud run deploy <your-service-name> --image gcr.io/<your-project-id>/<your-image-name> --platform managed --memory=2Gi`. Replace `<your-service-name>` with the service name you choose. You will be prompted for region and to **allow unauthenticated invocations**: respond `y` if you want public access, and `n` to limit IP access to resources in the same google project.
5. Wait a few moments for the deployment to complete. Once successful, the command line will display the service URL.
6. Similar to [FastAPI](#fastapi) step 2, take the sercive URL and add `/docs` after it.
7. Same as [FastAPI](#fastapi) step 3.

Reference: [Deploy a Dockerized FastAPI App to Google Cloud Platform](https://towardsdatascience.com/deploy-a-dockerized-fastapi-app-to-google-cloud-platform-24f72266c7ef?sk=11195a53615912077030568c8fe81b68) by Edward Krueger and Douglas Franklin.

## Limitations and potential extensions
1. Limited by our computing power, the sentence transformer model `paraphrase-multilingual-MiniLM-L12-v2` we use is quite simple.
2. Scrape [Steam](https://store.steampowered.com/search/?category1=998&ndl=1&ignore_preferences=1) periodically to update the database.

## Notes
1. When cleaning "Release Date", if a date is not in "Jan 1, 2000" format, set it to NaT/NaN. This includes "Apr 2019", "Apr-2019", "Coming soon", etc.
2. Game name has non-English (e.g. French), non-alphabetical (e.g. Chinese), and non-character (e.g. emoji) words.

## Remember to format code (black)
## Remember to update requirements.txt