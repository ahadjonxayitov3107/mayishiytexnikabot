import config
import db as dbmod
import telegram_api as tg
from helpers import (
    main_menu_keyboard,
    categories_keyboard,
    brands_keyboard,
    products_keyboard,
    product_card_keyboard,
    format_product_card,
)


def get_awaiting_search(chat_id):
    rows = dbmod.query("SELECT awaiting_search FROM user_state WHERE chat_id = ?", (chat_id,))
    return bool(rows[0]["awaiting_search"]) if rows else False


def set_awaiting_search(chat_id, value):
    dbmod.execute(
        """INSERT INTO user_state (chat_id, awaiting_search) VALUES (?, ?)
           ON CONFLICT(chat_id) DO UPDATE SET awaiting_search = excluded.awaiting_search""",
        (chat_id, int(value)),
    )


def handle_update(update):
    if "callback_query" in update:
        handle_callback(update["callback_query"])
    elif "message" in update:
        handle_message(update["message"])


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        set_awaiting_search(chat_id, False)
        name = message["from"].get("first_name", "")
        tg.send_message(
            chat_id,
            f"Assalomu alaykum, {name}! 👋\n\n"
            "Bizning botimiz orqali do'kondagi mayishiy texnikalar haqida narx va texnik "
            "xususiyatlarni bilib olishingiz mumkin.\n\nQuyidagi menyudan tanlang:",
            main_menu_keyboard(),
        )
        return

    if get_awaiting_search(chat_id):
        set_awaiting_search(chat_id, False)
        do_search(chat_id, text.strip())


def do_search(chat_id, query_text):
    like_pattern = f"%{query_text}%"
    rows = dbmod.query(
        "SELECT id, model, price FROM products WHERE model LIKE ? COLLATE NOCASE ORDER BY model LIMIT 20",
        (like_pattern,),
    )
    if not rows:
        tg.send_message(
            chat_id,
            f"\"{query_text}\" bo'yicha hech narsa topilmadi. Boshqa nom bilan urinib ko'ring.",
            main_menu_keyboard(),
        )
        return
    tg.send_message(chat_id, f"🔎 \"{query_text}\" bo'yicha natijalar:", products_keyboard(rows, "home"))


def handle_callback(cb):
    chat_id = cb["message"]["chat"]["id"]
    message_id = cb["message"]["message_id"]
    data = cb.get("data", "")
    tg.answer_callback_query(cb["id"])

    if data == "home":
        set_awaiting_search(chat_id, False)
        tg.edit_message_text(chat_id, message_id, "Bosh menyu:", main_menu_keyboard())

    elif data == "cats":
        rows = dbmod.query("SELECT id, name FROM categories ORDER BY sort_order, name")
        if not rows:
            tg.edit_message_text(chat_id, message_id, "Hozircha kategoriyalar qo'shilmagan.", main_menu_keyboard())
        else:
            tg.edit_message_text(chat_id, message_id, "📦 Kategoriyani tanlang:", categories_keyboard(rows))

    elif data.startswith("cat:"):
        category_id = data.split(":")[1]
        rows = dbmod.query("SELECT id, name FROM brands WHERE category_id = ? ORDER BY name", (category_id,))
        if not rows:
            tg.edit_message_text(chat_id, message_id, "Bu kategoriyada hozircha brendlar yo'q.", main_menu_keyboard())
        else:
            tg.edit_message_text(chat_id, message_id, "🏷 Brendni tanlang:", brands_keyboard(rows))

    elif data.startswith("brand:"):
        brand_id = data.split(":")[1]
        rows = dbmod.query(
            "SELECT id, model, price FROM products WHERE brand_id = ? ORDER BY model", (brand_id,)
        )
        if not rows:
            tg.edit_message_text(chat_id, message_id, "Bu brendda hozircha mahsulot yo'q.", main_menu_keyboard())
        else:
            tg.edit_message_text(chat_id, message_id, "📱 Modelni tanlang:", products_keyboard(rows, "cats"))

    elif data.startswith("prod:"):
        product_id = data.split(":")[1]
        rows = dbmod.query(
            """SELECT p.*, b.name AS brand_name, b.id AS brand_id
               FROM products p JOIN brands b ON p.brand_id = b.id
               WHERE p.id = ?""",
            (product_id,),
        )
        if not rows:
            tg.edit_message_text(chat_id, message_id, "Mahsulot topilmadi.", main_menu_keyboard())
            return
        product = rows[0]
        caption = format_product_card(product, product["brand_name"])
        back_callback = f"brand:{product['brand_id']}"

        if product["image_url"]:
            tg.delete_message(chat_id, message_id)
            tg.send_photo(chat_id, product["image_url"], caption, product_card_keyboard(back_callback))
        else:
            tg.edit_message_text(chat_id, message_id, caption, product_card_keyboard(back_callback))

    elif data == "search":
        set_awaiting_search(chat_id, True)
        tg.edit_message_text(
            chat_id, message_id,
            "🔍 Qidirmoqchi bo'lgan mahsulot nomini yozing (masalan: \"LG 350\" yoki \"muzlatgich\"):",
        )

    elif data == "promo":
        rows = dbmod.query("SELECT id, model, price FROM products WHERE is_promo = 1 ORDER BY model LIMIT 20")
        if not rows:
            tg.edit_message_text(chat_id, message_id, "Hozircha aksiyadagi mahsulotlar yo'q.", main_menu_keyboard())
        else:
            tg.edit_message_text(chat_id, message_id, "🎁 Aksiyadagi mahsulotlar:", products_keyboard(rows, "home"))

    elif data == "contact":
        text = (
            "☎️ Bog'lanish:\n\n"
            f"📞 Telefon: {config.SHOP_PHONE}\n"
            f"📍 Manzil: {config.SHOP_ADDRESS}\n"
            f"🕐 Ish vaqti: {config.SHOP_WORK_HOURS}\n"
            f"💬 Telegram: {config.SHOP_TELEGRAM}"
        )
        tg.edit_message_text(chat_id, message_id, text, main_menu_keyboard())
