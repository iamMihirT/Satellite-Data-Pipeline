import asyncio
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

async def generate_session(api_id, api_hash):
    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        session_string = client.session.save()
        return session_string

api_id = 27268549  # Replace with your API ID
api_hash = 'd390faee1fe7f79fe0b081324a343356'  # Replace with your API hash

session_string = asyncio.run(generate_session(api_id, api_hash))
print(session_string)
