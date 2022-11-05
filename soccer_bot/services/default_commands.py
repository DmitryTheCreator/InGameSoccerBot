from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand(command='start', description='Главное окно'),
        BotCommand(command='help', description='Список команд'),
        BotCommand(command='menu', description='Меню')
    ])
