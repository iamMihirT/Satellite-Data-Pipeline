import subprocess
import time
import os
from dotenv import load_dotenv
from datetime import datetime
from telegram_scraper import scrape
from fastapi import FastAPI
from pydantic import BaseModel


load_dotenv()


API_KEY = os.getenv("API_KEY")


app = FastAPI()

class TwitterScrapeRequest(BaseModel):
    query: str = "wildfire"

@app.put("/twitter/scrape")
async def scrape_twitter(request: TwitterScrapeRequest):
    datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    outfile = f"data_twitter_{request.channel}_{datetime}.csv"

    print(f"{datetime} - Starting scraping {outfile}")
    start_time = time.time()
    # This should be a background task
    await scrape(request.channel, outfile)
    print(f"{datetime} - Scraping completed in {time.time() - start_time} seconds")

    return {"data": "Scraping completed"}

def server() -> None:
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{HOST}", "--port", f"{PORT}"]
    subprocess.call(cmd)