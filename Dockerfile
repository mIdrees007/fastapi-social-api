# Use Python 3.9.7 as the base image for the application
FROM python:3.12-slim

# Set the working directory inside the Docker container
WORKDIR /usr/src/app

# Copy the Python dependency file into the container
COPY requirements.txt ./

# Install all required Python packages without caching downloaded files
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application source code into the container
COPY . .

# Start the FastAPI application using Uvicorn on port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]