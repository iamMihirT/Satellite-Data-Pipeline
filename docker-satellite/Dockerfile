# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire current directory into the container at /app
COPY . /app

# Install the required packages using pip
RUN pip install pandas spacy geopy geopandas sentinelhub-py numpy matplotlib

# Run your Python script when the container launches
CMD ["python", "your_script_name.py"]
