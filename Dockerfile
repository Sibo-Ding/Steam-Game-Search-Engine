FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy necessary files into the container
COPY requirements.txt /app
COPY .env /app
COPY main_local.sh /app
COPY code /app/code

# Install the dependencies
RUN pip install -r requirements.txt

# Give execute permissions
RUN chmod +x main_local.sh

# Make ports available to the world outside this container
# FastAPI (8080) and Streamlit (8501)
EXPOSE 8080
EXPOSE 8501

# Run Shell startup script
CMD ["/app/main_local.sh"]
