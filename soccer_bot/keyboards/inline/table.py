from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from soccer_bot.models.callback_factory.table import TableCallbackFactory


def table_keyboard(items: list[str], in_a_row: int = 2) -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру
    :param items: список текстов для кнопок
    :param in_a_row: количество кнопок в ряду
    :return: объект инлайн-клавиатуры
    """
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.button(text=item, callback_data=TableCallbackFactory(action="choose", text=item))
    builder.button(text="Назад", callback_data=TableCallbackFactory(action="cancel"))
    builder.adjust(in_a_row)
    return builder.as_markup()
