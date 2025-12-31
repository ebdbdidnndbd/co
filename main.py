import asyncio
import os
import logging
import random
import sys
import time
import json
import re
from datetime import datetime, timedelta
from urllib.parse import unquote, quote
from io import BytesIO

# =========================================================
# ⚙️ إعدادات البيئة (GitHub Secrets)
# =========================================================
def get_env_int(key, default):
    val = os.getenv(key)
    if val and val.strip():
        try:
            return int(val)
        except ValueError:
            return default
    return default

# سحب البيانات من GitHub Secrets مع توفير قيم افتراضية لمنع توقف الكود
API_ID = get_env_int("API_ID", 22439859)
API_HASH = os.getenv("API_HASH", '312858aa733a7bfacf54eede0c275db4')
BOT_TOKEN = os.getenv("BOT_TOKEN", '8586272670:AAHJ2dl_bJlCC4gvWQyyJksq36-FsPLCoN0')
REQUIRED_CHANNEL = os.getenv("REQUIRED_CHANNEL", 'iomk3')  
SUPPORT_USER = os.getenv("SUPPORT_USER", "iomk0")
SESSION_NAME = 'Mnager_V8_Final'

# =========================================================
# 📦 تثبيت المكاتب تلقائياً
# =========================================================
try:
    import requests
    from bs4 import BeautifulSoup
    import aiohttp
    from deep_translator import GoogleTranslator
    from langdetect import detect
    import yt_dlp
    import edge_tts
    from telethon import TelegramClient, events, functions, types, Button
    from telethon.sessions import StringSession
except ImportError:
    os.system('pip install requests beautifulsoup4 aiohttp deep-translator langdetect yt-dlp edge-tts telethon')
    import requests
    from bs4 import BeautifulSoup
    import aiohttp
    from deep_translator import GoogleTranslator
    from langdetect import detect
    import yt_dlp
    import edge_tts
    from telethon import TelegramClient, events, functions, types, Button
    from telethon.sessions import StringSession

# إعداد السجلات (Logging)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================================================
# 🧠 فئة الذكاء الاصطناعي Gemini المتقدم
# =========================================================
class GeminiAI:
    def __init__(self, userbot_instance=None):
        self.conversation_history = {}
        self.api_url = "https://firebasevertexai.googleapis.com/v1beta/projects/gemmy-ai-bdc03/locations/us-central1/publishers/google/models/gemini-2.0-flash-lite:generateContent"
        self.headers = {
            'User-Agent': "Ktor client", 
            'Accept': "application/json", 
            'Content-Type': "application/json", 
            'x-goog-api-key': "AIzaSyD6QwvrvnjU7j-R6fkOghfIVKwtvc7SmLk", 
            'x-goog-api-client': "gl-kotlin/2.2.0-ai fire/16.5.0", 
            'x-firebase-appid': "1:652803432695:android:c4341db6033e62814f33f2", 
            'x-firebase-appversion': "79", 
            'x-firebase-appcheck': "eyJlcnJvciI6IlVOS05PV05fRVJST1IifQ=="
        }
        self.userbot = userbot_instance

    async def chat(self, user_id, user_message, system_prompt="أنت مساعد ذكي ومفيد."):
        try:
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            history = self.conversation_history[user_id][-4:]
            full_prompt = f"System: {system_prompt}\n\n"
            
            for msg in history:
                role = "User" if msg["role"] == "user" else "Assistant"
                full_prompt += f"{role}: {msg['content']}\n"
            
            full_prompt += f"User: {user_message}\nAssistant:"
            
            payload = {
                "contents": [{"role": "user", "parts": [{"text": full_prompt}]}]
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload, headers=self.headers, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()
                        ai_reply = result['candidates'][0]['content']['parts'][0]['text'].strip()
                        self.conversation_history[user_id].extend([
                            {"role": "user", "content": user_message},
                            {"role": "assistant", "content": ai_reply}
                        ])
                        return f"• {ai_reply}"
                    return "• ⚠️ حدث خطأ في الاتصال بالسيرفر."
        except Exception as e:
            return "• 🧠 عذراً، واجهت مشكلة في معالجة طلبك."

# [ملاحظة: الكود يكمل باقي الوظائف من الملف الأصلي مثل الصيد، الحماية، والصور الفائقة بنفس المنطق]

# =========================================================
# 🎩 تشغيل البوت الرئيسي (Manager)
# =========================================================
manager = TelegramClient(StringSession(), API_ID, API_HASH)

async def main():
    await manager.start(bot_token=BOT_TOKEN)
    print("✅ تم تشغيل سورس كومن بنجاح على سيرفرات جيثب!")
    await manager.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
