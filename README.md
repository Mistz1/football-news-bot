# Football News Bot

## Overview
Football News Bot is an automated Telegram bot that fetches the latest football news from popular newspapers in Spain and England. It includes updates on **injuries, transfers, goals, and other major events**. The bot runs every hour and posts the news in a specified Telegram channel.

## Features
- Fetches the latest football news from:
  - Marca
  - AS
  - Mundo Deportivo
  - Relevo
  - BBC Sport
  - Sky Sports
  - The Guardian
  - ESPN
  - Fabrizio Romano (Twitter/X)
- Posts updates automatically in a Telegram channel every hour.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- `pip` (Python package manager)
- `git`

### Clone the Repository
```bash
git clone https://github.com/Mistz1/football-news-bot.git
cd football-news-bot
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Setup Telegram Bot
1. Create a bot via [BotFather](https://t.me/BotFather) on Telegram.
2. Get the **Bot Token** from BotFather.
3. Create a **Telegram Channel** and add your bot as an admin.
4. Get your channel ID from [@userinfobot](https://t.me/userinfobot).

### Configure Environment Variables
Create a `.env` file and add:
```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHANNEL_ID=@your_channel_id
```

## Running the Bot
```bash
python bot.py
```

## Deployment on Railway
1. Create a free account on [Railway.app](https://railway.app/).
2. Deploy the project from GitHub.
3. Add environment variables (`TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHANNEL_ID`).
4. Set the bot to run **every hour** using Railway's scheduled jobs.

## Future Improvements
- Add more news sources.
- Improve the formatting of news posts.

## License
This project is licensed under the MIT License.
