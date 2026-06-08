from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID   = os.environ.get("CHAT_ID")

SIGNALS = {
    "ut1_buy":  "🟢 UT Bot #1 — BUY\n📈 Сигнал на покупку",
    "ut1_sell": "🔴 UT Bot #1 — SELL\n📉 Сигнал на продаж",
    "ut2_buy":  "🔵 UT Bot #2 — BUY\n📈 Сигнал на покупку",
    "ut2_sell": "🟤 UT Bot #2 — SELL\n📉 Сигнал на продаж",
}

@app.route("/webhook", methods=["POST"])
def webhook():
    body    = request.get_json(silent=True) or {}
    signal  = body.get("signal", "").lower()
    ticker  = body.get("ticker", "—")
    price   = body.get("price",  "—")
    tf      = body.get("timeframe", "—")
    if signal not in SIGNALS:
        return jsonify({"ok": False}), 400
    text = f"{SIGNALS[signal]}\n\nТікер: {ticker}\nЦіна: {price}\nТаймфрейм: {tf}"
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                  json={"chat_id": CHAT_ID, "text": text})
    return jsonify({"ok": True})

@app.route("/")
def index():
    return "OK", 200
