### Build Image
```bash
docker build -t mpi-telegram-scraper .
```

### Run Container
```bash
docker run --rm \
    --name mpi-telegram-scraper \
    -v sda-telgram-scraper.session:/telegram_scrapper/ \
    -e API_ID=27268549 \
    -e API_HASH=d390faee1fe7f79fe0b081324a343356 \
    -e PHONE=+919724111939 \
    -e USERNAME=ptah112  \
    mpi-telegram-scraper
```
