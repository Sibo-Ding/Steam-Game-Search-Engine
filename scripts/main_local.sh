#!/bin/bash
cd code

python fastapi_app.py &
sleep 5
streamlit run streamlit_app.py