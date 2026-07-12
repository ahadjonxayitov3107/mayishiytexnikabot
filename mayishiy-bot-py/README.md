# Mayishiy texnika do'koni — katalog bot (PythonAnywhere versiyasi, Python + Flask)

Bu bot **butunlay bepul** ishlaydi (PythonAnywhere Free rejasida), chunki u
uzluksiz jarayon (`always-on task`, pullik) o'rniga **webhook** usulida ishlaydi —
oddiy veb-sayt sifatida ishga tushadi va Telegram undan xabarlarni "so'rab turadi" emas,
balki Telegram o'zi har bir xabarni shu saytga yuboradi.

## Tuzilma

```
mayishiy-bot-py/
├── app.py            # Flask ilova (webhook + admin panelni birlashtiradi)
├── config.py           # Sozlamalar (token, login/parol, do'kon ma'lumotlari)
├── db.py                 # SQLite baza bilan ishlash
├── telegram_api.py        # Telegram Bot API'ga so'rovlar
├── bot_logic.py             # Botning "miya"si — menyular, qidiruv va h.k.
├── admin.py                  # Admin panel yo'llari (routes)
├── templates/admin/            # Admin panel sahifalari (HTML)
├── requirements.txt
└── wsgi_namuna.py                # PythonAnywhere WSGI fayliga qo'yiladigan namuna
```

## 1-qadam: Telegram bot yaratish

Telegram'da **@BotFather** ga yozing → `/newbot` → nom bering → sizga
**BOT_TOKEN** beradi (masalan `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxx`).
Buni saqlab qo'ying.

## 2-qadam: PythonAnywhere'da akkaunt ochish

1. [pythonanywhere.com](https://www.pythonanywhere.com) → "Pricing & signup" → **"Create a Beginner account"** (bepul).
2. Kirganingizdan so'ng, **Dashboard**ga o'tasiz.

## 3-qadam: Fayllarni yuklash

**Eng oson yo'l — Files orqali:**
1. PythonAnywhere Dashboard'da **"Files"** bo'limiga o'ting.
2. Yangi papka yarating: `mayishiy-bot-py`
3. Shu zipdagi barcha fayllarni (papka tuzilmasini saqlagan holda) shu papka ichiga yuklang
   ("Upload a file" tugmasi bilan birma-bir, yoki quyidagi "Console" usuli bilan tezroq).

**Tezroq yo'l — Console orqali (tavsiya etiladi):**
1. Avval loyihangizni GitHub'ga yuklang (bepul akkaunt: github.com).
2. PythonAnywhere Dashboard'da **"Consoles"** → **"Bash"** ni oching.
3. Shu buyruqni yozing (repo manzilini o'zingiznikiga almashtiring):
   ```bash
   git clone https://github.com/SIZNING_USERNAME/mayishiy-bot-py.git
   ```

## 4-qadam: Kutubxonalarni o'rnatish

Bash konsolida:
```bash
cd mayishiy-bot-py
pip install --user -r requirements.txt
```

## 5-qadam: Sozlamalarni kiritish

`config.py` faylini oching (Files bo'limidan yoki `nano config.py` orqali konsoldan)
va quyidagilarni haqiqiy qiymatlarga almashtiring:
- `BOT_TOKEN` — 1-qadamda olingan token
- `ADMIN_USER`, `ADMIN_PASS` — admin panelga kirish uchun o'zingiz xohlagan login/parol
- `SECRET_KEY` — istalgan tasodifiy uzun so'z
- `SHOP_PHONE`, `SHOP_ADDRESS`, `SHOP_WORK_HOURS`, `SHOP_TELEGRAM` — do'kon ma'lumotlari

## 6-qadam: Web ilova (Web app) yaratish

1. Dashboard'da **"Web"** bo'limiga o'ting → **"Add a new web app"**.
2. Domenni tasdiqlang (masalan `sizningusername.pythonanywhere.com`) → **Next**.
3. Framework tanlashda: **"Manual configuration"** ni tanlang (Flask emas!) → Python versiyasini tanlang (3.10 yoki undan yuqori).
4. Web app yaratilgach, ochilgan sahifada **"Code"** bo'limida **"WSGI configuration file"** havolasini bosing.
5. Ochilgan faylning HAMMA tarkibini o'chirib, ushbu loyihadagi `wsgi_namuna.py` faylidagi
   kodni joylashtiring — faqat `SIZNING_USERNAME` va papka nomini o'zingiznikiga moslang.
6. Saqlang (Save).
7. Yana "Web" sahifasiga qayting, **"Reload"** (yashil) tugmasini bosing.

Endi saytingiz manzili: `https://sizningusername.pythonanywhere.com`

## 7-qadam: Telegram webhookni ulash

Brauzerda (yoki bash konsolda `curl` bilan) quyidagi manzilga kiring —
`BOT_TOKEN` va `SIZNING_USERNAME` o'rniga o'zingizning qiymatlaringizni qo'ying:

```
https://api.telegram.org/bot<BOT_TOKEN>/setWebhook?url=https://<SIZNING_USERNAME>.pythonanywhere.com/webhook/<BOT_TOKEN>
```

Agar javobda `"ok":true` chiqsa — tayyor! Botga Telegram'da `/start` yozib ko'ring.

## 8-qadam: Admin panelga kirish

Brauzerda: `https://sizningusername.pythonanywhere.com/admin`
`config.py`da bergan login/paroling bilan kiring va kategoriya/brend/mahsulot qo'shishni boshlang.

## Muhim eslatmalar

- **Har 3 oyda bir marta** PythonAnywhere akkauntingizga kirib turing (shunchaki login qiling) —
  aks holda bepul akkaunt vaqtincha to'xtatiladi.
- Kodni o'zgartirsangiz (masalan `config.py`ni tahrirlasangiz), "Web" bo'limida
  **"Reload"** tugmasini bosishni unutmang — aks holda o'zgarish kuchga kirmaydi.
- Baza fayli (`shop.db`) avtomatik yaratiladi, alohida sozlash shart emas.
