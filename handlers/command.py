from aiogram import Router
from aiogram.filters import CommandStart
from keyboards import create_inline_keyboard
from aiogram.types import Message
from utilities import load_message_data
from services import start_service, is_new_user

command_router = Router()


@command_router.message(CommandStart())
async def cmd_start(message: Message):
    if await is_new_user(message.from_user.id):
        await start_service(message.from_user.id, message.from_user.username)

    message_data = await load_message_data("start_message", "ru")

    await message.answer(text=message_data.get("text"),
                         parse_mode="HTML",
                         reply_markup=await create_inline_keyboard(message_data.get("buttons_text"),
                                                                   message_data.get("buttons_data")))

