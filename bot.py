import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import os

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)
sent_news = set()  # Store already sent news to avoid duplicates

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
            articles = soup.select("h2 a")[:10]  # Get top 10 news
        elif "bbc" in url or "guardian" in url:
            articles = soup.select("h3 a")[:10]
        elif "skysports" in url or "espn" in url:
            articles = soup.select("h4 a")[:10]

        for article in articles:
            title = article.get_text().strip()
            link = article["href"]
            if not link.startswith("http"):
                link = url + link
            headlines.append(f"📰 {site}: {title}\n🔗 {link}\n")

    return headlines

# Function to send news updates to Telegram
async def send_news():
    global sent_news
    news_list = get_latest_news()

    new_news = [news for news in news_list if news not in sent_news]  # Filter new news

    if new_news:
        for news in new_news:
            await bot.send_message(chat_id=CHANNEL_ID, text=news, disable_web_page_preview=True)
            sent_news.add(news)  # Mark news as sent

# Main loop to send news every 5 minutes
async def main():
    while True:
        await send_news()
        await asyncio.sleep(300)  # 5 minutes

# Run the bot
asyncio.run(main())