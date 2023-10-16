FROM python:3.8

WORKDIR /twitter_api_scrape

RUN pip install requests pandas

COPY . /twitter_api_scrape

CMD ["python", "your_script.py"]
