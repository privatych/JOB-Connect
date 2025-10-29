import logging
from aiogram import Bot, Dispatcher, BaseMiddleware
from handlers import command_router, admin_router
from aiogram.exceptions import TelegramBadRequest
import os
import asyncio
from config import BOT_TOKEN

if not os.path.exists("./logs"):
    os.makedirs("./logs")

if not os.path.exists("./cache"):
    os.makedirs("./cache")

if not os.path.exists("./logs/error.log"):
    with open("./logs/error.log", 'w') as file:
        file.write("")


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        try:
            return await handler(event, data)
        except TelegramBadRequest as telegram_exception:
            log(level=ERROR, msg=f"TelegramBadRequest: {telegram_exception}")
            if event.message:
                await event.message.answer(
                    text="Сообщение устарело. Воспользуйтесь командой /start",
                    parse_mode="HTML"
                )
        except Exception as e:
            log(level=ERROR, msg=f"Unexpected error: {e}")

            if event.message:
                await event.message.answer("Произошла неизвестная ошибка. Пожалуйста, попробуйте позже."
                                           "Или напишите в поддержку @cyberopennetwork_support")


bot = Bot(BOT_TOKEN)
dispatcher = Dispatcher()


async def main():
    dispatcher.callback_query.middleware(ErrorHandlerMiddleware())
    dispatcher.include_routers(admin_router, command_router)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    #logging.basicConfig(level=logging.ERROR, filename="./logs/error.log")
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        logging.log(level=logging.INFO, msg="Bot stop!")

