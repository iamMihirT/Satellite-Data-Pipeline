FROM python:3.8

WORKDIR /telegram_scrapper

RUN pip install telethon pandas nest_asyncio

COPY . /telegram_scrapper


ENV API_ID=27268549
ENV API_HASH=d390faee1fe7f79fe0b081324a343356
ENV PHONE=+919724111939
ENV USERNAME=ptah112
ENV SESSION_STRING=1BVtsOL0Bu4066f26k8Algbf3njrb3lBVepp90PB6po8kyEa6bTEeelC32RboyA0kt_CVvX79FmFtWQDeSXKHCexi-6GryZfVDAg6PXeHLe6UivAkReHJtO8AtBCWAblgW42MeyIhkpy3YUh0hyKaIa1tYI0z2IlfF5rzEGQ9VpwOMe0QqKbM3OUMyPnKs8Z1LELwRpGGUocQjV-z1TlQBsDxe1z18OgyqQmgbPI8fXyX0lmZ3q8baNcmH6MoBWJ51qo_-IPFHRwbDNAEISpIpABh5OHCJoP22yJwjAaVqe5qivCPQCdfV-tGFrhR4c57wvi4ukVLVJREd-uef7PLKqHlEdREg1g=

CMD ["python", "telegram_scrapper.py"]
