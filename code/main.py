import os
import subprocess
import time
import streamlit.web.cli

# Change working directory to the current .py file
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

# Run the FastAPI backend
subprocess.Popen(["python3", "fastapi_app.py"])

time.sleep(5)  # Wait for FastAPI to start up

# uns the Streamlit frontend
streamlit.web.cli.main(["run", "streamlit_app.py"])
