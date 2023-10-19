from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
from sentinelhub import BBox, CRS, DataCollection, MimeType, SentinelHubRequest, SHConfig, bbox_to_dimensions
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

def process_data():
    import pandas as pd
    from dateutil import parser
    import spacy
    import re
    from geopy.geocoders import Nominatim
    from sentinelhub import SHConfig   
    from utils import plot_image

    # Your data processing code
    logging.basicConfig(level=logging.DEBUG)
    logging.captureWarnings(True)

    df = pd.read_json("C:/Users/Mihir Trivedi/Desktop/final code/data2_climate.json")
    nlp = spacy.load("en_core_web_sm")

    def extract_country(location):
        doc = nlp(location)
        potential_countries = []
        for ent in doc.ents:
            if ent.label_ == "GPE":
                potential_countries.append(ent.text)

        if potential_countries:
            return potential_countries[0]
        return None

    def extract_date(date_str):
        date_pattern = (
            r'\d{1,4}[-/]\d{1,2}[-/]\d{1,4}' |
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b \d{1,2}, \d{4}' |
            r'\d{1,2}\.\d{1,2}\.\d{4}'
        )
        match = re.search(date_pattern, date_str)

        if match:
            extracted_date = match.group()
            return extracted_date
        return None

    df['Extracted Country'] = df['extracted.location'].apply(extract_country)
    df['Extracted Date'] = df['extracted.date'].apply(extract_date)

    def get_bounding_box(place_name):
        geolocator = Nominatim(user_agent="place_boundary")
        location = geolocator.geocode(place_name)
        if location:
            lat, lon = location.latitude, location.longitude
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

    config = SHConfig()
    config.sh_client_id = "35c2e8f8-8796-450a-9770-f4e481949986"
    config.sh_client_secret = "Y*X?HpB9W4N&#lWKt!1CQL3cj-)r(6M{n}Nuj6QD"
    config.save()

    resolution = 60
    coords_list = []
    coords_size_list = []

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

            coords_list.append((min_lon, min_lat, max_lon, max_lat))
            coords_size_list.append(coords_size)
        else:
            coords_list.append(())
            coords_size_list.append(None)

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
                };
            }
        }

        function evaluatePixel(sample) {
            return [sample.B04, sample.B03, sample.B02];
        }
    """

    for index, row in df2.iterrows():
        coords = row['coords']
        coords_size = row['coords_size']

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
                config=config
            )
            true_color_imgs = request_true_color.get_data()

            image = true_color_imgs[0]
            print(f"Image type: {image.dtype}")
            plot_image(image, factor=3.5 / 255, clip_range=(0, 1))

    result = {"message": "Data processing completed."}
    return result

class QueryModel(BaseModel):
    latitude: float
    longitude: float

class DataSourceModel(BaseModel):
    source: str
    q: QueryModel

class PipelineRequestModel(BaseModel):
    name: str
    data_sources: list[DataSourceModel]

@app.put("/pipeline")
async def process_pipeline(request_data: PipelineRequestModel):
    name = request_data.name
    data_sources = request_data.data_sources

    # You can process the data_sources as needed here
    results = []

    for source in data_sources:
        source_name = source.source
        query = source.q
        latitude = query.latitude
        longitude = query.longitude

        # Perform actions based on the source and query parameters
        # For example, you can store or use the 'source_name', 'latitude', and 'longitude' as required

        # Append results for each source to the results list
        results.append({"source": source_name, "latitude": latitude, "longitude": longitude})

    response_data = {"message": "Pipeline processing completed for " + name, "results": results}
    return JSONResponse(content=response_data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
