import asyncio
import os 
import pandas as pd
import nest_asyncio
from dotenv import load_dotenv
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")
USERNAME = os.getenv("USERNAME")


async def generate_session(api_id, api_hash):
    async with TelegramClient('sda-telgram-scraper', api_id, api_hash) as client:
        session_string = client.session.save()
        return session_string

SESSION_SECRET = asyncio.run(generate_session(API_ID, API_HASH))


# Initialize nest_asyncio to run asyncio within Jupyter/IPython
nest_asyncio.apply()


async def main():
    try:
        async with TelegramClient(StringSession(SESSION_SECRET), API_ID, API_HASH) as client:
            data = []
            async for message in client.iter_messages("https://t.me/GCC_report"):
                print(message.sender_id, ':', message.text, message.date)
                data.append([message.sender_id, message.text, message.date, message.id, message.post_author, message.views, message.peer_id.channel_id])

                # Check if the message has media (photo or video)
                if message.media:
                    if hasattr(message.media, 'photo'):
                        # Download photo
                        file_location = await client.download_media(message.media.photo, file=os.path.join('downloaded_media', 'photos'))
                        print(f"Downloaded photo: {file_location}")
                    elif hasattr(message.media, 'document'):
                        # Download video (or other documents)
                        file_location = await client.download_media(message.media.document, file=os.path.join('downloaded_media', 'videos'))
                        print(f"Downloaded video: {file_location}")

            # Save the data to a CSV file
            df = pd.DataFrame(data, columns=["message.sender_id", "message.text", "message.date", "message.id",  "message.post_author", "message.views", "message.peer_id.channel_id"])
            df.to_csv('data2_climate.csv', encoding='utf-8')

    except Exception as e:
        print("Session Timeout")

# Run the asynchronous code
loop = asyncio.get_event_loop()
loop.run_until_complete(main())





