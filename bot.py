import requests
import json
import time
import os
from bs4 import BeautifulSoup
from telegram import Bot

# Telegram Bot Token & Channel ID from Railway environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Twitter API credentials
CLIENT_ID = os.getenv("TWITTER_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITTER_CLIENT_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

bot = Bot(token=BOT_TOKEN)

# Function to scrape news
def get_latest_news():
    urls = {
        "Marca": "https://www.marca.com/en/",
        "AS": "https://en.as.com/",
        "Mundo Deportivo": "https://www.mundodeportivo.com/",
        "BBC Sport": "https://www.bbc.com/sport",
        "Sky Sports": "https://www.skysports.com/",
        "The Guardian": "https://www.theguardian.com/football",
        "ESPN": "https://www.espn.com/soccer/"
    }
    headlines = []
    for site, url in urls.items():
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        if "marca" in url or "as" in url or "mundodeportivo" in url:
            articles = soup.select("h2 a")[:5]
        elif "bbc" in url or "guardian" in url:
            articles = soup.select("h3 a")[:5]
        elif "skysports" in url or "espn" in url:
            articles = soup.select("h4 a")[:5]
        for article in articles:
            title = article.get_text().strip()
            link = article["href"]
            if not link.startswith("http"):
                link = url + link
            headlines.append(f"📰 {site}: {title}\n🔗 {link}\n")
    return "\n".join(headlines[:10])

# Function to fetch latest tweets from Fabrizio Romano using OAuth 2.0
def get_fabrizio_romano_tweets():
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    url = "https://api.twitter.com/2/users/by/username/FabrizioRomano"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "⚠️ Failed to fetch Twitter user info"
    user_id = response.json().get("data", {}).get("id")
    if not user_id:
        return "⚠️ Failed to get user ID"
    tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results=5"
    tweets_response = requests.get(tweets_url, headers=headers)
    if tweets_response.status_code != 200:
        return "⚠️ Failed to fetch tweets"
    tweets = tweets_response.json().get("data", [])
    fabrizio_news = [f"⚡ Fabrizio Romano: {tweet['text']}\n🔗 https://twitter.com/FabrizioRomano/status/{tweet['id']}\n" for tweet in tweets]
    return "\n".join(fabrizio_news)

# Function to send news to Telegram channel
def send_news():
    news = get_latest_news()
    fabrizio_updates = get_fabrizio_romano_tweets()
    message = f"{news}\n\n{fabrizio_updates}" if fabrizio_updates else news
    if message:
        bot.send_message(chat_id=CHANNEL_ID, text=message, disable_web_page_preview=True)

# Run every 5 minutes
while True:
    send_news()
    time.sleep(300)  # 300 seconds = 5 minutes
