from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Переменные окружения
# BOT_TOKEN: токен Telegram-бота
# ADMIN: Telegram ID администратора (целое число)

BOT_TOKEN = getenv("BOT_TOKEN", "")

ADMIN = int(getenv("ADMIN", "0"))