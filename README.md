# --- Create README.md ---
Write-File "README.md" @"
# PriceAlertEngine

Real-time price alert system for cryptocurrencies and stocks.

## Features

- Monitor cryptocurrency prices via CoinGecko (free, no API key)
- Monitor stock prices via Yahoo Finance (using yfinance)
- Create alerts with conditions: greater than, less than, percentage change (experimental)
- Email notifications when alerts trigger
- Web UI to manage alerts
- Background scheduler checks every 30 seconds (configurable)
- Logs all checks and notifications

## Tech Stack

- Python 3.8+
- Flask
- SQLAlchemy (SQLite/PostgreSQL)
- APScheduler
- yfinance, requests
- smtplib (Gmail SMTP)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tayebmekati37-art/price-alert-engine.git
   cd price-alert-engine
   "@