from aiogram import Router
from aiogram.dispatcher.filters.command import Command
from aiogram.dispatcher.filters.text import Text
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

router = Router()


@router.message(Command(commands=["start"]))
@router.message(Command(commands=["help"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="🔮 In Game предоставляет доступ к расширенной статистике топ-чемпионатов:\n\n"
             "🇬🇧 <b>Английской Премьер-Лиги</b>\n"
             "🇪🇸 <b>Испанской Ла-Лиги</b>\n"
             "🇩🇪 <b>Немецкой Бундес-Лиги</b>\n"
             "🇮🇹 <b>Итальянской Серии А</b>\n"
             "🇫🇷 <b>Французской Лиги 1</b>\n"
             "🇷🇺 <b>Российской Премьер-Лиги</b>\n\n"
             "Возможности бота:\n\n"
             "Используйте команду <b>/menu</b>, чтобы выбрать чемпионат и интересующую таблицу",
        reply_markup=ReplyKeyboardRemove()
    )
