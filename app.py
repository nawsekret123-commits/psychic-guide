from flask import Flask, request, redirect, url_for, render_template
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("8799281877:AAHuImnbo4676epEZKKmRuMRR5skmR-0F2g")
TELEGRAM_CHAT_ID = os.getenv("622522768")


def send_telegram(name, phone, service, comment):
    if not TELEGRAM_TOKEN:
        print("ERROR: TELEGRAM_TOKEN is empty")
        return False

    if not TELEGRAM_CHAT_ID:
        print("ERROR: TELEGRAM_CHAT_ID is empty")
        return False

    text = f"""Новая заявка AqylFlow

Имя: {name}
Телефон: {phone}
Услуга: {service}
Комментарий: {comment}
"""

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    response = requests.post(
        url,
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        },
        timeout=15
    )

    print("TELEGRAM STATUS:", response.status_code)
    print("TELEGRAM RESPONSE:", response.text)

    return response.status_code == 200


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        service = request.form.get("service", "").strip()
        comment = request.form.get("comment", "").strip()

        if not name or not phone or not service:
            message = "Заполните имя, телефон и услугу"
            return render_template("index.html", message=message)

        ok = send_telegram(name, phone, service, comment)

        if ok:
            return redirect(url_for("home", success=1))
        else:
            return redirect(url_for("home", error=1))

    if request.args.get("success"):
        message = "Заявка отправлена"

    if request.args.get("error"):
        message = "Ошибка отправки в Telegram"

    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
