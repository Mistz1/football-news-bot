import tweepy
import requests
import time
from telegram import Bot

# Twitter API Credentials (Replace with your keys)
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
ACCESS_TOKEN = "your_access_token"
ACCESS_SECRET = "your_access_secret"

# Telegram Bot Token & Channel ID
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHANNEL_ID = "@your_channel"

# Initialize Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def get_fabrizio_romano_tweets():
    """Fetch latest Fabrizio Romano tweets"""
    tweets = api.user_timeline(screen_name="FabrizioRomano", count=5, tweet_mode="extended")
    return [tweet.full_text for tweet in tweets]

def send_news():
    """Fetch latest tweets & send them to Telegram"""
    try:
        tweets = get_fabrizio_romano_tweets()
        for tweet in tweets:
            bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=tweet)
            time.sleep(2)  # Delay to avoid spam

    except Exception as e:
        print(f"Error: {e}")

# Run every 5 minutes
if __name__ == "__main__":
    while True:
        send_news()
        time.sleep(300)  # Wait 5 minutes (300 sec)
