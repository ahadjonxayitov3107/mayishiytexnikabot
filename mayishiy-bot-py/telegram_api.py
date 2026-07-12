import requests
import config

API_BASE = f"https://api.telegram.org/bot{config.BOT_TOKEN}"


def _call(method, payload):
    try:
        resp = requests.post(f"{API_BASE}/{method}", json=payload, timeout=10)
        return resp.json()
    except requests.RequestException as e:
        print(f"Telegram API xatosi ({method}): {e}")
        return None


def send_message(chat_id, text, reply_markup=None, parse_mode="Markdown"):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return _call("sendMessage", payload)


def edit_message_text(chat_id, message_id, text, reply_markup=None, parse_mode="Markdown"):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": parse_mode,
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    result = _call("editMessageText", payload)
    # Agar tahrirlab bo'lmasa (masalan xabar rasm bo'lsa), yangi xabar yuboramiz
    if not result or not result.get("ok"):
        return send_message(chat_id, text, reply_markup, parse_mode)
    return result


def send_photo(chat_id, photo_url, caption, reply_markup=None, parse_mode="Markdown"):
    payload = {"chat_id": chat_id, "photo": photo_url, "caption": caption, "parse_mode": parse_mode}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return _call("sendPhoto", payload)


def delete_message(chat_id, message_id):
    return _call("deleteMessage", {"chat_id": chat_id, "message_id": message_id})


def answer_callback_query(callback_query_id, text=None):
    payload = {"callback_query_id": callback_query_id}
    if text:
        payload["text"] = text
    return _call("answerCallbackQuery", payload)


def set_webhook(url):
    return _call("setWebhook", {"url": url})
