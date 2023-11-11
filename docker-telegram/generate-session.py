import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

async def generate_session(api_id, api_hash):
    async with TelegramClient("sda-telegram-scraper", api_id, api_hash) as client:
        session_string = client.session.save()
        return session_string

async def main():
    await generate_session(API_ID, API_HASH)

# Run the asynchronous code
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
