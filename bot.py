import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio
import os

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)

# Dictionary to store last sent headlines
last_sent_news = set()

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
        try:
            response = requests.get(url, timeout=10)
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
                headlines.append((title, f"📰 {site}: {title}\n🔗 {link}\n"))

        except Exception as e:
            print(f"Error fetching {site}: {e}")

    return headlines

# Function to send news updates to Telegram
async def send_news():
    global last_sent_news
    news_list = get_latest_news()
    
    # Filter out previously sent news
    new_news = [news for title, news in news_list if title not in last_sent_news]
    
    if new_news:
        message = "\n".join(new_news[:10])  # Limit to 10 news articles per message
        await bot.send_message(chat_id=CHANNEL_ID, text=message, disable_web_page_preview=True)

        # Update sent news tracker
        last_sent_news = set(title for title, _ in news_list)  # Store only titles

# Main loop to send news every 5 minutes
async def main():
    while True:
        await send_news()
        await asyncio.sleep(300)  # 5 minutes

# Run the bot
asyncio.run(main())