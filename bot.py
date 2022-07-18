import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from soccer_bot.config import load_config
from soccer_bot.handlers.start import start_router
from soccer_bot.services import broadcaster
from soccer_bot.services.default_commands import set_default_commands

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот был запущен!")
    await set_default_commands(bot)


def register_global_middlewares(dp: Dispatcher, config, session_pool):
    pass


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )
    config = load_config('.env')
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp['config'] = config

    for router in [start_router]:
        dp.include_router(router)

    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')

