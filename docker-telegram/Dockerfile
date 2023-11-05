FROM python:3.10

WORKDIR /telegram_scrapper
COPY . /telegram_scrapper
RUN pip install -r requirements.txt
RUN mkdir -p  downloaded_media/photos downloaded_media/videos

CMD ["sleep", "infinity"]
