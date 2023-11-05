FROM python:3.10

WORKDIR /telegram_scraper
COPY . /telegram_scraper
RUN pip install -r requirements.txt
RUN mkdir -p  downloaded_media/photos downloaded_media/videos

CMD ["sleep", "infinity"]
