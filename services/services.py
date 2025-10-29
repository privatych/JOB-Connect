from aiogram.types import FSInputFile
from utilities import Database
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import os

database = Database("./data/bot.db")


# region Users service
async def start_service(telegram_id: int, telegram_username: str):
    return database.add_user(telegram_id, telegram_username)

async def is_new_user(telegram_id: int):
    return True if database.get_user(telegram_id) is None else False


async def get_all_users_service():
    return database.get_users()
# endregion

# region Statistic service
async def set_user_activity_service(telegram_id: int, value: int):
    return database.set_user_active(telegram_id, value)


async def get_statistic_service() -> dict:
    statistic_data = {}

    statistic_data["users_count"] = len(database.get_users())
    statistic_data["active_users_count"] = len(database.get_users_by_activity(1))
    statistic_data["no_active_users_count"] = statistic_data["users_count"] - statistic_data["active_users_count"]

    return statistic_data


async def create_week_statistic_graphic():
    data = database.get_users()
    today = datetime.now().date()
    start_of_week = today - timedelta(days=7)
    registrations_per_day = defaultdict(int)

    for entry in data:
        registration_date = datetime.strptime(entry[2], "%Y-%m-%d").date()
        if start_of_week <= registration_date <= today:
            registrations_per_day[registration_date] += 1

    for day in range(7):
        current_day = start_of_week + timedelta(days=day)
        if current_day not in registrations_per_day:
            registrations_per_day[current_day] = 0

    sorted_registrations = sorted(registrations_per_day.items())
    dates = [date.strftime("%Y-%m-%d") for date, count in sorted_registrations]
    counts = [count for date, count in sorted_registrations]

    sns.set(style="whitegrid", palette="pastel")
    plt.ioff()

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=dates, y=counts, palette="viridis", hue=dates, legend=False)

    for i, count in enumerate(counts):
        ax.text(i, count + 0.1, str(count), ha="center", va="bottom", fontsize=12)

    plt.title("Регистрации за последнюю неделю", fontsize=16, pad=20)
    plt.xlabel("Дата", fontsize=14)
    plt.ylabel("Количество регистраций", fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()

    file_path = os.path.join("cache", "registrations_bar_chart.png")
    plt.savefig(file_path, dpi=300, bbox_inches="tight")
    plt.close()

    return FSInputFile(file_path)
# endregion