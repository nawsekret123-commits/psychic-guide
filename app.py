import os
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "8799281877:AAHuImnbo4676epEZKKmRuMRR5skmR-0F2g"
TELEGRAM_CHAT_ID = "622522768"

def send_telegram_message(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram env not set")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }

    try:
        r = requests.post(url, json=payload, timeout=10)
        print("TG:", r.status_code, r.text)
        return r.status_code == 200
    except Exception as e:
        print("Telegram error:", e)
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "").strip()
    phone = request.form.get("phone", "").strip()
    service = request.form.get("service", "").strip()
    comment = request.form.get("comment", "").strip()

    text = (
        "Новая заявка с сайта AqylFlow\n"
        f"Имя: {name}\n"
        f"Телефон: {phone}\n"
        f"Услуга: {service}\n"
        f"Комментарий: {comment}"
    )

    sent = send_telegram_message(text)

    if sent:
        return jsonify({"ok": True, "message": "Заявка отправлена"})
    return jsonify({"ok": False, "message": "Ошибка отправки в Telegram"}), 500
