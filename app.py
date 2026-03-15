from flask import Flask, request, redirect, url_for, render_template
import os
import requests
from datetime import datetime

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("8799281877:AAE-9WAtLb5zrifnNLebL9Xiw6j1bn5RVeI")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "622522768")


def send_telegram(name: str, phone: str, service: str, comment: str) -> None:
    text = f"""
Новая заявка AqylFlow

Имя: {name}
Телефон: {phone}
Услуга: {service}
Комментарий: {comment if comment else "-"}
Время: {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}
"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(
        url,
        data={"chat_id": TELEGRAM_CHAT_ID, "text": text},
        timeout=10,
    )


@app.route("/", methods=["GET", "POST"])
def home():
    success = request.args.get("success")
    error = request.args.get("error")

    message = ""

    if success:
        message = """
        <div class="alert success">
            Заявка отправлена. Мы свяжемся с вами.
        </div>
        """

    if error == "empty":
        message = """
        <div class="alert error">
            Заполните имя, телефон и выберите услугу.
        </div>
        """

    if error == "spam":
        message = """
        <div class="alert error">
            Заявка отклонена.
        </div>
        """

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        service = request.form.get("service", "").strip()
        comment = request.form.get("comment", "").strip()
        website = request.form.get("website", "").strip()

        if website:
            return redirect(url_for("home", error="spam"))

        if not (name and phone and service):
            return redirect(url_for("home", error="empty"))

        try:
            send_telegram(name, phone, service, comment)
        except Exception as e:
            print("TELEGRAM ERROR:", e)

        return redirect(url_for("home", success=1))

    return render_template("index.html", message=message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
