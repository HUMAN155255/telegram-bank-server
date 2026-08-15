import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.environ["8571545356:AAGtqHYmafuPxJbQn00ipb2PxtXlKHi40Rw"]
ADMIN_ID = os.environ["6306406299"]


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

    if not bank:
        return jsonify({
            "ok": False,
            "error": "Банк таңдалмаған"
        }), 400

    # Тек жалған DEMO деректері жіберіледі
    message = (
        "🔔 DEMO ӨТІНІМ\n\n"
        f"🏦 Банк: {bank}\n"
        "👤 Аты: Demo User\n"
        "📱 Демо нөмірі: +7 700 000 00 00\n"
        "🔗 Username: @demo_user\n"
        "💰 Сома: 15000 ₸"
    )

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": ADMIN_ID,
                "text": message
            },
            timeout=15
        )

        if not response.ok:
            return jsonify({
                "ok": False,
                "error": "Telegram API error"
            }), 500

    except requests.RequestException:
        return jsonify({
            "ok": False,
            "error": "Telegram connection error"
        }), 500

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
