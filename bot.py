import requests
from bs4 import BeautifulSoup
from telegram import Bot
import snscrape.modules.twitter
import time
import os

# Telegram Bot Token (from Railway environment variable)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Use your channel username or ID

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

# Function to get Fabrizio Romano's latest tweets
def get_fabrizio_romano_tweets():
    query = "from:FabrizioRomano football"
    tweets = sntwitter.TwitterSearchScraper(query).get_items()

    fabrizio_news = []
    for i, tweet in enumerate(tweets):
        if i >= 5:
            break
        fabrizio_news.append(f"⚡ Fabrizio Romano: {tweet.content}\n🔗 https://twitter.com/FabrizioRomano/status/{tweet.id}\n")

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
