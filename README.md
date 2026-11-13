# Crypto Portfolio Tracker

A small Flask web app to track crypto holdings and see their live value and gain/loss, using Coinbase's public price API.

**Live demo:** 

## Features
- Add and remove holdings (symbol, quantity, buy price)
- Live prices from the Coinbase public API (no API key needed)
- Total value, total gain/loss, and best performer
- Holdings sorted by value
- Handles bad input and unavailable prices without crashing

## Tech
Python, Flask, SQLite, HTML/CSS, Jinja templates, pytest

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py                  # http://127.0.0.1:5001
pytest
```

## How it works
- `app.py`: routes, database, and the price request
- `calc.py`: gain/loss, sorting, and best-performer logic (tested in `tests/`)

## What I learned

