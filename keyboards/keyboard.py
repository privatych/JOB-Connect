from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton, WebAppInfo


async def create_inline_keyboard(button_text_array: list[str],
                                 button_callback_data: list[str],
                                 button_per_line: int = 1) -> InlineKeyboardMarkup:
    """
    Create inline keyboard with text and callback in arrays.
    You can set the number of buttons per line, default = 1
    You can also use url:{need url} in button_callback_data for create urls button
    You can also use app:{need url} in button_callback_data for create miniapp execute button
    """
    auto_inline_keyboard = InlineKeyboardBuilder()

    for i in range(len(button_text_array)):
        if button_callback_data[i][:4] == "url:":
            auto_inline_keyboard.add(
                InlineKeyboardButton(text=button_text_array[i],
                                     url=button_callback_data[i][4:])
            )
        elif button_callback_data[i][:4] == "app:":
            auto_inline_keyboard.add(
                InlineKeyboardButton(text=button_text_array[i],
                                     web_app=WebAppInfo(url=button_callback_data[i][4:]))
            )
        else:
            auto_inline_keyboard.add(InlineKeyboardButton(text=button_text_array[i],
                                                          callback_data=button_callback_data[i]))

    return auto_inline_keyboard.adjust(button_per_line).as_markup()
