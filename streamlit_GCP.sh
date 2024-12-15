#!/bin/bash
cd code

uvicorn fastapi_app:app --host 0.0.0.0 --port 8000 &
sleep 15
streamlit run streamlit_app_GCP.py --server.address=0.0.0.0 --server.port=8080