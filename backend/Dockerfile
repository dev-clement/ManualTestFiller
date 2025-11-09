# Use a lightweight official python image
FROM python:3.11-slim

# Prevents python from writing .pyc files and buffering logs at the same time
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFERRED=1

# Set environment to production
ENV FLASK_ENV=prod

# Create an set the working dirrectory
WORKDIR /app

# Create a logs folder
RUN mkdir -p /app/logs

# Install system dependencies 
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc &&\
    rm -rf /var/lib/apt/lists/*

# Copy the requirements and install the dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the FLASK app code
COPY . .

# Expose the Flask default port
EXPOSE 5000

# Default command to run the Flask app
# (assuming your entrypoint is run.py)
CMD ["python", "run.py"]