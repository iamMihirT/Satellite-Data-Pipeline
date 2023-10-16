#!/usr/bin/env python
# coding: utf-8

# In[13]:


import requests
import pandas as pd
import json
import logging


# In[24]:


logging.basicConfig(filename='twtscrape.log', level=logging.DEBUG)


# In[22]:


try:
    payload = {
        'api_key': '9ed28736eca09e2034823537c7448a35',
        'query': 'wildfire',
        'num': '100',
        'date_range_start' : '2023-08-20',
        'date_range_end' : '2023-09-20'
}
    response = requests.get(
        'https://api.scraperapi.com/structured/twitter/search', params=payload)

    data = json.loads(response.text)

    output = json.dumps(data, indent=4)

except Exception as e:
    logging.error("API expired or account reached its maximum request limit")


# In[23]:


print(output)


# In[ ]:





# In[5]:


data = json.loads(response.text)

tweets = data['organic_results']

for tweet in tweets:
    print(tweet['title'])
    print(tweet['snippet'])
    print(tweet['link'])


# In[11]:


twitter_data = []
for tweet in tweets:
    twitter_data.append({
        'Title' : tweet["title"],
        'Tweet' : tweet["snippet"],
        'URL' : tweet["link"]
    })


# In[7]:





# In[ ]:





# In[12]:


df = pd.DataFrame(twitter_data)
df.to_json('scraped_tweets10.json', orient = 'index')
print('Export Successful')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




