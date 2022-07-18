from aiogram import types, Dispatcher
from aiogram import Router

start_router = Router()


@start_router.message(commands=['start'])
async def bot_start(message: types.Message):
    await message.answer('Для просмотра турнирной таблицы или статистики игроков выбери соответсвующий чемпионат:')

# def register_start(dp: Dispatcher):
#     dp.register_message_handler(bot_start)
