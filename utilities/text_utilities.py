import json
from typing import Literal


async def load_json_data(file_path: str) -> dict:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data


async def load_message_data(text_name: str, locale: Literal["eu", "ru"]) -> dict:
    file_path = f"./data/{locale}/{text_name}.json"
    return await load_json_data(file_path)