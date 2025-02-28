import tweepy
import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Telegram bot credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Tweepy client
client = tweepy.Client(bearer_token=BEARER_TOKEN)

def get_latest_tweets(username, count=5):
    """Fetch latest tweets from a specific user"""
    user = client.get_user(username=username, user_auth=True)
    tweets = client.get_users_tweets(user.data.id, max_results=count, tweet_fields=["created_at"])
    
    if tweets.data:
        return [tweet.text for tweet in tweets.data]
    return []

def send_telegram_message(message):
    """Send a message to the Telegram channel"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)

def main():
    while True:
        tweets = get_latest_tweets("FabrizioRomano", count=3)  # Fetch latest tweets
        for tweet in tweets:
            send_telegram_message(tweet)  # Send each tweet to Telegram
        time.sleep(300)  # Wait 5 minutes before fetching again

if __name__ == "__main__":
    main()
