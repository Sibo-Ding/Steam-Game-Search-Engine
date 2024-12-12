FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy necessary files into the container
COPY requirements.txt /app
COPY .env /app
COPY code /app

# Install the dependencies
RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the FastAPI app using uvicorn (entry point)
CMD ["uvicorn", "main:app", "--timeout-keep-alive", "0", "--host", "0.0.0.0", "--port", "8080"]
