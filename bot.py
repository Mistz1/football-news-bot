import requests
from bs4 import BeautifulSoup
from telegram import Bot
import tweepy
import asyncio
import os

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

bot = Bot(token=BOT_TOKEN)

# Twitter authentication
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

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
            headlines.append(f"\U0001F4F0 {site}: {title}\n\U0001F517 {link}\n")
    return "\n".join(headlines[:10])

# Function to get Fabrizio Romano's latest tweets
def get_fabrizio_romano_tweets():
    tweets = client.search_recent_tweets(query="from:FabrizioRomano", tweet_fields=["id", "text"], max_results=5)
    fabrizio_news = []
    if tweets.data:
        for tweet in tweets.data:
            fabrizio_news.append(f"⚡ Fabrizio Romano: {tweet.text}\n🔗 https://twitter.com/FabrizioRomano/status/{tweet.id}\n")
    return "\n".join(fabrizio_news)

# Function to send news to Telegram channel
async def send_news():
    news = get_latest_news()
    fabrizio_updates = get_fabrizio_romano_tweets()
    message = f"{news}\n\n{fabrizio_updates}" if fabrizio_updates else news
    if message:
        await bot.send_message(chat_id=CHANNEL_ID, text=message, disable_web_page_preview=True)

# Run every 5 minutes
async def main():
    while True:
        await send_news()
        await asyncio.sleep(300)  # 300 seconds = 5 minutes

if __name__ == "__main__":
    asyncio.run(main())
