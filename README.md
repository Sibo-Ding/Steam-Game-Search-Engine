# eco395m-final-project

## Intuition of vector search
Imagine you are in a grocery store. You want to find a fruit that is most similar to a certain orange. But how do you compare an apple to an orange?

First, you convert the fruits into numbers: a lemon is represented by 1, an orange by 2, and a watermelon by 10. These numbers could represent attributes such as size, price, etc. Next, you decide to use the difference between these numbers as a proxy for the difference between the fruits. This way, compared to the lemon, the watermelon is more different from the orange. In other words, the lemon is more similar to the orange.

In our context, fruits represent the games in our database, and the orange represents users' search input. We use a [sentence transformer](https://sbert.net) (or use [LangChain](https://python.langchain.com/docs) if you like) to convert them into vectors (i.e. lists of numbers) and use [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity) to measure the similarities between these vectors. Finally, we find the games most similar to users' search input.

## Intuition of API
An API (Application Programming Interface) is like a factory, or a math function. A factory takes specific inputs ($x$) and produces predictable outputs ($y$)—all without requiring people to understand the internal workings of the factory.  

Similarly, an API takes a request, processes it according to predefined rules, and sends a response. In our context, the API takes a user's search input and returns the most similar games.

## Datebase setup
1. Create a PostgreSQL database instance in GCP SQL.
2. Create a database called `steam` in GCP SQL in the "Databases" tab.
3. Create a `.env` file at the top of the repo saving database credentials, following the format in [demo.env](demo.env). You can use the default username `postgres` and the password you set. Your host can be found in GCP SQL on the "Overview" tab. The port will be the default Postgres port: `5432`. Connect with database as `steam`.

## Setup
1. Install packages in [requirements.txt](requirements.txt).
2. Download data from [Kaggle](https://www.kaggle.com/datasets/nikatomashvili/steam-games-dataset), save as [data/steam_data.csv](data/steam_data.csv).
3. Create a SQL table by running [create_table.py](setup/create_table.py).
4. Clean data and use sentence transformer to create a column with vector embeddings by running [clean_embedding_local.py](setup/clean_embedding_local.py) for about 1.5 hours on my computer, output `data/steam_clean_no_header.csv`.
    - Loading `sentence_transformers` package locally requires `numpy.__version__` < 2 and `keras.__version__` < 3.
    - Alternatively, run [clean_embedding_GCP_Vertex.ipynb](setup/clean_embedding_GCP_Vertex.ipynb) on GCP Vertex AI for about 1.5 hours; run [clean_embedding_Google_Drive.ipynb](setup/clean_embedding_Google_Drive.ipynb) on Google Drive for about 3.5 hours. Detailed instructions about loading data are in those files.
5. Upload `steam_clean_no_header.csv` into GCP bucket. Load it into `steam` table with the "Import" option in GCP SQL instance's console.
6. Create vector indexes by running [create_vector_indexes.py](setup/create_vector_indexes.py).

Steps 3 to 6 can be combined and automated by running [combined_setup.py](setup/combined_setup.py). However, this is not recommended because it is hard to debug.  

## Vector search
In [vector_search.py](code/vector_search.py), modify search criteria and run.  
You can add more search criteria to this code, by doing:
- Add filter criteria `AND column_you_choose = $6` after the `results` query; add parameters to `results`.
- Assign values to parameters at the top of the program.

## FastAPI
1. Start API server by running [main.py](code/main.py).
2. Open Swagger UI on a browser by navigating to [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) or [http://localhost:8080/docs](http://localhost:8080/docs).
3. Submit the request:
    - Find the endpoint (`/search/`) in the Swagger UI.
    - Click **Try it out**.
    - Modify the JSON request.

## Docker
1. Install Docker Desktop for [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/), [MacOS](https://docs.docker.com/docker-for-mac/install/), or [Windows](https://docs.docker.com/docker-for-windows/install/). Windows users may need to connect Docker Desktop to WSL.
2. Build a Docker image: In your terminal (or Docker Desktop terminal), change the working directory to this repo, run `docker build -t <your-image-name> .`. From now on, replace `<your-image-name>` by the image name you set.
3. Run a Docker container: Run `docker run -p 8080:8080 <your-image-name>`.
4. Same as [FastAPI](#fastapi) step 2.
5. Same as [FastAPI](#fastapi) step 3.

## Deploy Docker on GCP
1. Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) and authenticate (follow the instructions on the website). Authenticate Docker by running `gcloud auth configure-docker` in your terminal.
2. For M1/M2 Mac users, redo [Docker](#docker) step 2 by running `docker buildx build --platform linux/amd64 -t <your-image-name> .`, because Google Cloud Run does not support arm64. You can use a new image name to distinguish the local one.
3. Push the Docker image to Google Cloud Registry by running `docker tag <your-image-name> gcr.io/<your-project-id>/<your-image-name>` and `docker push gcr.io/<your-project-id>/<your-image-name>`. From now on, replace `<your-project-id>` by your GCP project ID.
4. Deploy the image on GCP: run `gcloud run deploy <your-service-name> --image gcr.io/<your-project-id>/<your-image-name> --platform managed --memory=2Gi`. Replace `<your-service-name>` by the service name you set. You will be prompted for region and to **allow unauthenticated invocations**: respond `y` if you want public access, and `n` to limit IP access to resources in the same google project.
5. Wait a few moments until the deployment is complete. On success, the command line displays the service URL.
6. Similar to [FastAPI](#fastapi) step 2, take the sercive URL and add `/docs` after it.
7. Same as [FastAPI](#fastapi) step 3.

Reference: [Deploy a Dockerized FastAPI App to Google Cloud Platform](https://towardsdatascience.com/deploy-a-dockerized-fastapi-app-to-google-cloud-platform-24f72266c7ef?sk=11195a53615912077030568c8fe81b68) by Edward Krueger and Douglas Franklin.

## Notes
1. When cleaning "Release Date", if a date is not in "Jan 1, 2000" format, set it to NaT/NaN. This includes "Apr 2019", "Apr-2019", "Coming soon", etc.
2. Game name has non-English (e.g. French), non-alphabetical (e.g. Chinese), and non-character (e.g. emoji) words.

## Remember to format code (black)
## Remember to update requirements.txt