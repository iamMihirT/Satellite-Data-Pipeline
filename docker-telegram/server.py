import subprocess
import time
import os
import nest_asyncio
from dotenv import load_dotenv
from datetime import datetime
from telegram_scraper import scrape
from fastapi import FastAPI
from pydantic import BaseModel


load_dotenv()
nest_asyncio.apply()


API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")
USERNAME = os.getenv("USERNAME")
HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "8000")

app = FastAPI()

class TelegramScrapeRequest(BaseModel):
    channel: str = "GCC_report"
    
@app.put("/telegram/scrape")
async def scrape_telegram(request: TelegramScrapeRequest):
    datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    outfile = f"data_telegram_{request.channel}_{datetime}.csv"

    print(f"{datetime} - Starting scraping {outfile}")
    start_time = time.time()
    # This should be a background task
    await scrape(request.channel, outfile)
    print(f"{datetime} - Scraping completed in {time.time() - start_time} seconds")
    
    return {"data": "Scraping completed"}

def server() -> None:
    cmd = ["uvicorn", "main:app", "--reload", "--host", f"{HOST}", "--port", f"{PORT}"]
    subprocess.call(cmd)