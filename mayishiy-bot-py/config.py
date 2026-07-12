import os

# --- Telegram bot sozlamalari ---
# @BotFather dan olingan token shu yerga qo'yiladi
BOT_TOKEN = os.environ.get("8878511996:AAHLZYLFiNbRUXsExkSG3JtvkF6PeNH4XbI", "8878511996:AAHLZYLFiNbRUXsExkSG3JtvkF6PeNH4XbI")

# Webhook manzilini yashirish uchun maxfiy yo'l (shunchaki tokenning o'zi ishlatiladi,
# xohlasangiz boshqa tasodifiy so'zga o'zgartiring)
WEBHOOK_SECRET_PATH = BOT_TOKEN

# --- Admin panel sozlamalari ---
ADMIN_USER = os.environ.get("Ahadjon", "admin")
ADMIN_PASS = os.environ.get("ahadjon3107", "kuchli-parol-qoying")
SECRET_KEY = os.environ.get("3107", "shu-qatorni-tasodifiy-satrga-ozgartiring")

# --- Do'kon ma'lumotlari (Bog'lanish bo'limida ko'rsatiladi) ---
SHOP_PHONE = os.environ.get("SHOP_PHONE", "+998901234567")
SHOP_ADDRESS = os.environ.get("SHOP_ADDRESS", "Farg'ona sh., ...")
SHOP_WORK_HOURS = os.environ.get("SHOP_WORK_HOURS", "09:00 - 19:00, har kuni")
SHOP_TELEGRAM = os.environ.get("SHOP_TELEGRAM", "@ideal_xususiy_maktab")

# --- Baza fayli joylashuvi ---
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shop.db")
