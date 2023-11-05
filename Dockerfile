FROM python:3.10

WORKDIR /twitter_api_scrape

COPY . /twitter_api_scrape

RUN pip install -r requirements.txt

RUN mkdir -p downloaded_media/tweet && mkdir -p downloaded_media/link


CMD ["sleep", "infinity"]
