import sqlite3

import requests
from flask import Flask, redirect, render_template, request, url_for

from calc import best_performer, gain_loss, sort_by_value

app = Flask(__name__)
DATABASE = "portfolio.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS holdings (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               symbol TEXT NOT NULL,
               quantity REAL NOT NULL,
               buy_price REAL NOT NULL
           )"""
    )
    conn.commit()
    conn.close()


def get_price(symbol):
    """Return the current USD price as a float, or None if the request fails."""
    url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return float(response.json()["data"]["amount"])
    except (requests.RequestException, KeyError, ValueError):
        return None


def build_portfolio():
    """Read holdings from the database and attach live prices and gain/loss."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM holdings").fetchall()
    conn.close()

    priced, unpriced = [], []
    for row in rows:
        holding = dict(row)
        price = get_price(holding["symbol"])
        if price is None:
            unpriced.append(holding)
            continue
        value, gain, gain_pct = gain_loss(holding["quantity"], holding["buy_price"], price)
        holding.update(price=price, value=value, gain=gain, gain_pct=gain_pct)
        priced.append(holding)

    priced = sort_by_value(priced)
    total_value = sum(h["value"] for h in priced)
    total_cost = sum(h["quantity"] * h["buy_price"] for h in priced)
    return {
        "priced": priced,
        "unpriced": unpriced,
        "total_value": total_value,
        "total_gain": total_value - total_cost,
        "best": best_performer(priced),
    }


@app.route("/")
def index():
    return render_template("index.html", error=request.args.get("error"), **build_portfolio())


@app.route("/add", methods=["POST"])
def add():
    symbol = request.form.get("symbol", "").strip().upper()
    try:
        quantity = float(request.form.get("quantity", ""))
        buy_price = float(request.form.get("buy_price", ""))
    except ValueError:
        return redirect(url_for("index", error="Quantity and buy price must be numbers."))

    if not symbol.isalnum() or not 2 <= len(symbol) <= 10:
        return redirect(url_for("index", error="Symbol must be 2-10 letters or digits, like BTC."))
    if quantity <= 0 or buy_price < 0:
        return redirect(url_for("index", error="Quantity must be above 0 and price can't be negative."))

    conn = get_connection()
    conn.execute(
        "INSERT INTO holdings (symbol, quantity, buy_price) VALUES (?, ?, ?)",
        (symbol, quantity, buy_price),
    )
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:holding_id>", methods=["POST"])
def delete(holding_id):
    conn = get_connection()
    conn.execute("DELETE FROM holdings WHERE id = ?", (holding_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
