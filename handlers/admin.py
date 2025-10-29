from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from keyboards import create_inline_keyboard
from aiogram.fsm.context import FSMContext
from states import BroadcastState
from services import get_all_users_service, set_user_activity_service, get_statistic_service, create_week_statistic_graphic
from logging import log, ERROR
from config import ADMIN


admin_router = Router()


@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id == ADMIN:
        await message.answer(text="Добро пожаловать в панель администратора. Выбери нужную функцию:",
                             parse_mode="HTML",
                             reply_markup=await create_inline_keyboard(["🚀Отправить рассылку",
                                                                        "📊Получить статистику"],
                                                                       ["send_broadcast_message",
                                                                        "get_stat"]))


@admin_router.callback_query(F.data == "admin_menu")
async def cmd_admin(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.delete()

    if callback.from_user.id == ADMIN:
        await callback.message.answer(text="Добро пожаловать в панель администратора. Выбери нужную функцию:",
                             parse_mode="HTML",
                             reply_markup=await create_inline_keyboard(["🚀Отправить рассылку",
                                                                        "📊Получить статистику"],
                                                                       ["send_broadcast_message",
                                                                        "get_stat"]))


@admin_router.callback_query(F.data == "get_stat")
async def send_stat_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()

    graphic = await create_week_statistic_graphic()

    if callback.from_user.id == ADMIN:
        stat_data = await get_statistic_service()

        message_text = (f"Статистика бота:\n"
                        f"Кол-во пользователей: <b>{stat_data.get("users_count")}</b>\n"
                        f"Кол-во активных пользователей: <b>{stat_data.get("active_users_count")}</b>\n"
                        f"Кол-во неактивных пользователей: <b>{stat_data.get("no_active_users_count")}</b>\n")

        await callback.message.answer_photo(photo=graphic,
                                            caption=message_text,
                                            parse_mode="HTML",
                                            reply_markup=await create_inline_keyboard(["⬅️Назад"],
                                                                                ["admin_menu"]))


@admin_router.callback_query(F.data == "send_broadcast_message")
async def send_broadcast_message_handler(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    msg = await callback.message.answer(text="Пришли мне сообщение для рассылки.",
                                  parse_mode="HTML",
                                  reply_markup=await create_inline_keyboard(["⬅️Назад"],
                                                                            ["admin_menu"]))

    await state.set_state(BroadcastState.broadcast_message)
    await state.update_data(last_message_id=msg.message_id)


@admin_router.message(BroadcastState.broadcast_message)
async def send_broadcast_message_handler(message: Message, state: FSMContext):
    state_data = await state.get_data()
    last_message_id = state_data.get("last_message_id")

    await message.bot.delete_message(message.chat.id, last_message_id)

    if message.text:
        text_data = message.text
    else:
        text_data = message.caption

    photo = message.photo[-1] if message.photo else None
    video = message.video if message.video else None

    await state.update_data(text_data=text_data, photo=photo, video=video)

    if photo:
        await message.answer_photo(photo=photo.file_id,
                                   caption=text_data,
                                   parse_mode="HTML",
                                   reply_markup=await create_inline_keyboard(["🚀Отправить",
                                                                              "❌Отменить"],
                                                                             ["send_broadcast_confirm",
                                                                              "admin_menu"]))
    elif video:
        await message.answer_video(video=video.file_id,
                                   caption=text_data,
                                   parse_mode="HTML",
                                   reply_markup=await create_inline_keyboard(["🚀Отправить",
                                                                              "❌Отменить"],
                                                                             ["send_broadcast_confirm",
                                                                              "admin_menu"]))
    else:
        await message.answer(text=text_data,
                             parse_mode="HTML",
                             reply_markup=await create_inline_keyboard(["🚀Отправить",
                                                                              "❌Отменить"],
                                                                             ["send_broadcast_confirm",
                                                                              "admin_menu"]))

    await state.set_state(BroadcastState.confirm_message)


@admin_router.callback_query(F.data == "send_broadcast_confirm", BroadcastState.confirm_message)
async def send_broadcast_confirm_message(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()

    message_data = await state.get_data()
    text_data = message_data.get("text_data")
    photo = message_data.get("photo")
    video = message_data.get("video")

    users = await get_all_users_service()
    count = 0

    for user in users:
        try:
            if photo:
                await callback.bot.send_photo(user[0], photo.file_id, caption=text_data, parse_mode="HTML")
                count += 1
            elif video:
                await callback.bot.send_video(user[0], video.file_id, caption=text_data, parse_mode="HTML")
                count += 1
            else:
                await callback.bot.send_message(user[0], text_data, parse_mode="HTML")
                count += 1
            await set_user_activity_service(user[0], 1)
        except Exception as e:
            await set_user_activity_service(user[0], 0)
            log(level=ERROR, msg=f"Ошибка при отправке сообщения пользователю {user[0]}: {e}")

    await callback.message.answer(f"Рассылка завершена. Кол-во пользователей получивших рассылку: {count}")


@admin_router.message(Command("photo_id"))
async def cmd_photo_id(message: Message):
    if message.from_user.id == ADMIN:
        await message.answer(text=f"{message.photo[-1].file_id}")



