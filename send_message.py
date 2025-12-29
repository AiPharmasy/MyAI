import os
import requests
from datetime import datetime

# ==============================
# تنظیم متغیرهای محیطی
# ==============================
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

# ==============================
# ارسال پیام تلگرام
# ==============================
def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "disable_web_page_preview": True
    }
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()

# ==============================
# ارسال پیام به OpenRouter و گرفتن پاسخ
# ==============================
def chat_openrouter(message: str) -> str:
    if not OPENROUTER_API_KEY:
        return "❌ OpenRouter API Key تنظیم نشده."

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",  # مدل دلخواه
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        r.raise_for_status()
        data = r.json()
        reply = data["choices"][0]["message"]["content"]
        return reply
    except Exception as e:
        return f"❌ خطا در تماس با OpenRouter: {e}"

# ==============================
# اجرای اصلی
# ==============================
if __name__ == "__main__":
    now = datetime.utcnow()
    user_message = "سلام"

    # دریافت پاسخ مدل
    openrouter_reply = chat_openrouter(user_message)

    # ساخت پیام نهایی تلگرام
    message = (
        f"⏰ پیام خودکار تلگرام\n"
        f"زمان اجرا: {now} UTC\n\n"
        f"پیام ارسالی: {user_message}\n"
        f"پاسخ OpenRouter: {openrouter_reply}"
    )

    send_telegram_message(message)
    print("پیام ارسال شد و پاسخ مدل دریافت شد!")
