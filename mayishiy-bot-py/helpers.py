import db as dbmod


def main_menu_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "📦 Kategoriyalar", "callback_data": "cats"}],
            [{"text": "🔍 Qidirish", "callback_data": "search"}],
            [{"text": "🎁 Aksiyalar", "callback_data": "promo"}],
            [{"text": "☎️ Bog'lanish", "callback_data": "contact"}],
        ]
    }


def categories_keyboard(categories):
    rows = [[{"text": c["name"], "callback_data": f"cat:{c['id']}"}] for c in categories]
    rows.append([{"text": "⬅️ Bosh menyu", "callback_data": "home"}])
    return {"inline_keyboard": rows}


def brands_keyboard(brands):
    rows = [[{"text": b["name"], "callback_data": f"brand:{b['id']}"}] for b in brands]
    rows.append([{"text": "⬅️ Kategoriyalar", "callback_data": "cats"}])
    return {"inline_keyboard": rows}


def products_keyboard(products, back_callback):
    rows = []
    for p in products:
        label = p["model"]
        if p["price"]:
            label += f" — {format_price(p['price'])}"
        rows.append([{"text": label, "callback_data": f"prod:{p['id']}"}])
    rows.append([{"text": "⬅️ Ortga", "callback_data": back_callback}])
    return {"inline_keyboard": rows}


def product_card_keyboard(back_callback):
    return {
        "inline_keyboard": [
            [{"text": "☎️ Sotuvchi bilan bog'lanish", "callback_data": "contact"}],
            [{"text": "⬅️ Ortga", "callback_data": back_callback}],
        ]
    }


def format_price(price):
    if price is None:
        return "Narxi kelishiladi"
    return f"{int(price):,}".replace(",", " ") + " so'm"


def format_product_card(product, brand_name):
    stock_text = "Omborda bor ✅" if product["in_stock"] else "Omborda yo'q ❌"
    text = f"🛒 *{brand_name} {product['model']}*\n\n"
    text += f"💰 Narxi: {format_price(product['price'])}\n"
    text += f"📦 Holati: {stock_text}\n\n"

    specs = dbmod.parse_specs(product["specs"])
    if specs:
        text += "*Texnik xususiyatlari:*\n"
        for key, value in specs.items():
            text += f"• {key}: {value}\n"
        text += "\n"

    if product["description"]:
        text += f"{product['description']}\n"

    return text
