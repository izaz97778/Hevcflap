# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port for FastAPI (Uvicorn default is 8000, but we'll use 8080 for Koyeb)
EXPOSE 8080

# Start the FastAPI app using uvicorn
CMD ["bash", "start.sh"]
