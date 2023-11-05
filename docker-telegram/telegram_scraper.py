import os
import pandas as pd
import nest_asyncio
from dotenv import load_dotenv
from telethon.sync import TelegramClient


# Initialize nest_asyncio to run asyncio within Jupyter/IPython
nest_asyncio.apply()


async def scrape(channel_name: str, outfile: str, api_id: str, api_hash: str):
    try:
        async with TelegramClient(
            'sda-telegram-scraper', api_id, api_hash
        ) as client:
            data = []
            async for message in client.iter_messages(f"https://t.me/{channel_name}"):
                print(message.sender_id, ":", message.text, message.date)
                data.append(
                    [
                        message.sender_id,
                        message.text,
                        message.date,
                        message.id,
                        message.post_author,
                        message.views,
                        message.peer_id.channel_id,
                    ]
                )

                # Check if the message has media (photo or video)
                if message.media:
                    if hasattr(message.media, "photo"):
                        # Download photo
                        file_location = await client.download_media(
                            message.media.photo,
                            file=os.path.join("downloaded_media", "photos"),
                        )
                        print(f"Downloaded photo: {file_location}")
                    elif hasattr(message.media, "document"):
                        # Download video (or other documents)
                        file_location = await client.download_media(
                            message.media.document,
                            file=os.path.join("downloaded_media", "videos"),
                        )
                        print(f"Downloaded video: {file_location}")

            # Save the data to a CSV file
            df = pd.DataFrame(
                data,
                columns=[
                    "message.sender_id",
                    "message.text",
                    "message.date",
                    "message.id",
                    "message.post_author",
                    "message.views",
                    "message.peer_id.channel_id",
                ],
            )
            df.to_csv(outfile, encoding="utf-8")

    except Exception as e:
        print("Session Timeout")

