from flask import Flask, request, jsonify, redirect, url_for

import config
import db as dbmod
import bot_logic
from admin import admin_bp

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.register_blueprint(admin_bp)

# Baza jadvallarini birinchi ishga tushirishda yaratib qo'yamiz
dbmod.init_db()


@app.teardown_appcontext
def _close_db(exception=None):
    dbmod.close_db(exception)


@app.route("/")
def index():
    return redirect(url_for("admin.login"))


# Telegram shu manzilga POST so'rov yuboradi (webhook)
@app.route(f"/webhook/{config.WEBHOOK_SECRET_PATH}", methods=["POST"])
def webhook():
    update = request.get_json(force=True, silent=True) or {}
    try:
        bot_logic.handle_update(update)
    except Exception as e:
        print(f"Update qayta ishlashda xato: {e}")
    return jsonify({"ok": True})


if __name__ == "__main__":
    # Faqat local test uchun. PythonAnywhere'da WSGI orqali ishga tushadi.
    app.run(debug=True, port=5000)
