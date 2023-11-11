### Build Image
```bash
docker build -t mpi-telegram-scraper .
```

### Run Container
```bash
docker run --rm \
    --name mpi-telegram-scraper \
    -v $(pwd)/sda-telgram-scraper.session:/telegram_scaper/sda-telegram-scraper.session:ro \
    -e API_ID=25490965 \
    -e API_HASH=48bd72d57fb01b87965eb14d87c0f453 \
    -e PHONE=+16174305353 \
    -e USERNAME=mpisda  \
    -e HOSTNAME=localhost \
    -e PORT=8080 \
    -p 8080:8080 \
    mpi-telegram-scraper
```
