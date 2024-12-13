import os
import subprocess
import time
import streamlit.web.cli

def run_fastapi():
    """Runs the FastAPI backend."""
    subprocess.Popen(["python", "fastapi_app.py"])

def run_streamlit():
    """Runs the Streamlit frontend."""
    streamlit.web.cli.main(["run", "streamlit_app.py"])

if __name__ == "__main__":

    # Change working directory to the current .py file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_directory)

    run_fastapi()

    time.sleep(10)  # Wait for FastAPI to start up

    run_streamlit()
