import requests
import tweepy
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import os
import time

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

bot = Bot(token=BOT_TOKEN)

# Tweepy Client
client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)

# Function to fetch latest tweets from Fabrizio Romano
async def get_fabrizio_romano_tweets():
    query = "from:FabrizioRomano"
    
    try:
        # Removed 'await' because search_recent_tweets() is NOT async
        tweets = client.search_recent_tweets(query=query, tweet_fields=["id", "text"], max_results=10)

        if tweets and tweets.data:
            fabrizio_news = [
                f"⚡ Fabrizio Romano: {tweet.text}\n🔗 https://twitter.com/FabrizioRomano/status/{tweet.id}\n"
                for tweet in tweets.data
            ]
            return "\n".join(fabrizio_news)

        return "No new tweets from Fabrizio Romano."
    
    except tweepy.TooManyRequests:
        print("Rate limit exceeded. Waiting 15 minutes before retrying...")
        await asyncio.sleep(900)  # Wait 15 minutes before retrying
        return await get_fabrizio_romano_tweets()
    
    except tweepy.BadRequest as e:
        print(f"Bad Request Error: {e}")
        return ""

# Function to get news headlines
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

# Function to send news updates to Telegram
async def send_news():
    news = get_latest_news()
    fabrizio_updates = await get_fabrizio_romano_tweets()

    message = f"{news}\n\n{fabrizio_updates}" if fabrizio_updates else news
    if message:
        await bot.send_message(chat_id=CHANNEL_ID, text=message, disable_web_page_preview=True)

# Main loop to send news every 5 minutes
async def main():
    while True:
        await send_news()
        await asyncio.sleep(300)  # 5 minutes

# Run the bot
asyncio.run(main())
