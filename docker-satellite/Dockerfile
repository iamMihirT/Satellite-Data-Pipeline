
FROM python:3.8


WORKDIR /app

COPY . /app


RUN pip install pandas geopy geopandas shapely sentinelhub-py geocoder numpy spacy dateutilparser


RUN python -m spacy download en_core_web_sm



# Run your script when the container launches
CMD ["python", "your_script.py"]
