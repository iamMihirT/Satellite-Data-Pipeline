# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages using pip
RUN pip install fastapi uvicorn pandas geopy requests numpy \
    spacy scikit-learn matplotlib seaborn \
    sentence-transformers==2.0.0.post3 \
    sentinelhub-py==3.2.0

# Define environment variables
ENV SH_CLIENT_ID "35c2e8f8-8796-450a-9770-f4e481949986"
ENV SH_CLIENT_SECRET "Y*X?HpB9W4N&#lWKt!1CQL3cj-)r(6M{n}Nuj6QD"

# Make port 80 available to the world outside this container
EXPOSE 80

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
