#!/usr/bin/env python
# coding: utf-8



import pandas as pd
from dateutil import parser
import spacy
import re
from geopy.geocoders import Nominatim
import geopandas as gpd
from shapely.geometry import Point
import json
import logging
from sentinelhub import SHConfig   
import datetime
import os

import matplotlib.pyplot as plt
import numpy as np

from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
)
from utils import plot_image


logging.basicConfig(level=logging.DEBUG)
logging.captureWarnings(True)



df = pd.read_json("data2_climate.json")
nlp = spacy.load("en_core_web_sm")



def extract_country(location):
    # Process the location string with spaCy
    doc = nlp(location)

    # Initialize a list to store potential country names
    potential_countries = []

    # Iterate through entities in the processed text
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Check if the entity is a geopolitical entity (which can include countries)
            potential_countries.append(ent.text)

    # If there are potential countries, return the first one found
    if potential_countries:
        return potential_countries[0]

    # If no country names were found, return None
    return None

# Function to extract date from date column
def extract_date(date_str):
    # Define a regex pattern to match dates in various formats
    date_pattern = (
        r'\d{1,4}[-/]\d{1,2}[-/]\d{1,4}'  # Matches YYYY-MM-DD, YYYY/MM/DD
        r'|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b \d{1,2}, \d{4}'  # Matches Month Day, YYYY
        r'|\d{1,2}\.\d{1,2}\.\d{4}'  # Matches day.month.year
    )

    # Search for the date pattern in the input text
    match = re.search(date_pattern, date_str)

    if match:
        # Extract the matched date string
        extracted_date = match.group()

        # You can further process the extracted_date if needed, e.g., parsing it with dateutil.parser
        return extracted_date

    return None

# Create new columns with extracted information
df['Extracted Country'] = df['extracted.location'].apply(extract_country)
df['Extracted Date'] = df['extracted.date'].apply(extract_date)

def get_bounding_box(place_name):
    geolocator = Nominatim(user_agent="place_boundary")
    location = geolocator.geocode(place_name)
    
    if location:
        # Get latitude and longitude
        lat, lon = location.latitude, location.longitude
        
        # Define a bounding box around the location (adjust the size as needed)
        bounding_box = {
            'min_latitude': lat - 0.4,
            'max_latitude': lat + 0.45,
            'min_longitude': lon - 0.4,
            'max_longitude': lon + 0.45
        }
        
        return bounding_box
    else:
        return None



df['bounding_box'] = df['Extracted Country'].apply(get_bounding_box)


from sentinelhub import SHConfig   
config = SHConfig()
config.sh_client_id = "35c2e8f8-8796-450a-9770-f4e481949986"
config.sh_client_secret = "Y*X?HpB9W4N&#lWKt!1CQL3cj-)r(6M{n}Nuj6QD"

config.save()

config = SHConfig()

if not config.sh_client_id or not config.sh_client_secret:
    print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")




resolution = 60
coords_list = []  # List to store the calculated coordinates
coords_size_list = []  # List to store the calculated sizes

for index, row in df.iterrows():
    bounding_box_dict = row['bounding_box']

    if bounding_box_dict is not None:
        min_lat = bounding_box_dict['min_latitude']
        max_lat = bounding_box_dict['max_latitude']
        min_lon = bounding_box_dict['min_longitude']
        max_lon = bounding_box_dict['max_longitude']

        coords_wgs84 = (min_lon, min_lat, max_lon, max_lat)
        coords_bbox = BBox(bbox=coords_wgs84, crs=CRS.WGS84)
        coords_size = bbox_to_dimensions(coords_bbox, resolution=resolution)

        # Append the values directly without naming them
        coords_list.append((min_lon, min_lat, max_lon, max_lat))
        coords_size_list.append(coords_size)
    else:
        # Append an empty tuple and None for coords_size if 'bounding_box' is None
        coords_list.append(())
        coords_size_list.append(None)

# Create a new DataFrame with 'coords' and 'coords_size' columns
df2 = pd.DataFrame({
    'coords': coords_list,
    'coords_size': coords_size_list
})







evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
"""

for index, row in df2.iterrows():
    coords = row['coords']
    coords_size = row['coords_size']

    # Check if coords is not an empty tuple
    if coords:
        min_lon, min_lat, max_lon, max_lat = coords

        coords_bbox = BBox((min_lon, min_lat, max_lon, max_lat), crs=CRS.WGS84)

        request_true_color = SentinelHubRequest(
            evalscript=evalscript_true_color,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L1C,
                    time_interval=("2022-10-09", "2022-10-09"),
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
            bbox=coords_bbox,
            size=coords_size,
            config=config,  # Use your config object
        )
        true_color_imgs = request_true_color.get_data()

        image = true_color_imgs[0]
        print(f"Image type: {image.dtype}")
        plot_image(image, factor=3.5 / 255, clip_range=(0, 1))


    else:
        # Handle the case where coords is an empty tuple
        pass







print(f"Returned data is of type = {type(true_color_imgs)} and length {len(true_color_imgs)}.")
print(f"Single element in the list is of type {type(true_color_imgs[-1])} and has shape {true_color_imgs[-1].shape}")






