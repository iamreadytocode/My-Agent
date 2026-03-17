
from langchain_core.tools import tool
import requests
import os


NEWS_API = "https://newsapi.org/v2/top-headlines"
API_KEY = os.getenv("NEWS_API_KEY")


@tool
def fetch_daily_news():
    """Fetch the top 3 daily news headlines."""
    response = requests.get(
        NEWS_API,
        params={
            "apiKey": API_KEY,
            "language": "en"
        }
    )

    data = response.json()
    headlines = [a["title"] for a in data.get("articles", [])[:5]]

    return headlines


@tool
def deep_dive_news(topic: str):
    """Provide a detailed explanation about a news topic."""
    return f"Detailed explanation about {topic}."
