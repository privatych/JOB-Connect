FROM python:3.12-slim

# Рабочая директория внутри контейнера согласована с docker-compose
WORKDIR /opt/Job_ConnectBot

# Установка зависимостей
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY . .

# Запуск бота
CMD ["python", "run.py"]
