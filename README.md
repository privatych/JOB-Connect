# Job_ConnectBot — Telegram бот на aiogram v3

Этот бот на aiogram v3 регистрирует пользователей в локальную SQLite-базу, показывает стартовое сообщение с кнопкой на мини‑приложение, а для администратора предоставляет панель с:
- отправкой рассылки по всем пользователям (текст/фото/видео);
- просмотром статистики с графиком регистраций за неделю.

## Требования
- Python 3.12+
- Telegram Bot Token
- Опционально: Docker + Docker Compose

## Структура проекта (основное)
- `run.py` — точка входа, регистрация роутеров, запуск polling.
- `handlers/command.py` — обработчик `/start`.
- `handlers/admin.py` — админ‑панель: рассылка и статистика.
- `services/services.py` — работа с БД и построение графика (seaborn/matplotlib).
- `utilities/database.py` — SQLite‑обёртка (`data/bot.db`).
- `utilities/text_utilities.py` — загрузка текстов из `data/<locale>/*.json`.
- `keyboards/keyboard.py` — генератор inline‑клавиатур.
- `states/admin_states.py` — FSM состояния рассылки.
- `config.py` — загрузка переменных окружения (`BOT_TOKEN`, `ADMIN`).

## Переменные окружения
Используйте `.env` в корне:
```
BOT_TOKEN=your-telegram-bot-token
ADMIN=123456789
```
См. шаблон `.env.example`.

## Установка и запуск (локально)
1. Создайте и активируйте виртуальное окружение (рекомендуется):
```
python3 -m venv .venv
source .venv/bin/activate
```
2. Установите зависимости:
```
pip install --upgrade pip
pip install -r requirements.txt
```
3. Создайте файл `.env` по образцу `.env.example` и заполните `BOT_TOKEN`, `ADMIN`.
4. Убедитесь, что файл БД существует: `data/bot.db`. Если его нет, создайте пустую БД c таблицей:
```
sqlite3 data/bot.db "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, telegram_id INTEGER UNIQUE, telegram_username TEXT, registration_date TEXT, is_active INTEGER DEFAULT 1);"
```
5. Запустите бота:
```
python run.py
```

## Запуск в Docker
1. Создайте `.env` (см. выше).
2. Соберите и запустите контейнер:
```
docker compose up -d --build
```
Логи:
```
docker compose logs -f
```

## Описание функционала
- `/start` — регистрация нового пользователя (если ещё не был в БД), вывод локализованного сообщения `data/ru/start_message.json` с кнопкой (поддержка `url:` и `app:` ссылок).
- `/admin` — доступ только пользователю с `ADMIN` (из `.env`):
  - "🚀Отправить рассылку" — загрузка текста/фото/видео, предпросмотр, подтверждение и рассылка всем пользователям; при ошибке доставки помечает пользователя как неактивного.
  - "📊Получить статистику" — отправляет график регистраций за последнюю неделю (PNG в `cache/registrations_bar_chart.png`).

## Примечания по разработке
- Логи ошибок — в `logs/error.log` (каталоги `logs` и `cache` создаются при старте).
- Графики сохраняются в `cache/` и отправляются как `FSInputFile`.
- Локализация текстов — через JSON в `data/<locale>/`.

## Типичные проблемы
- Неверный токен или отсутствует интернет — бот не стартует (`TelegramBadRequest`).
- В БД нет таблицы `users` — создайте схему, как показано выше.
- Несовпадение путей при Docker‑запуске — в `Dockerfile` и `docker-compose.yml` рабочая директория согласована: `/opt/Job_ConnectBot`.

## Лицензия
MIT (при необходимости замените).
