import requests
import pandas as pd
import json
import logging
from decouple import config

# Load API key from .env file
api_key = config('API_KEY')

logging.basicConfig(filename='twtscrape.log', level=logging.DEBUG)

try:
    payload = {
        'api_key': api_key,
        'query': 'wildfire',
        'num': '100',
        'date_range_start': '2023-08-20',
        'date_range_end': '2023-09-20'
    }
    response = requests.get('https://api.scraperapi.com/structured/twitter/search', params=payload)

    data = json.loads(response.text)

    output = json.dumps(data, indent=4)

except Exception as e:
    logging.error("API expired or account reached its maximum request limit")

print(output)

data = json.loads(response.text)

tweets = data['organic_results']

for tweet in tweets:
    print(tweet['title'])
    print(tweet['snippet'])
    print(tweet['link'])

twitter_data = []
for tweet in tweets:
    twitter_data.append({
        'Title': tweet["title"],
        'Tweet': tweet["snippet"],
        'URL': tweet["link"]
    })

df = pd.DataFrame(twitter_data)
df.to_json('scraped_tweets10.json', orient='index')
print('Export Successful')
