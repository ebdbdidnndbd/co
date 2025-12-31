import os

# جلب القيم مع التأكد أنها ليست فارغة
api_id_env = os.getenv("API_ID")
API_ID = int(api_id_env) if api_id_env and api_id_env.strip() else 22439859

API_HASH = os.getenv("API_HASH") or "312858aa733a7bfacf54eede0c275db4"
BOT_TOKEN = os.getenv("BOT_TOKEN") or "8307560710:AAFNRpzh141cq7rKt_OmPR0A823dxEaOZVU"
