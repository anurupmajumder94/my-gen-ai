from tavily import TavilyClient
from dotenv import dotenv_values
import os
config = dotenv_values(".env")

def search_internet(query):
    client = TavilyClient(api_key=config["TAVILY_API_KEY"])
    response = client.search(
        query = query,
        search_depth="advanced",       # "basic" | "advanced"
        topic="news",                  # boosts recent/news results
        max_age_days=14,               # recency window
        max_results=5,                 # number of sources to return
        include_answer=True,
        include_images=False,
        include_raw_content=False,
        include_domains=["reuters.com", "economictimes.indiatimes.com"],
        exclude_domains=[]
    )
    return response

response = search_internet("Latest EV policies in India")
print(f'Title: {response['results'][0]['title']}')
print(f'Content: {response['results'][0]['content']}')