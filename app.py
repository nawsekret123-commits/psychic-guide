from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("8799281877:AAE-9WAtLb5zrifnNLebL9Xiw6j1bn5RVeI")
TELEGRAM_CHAT_ID = os.getenv("622522768")

def send_telegram(name, phone, service, comment):

    text = f"""
Новая заявка AqylFlow

Имя: {name}
Телефон: {phone}
Услуга: {service}
Комментарий: {comment}
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(
        url,
        data={"chat_id": TELEGRAM_CHAT_ID, "text": text}
    )

@app.route("/", methods=["GET","POST"])
def home():

    message = ""

    if request.method == "POST":

        name = request.form.get("name")
        phone = request.form.get("phone")
        service = request.form.get("service")
        comment = request.form.get("comment")

        send_telegram(name, phone, service, comment)

        message = "Заявка отправлена"

    return render_template("index.html", message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
