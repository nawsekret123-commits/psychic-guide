from flask import Flask, request, redirect, url_for, render_template_string
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("8799281877:AAE-9WAtLb5zrifnNLebL9Xiw6j1bn5RVeI")
TELEGRAM_CHAT_ID = os.getenv("622522768")

with open("index.html", "r", encoding="utf-8") as f:
    HTML = f.read()

def send_telegram(name, phone, service, comment):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return

    text = f"""Новая заявка AqylFlow

Имя: {name}
Телефон: {phone}
Услуга: {service}
Комментарий: {comment}
"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(
        url,
        data={"chat_id": TELEGRAM_CHAT_ID, "text": text},
        timeout=10
    )

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        service = request.form.get("service", "").strip()
        comment = request.form.get("comment", "").strip()
        website = request.form.get("website", "").strip()

        if website:
            message = """
            <div style="margin:20px 0;padding:16px;border-radius:14px;background:#3d1f28;color:#ffb3b3;">
                Заявка отклонена.
            </div>
            """
            return render_template_string(HTML, message=message)

        if not (name and phone and service):
            message = """
            <div style="margin:20px 0;padding:16px;border-radius:14px;background:#3d1f28;color:#ffb3b3;">
                Заполните имя, телефон и выберите услугу.
            </div>
            """
            return render_template_string(HTML, message=message)

        try:
            send_telegram(name, phone, service, comment)
            message = """
            <div style="margin:20px 0;padding:16px;border-radius:14px;background:#123d2a;color:#7CFFB2;">
                Заявка отправлена. Мы свяжемся с вами.
            </div>
            """
        except Exception:
            message = """
            <div style="margin:20px 0;padding:16px;border-radius:14px;background:#3d1f28;color:#ffb3b3;">
                Ошибка отправки заявки.
            </div>
            """

        return render_template_string(HTML, message=message)

    return render_template_string(HTML, message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
