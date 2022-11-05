from aiogram import Router, F, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.dispatcher.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from soccer_bot.keyboards.inline.competition import competition_keyboard
from soccer_bot.keyboards.inline.table import table_keyboard
from soccer_bot.models.callback_factory.competition import CompetitionCallbackFactory
from soccer_bot.models.callback_factory.table import TableCallbackFactory

router = Router()

# Списки доступных чемпионатов и таблиц
available_competition_names = ["🇬🇧 АПЛ",
                               "🇪🇸 ЛА-ЛИГА",
                               "🇩🇪 БУНДЕС-ЛИГА",
                               "🇮🇹 СЕРИЯ А",
                               "🇫🇷 ЛИГА 1",
                               "🇷🇺 РПЛ"]

available_table_names = ["📊 Таблица",
                         "📆 Следующий тур",
                         "🎯 Бомбардиры",
                         "💡 Ассистенты",
                         "💎 Гол+Пас",
                         "🧤 Сухие матчи"]


# Возможные состояния меню
class ChooseTable(StatesGroup):
    choosing_competition_name = State()
    choosing_table_name = State()


@router.message(Command(commands=["menu"]))
async def cmd_table(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Для просмотра статистики выберите чемпионат",
        # Инлайн клнопки с чемпионатами
        reply_markup=competition_keyboard(items=available_competition_names)
    )
    # Текущее состояние - выбор чемпионата
    await state.set_state(ChooseTable.choosing_competition_name)


# Этап выбора чемпионата
@router.callback_query(ChooseTable.choosing_competition_name,
                       CompetitionCallbackFactory.filter(F.action == "choose"))
async def competition_chosen(
        callback: types.CallbackQuery,
        callback_data: CompetitionCallbackFactory,
        state: FSMContext):
    # Сохранение выбранного чемпионата
    await state.update_data(chosen_competition=callback_data.text.lower())
    await callback.message.answer(
        text=f"Вы выбрали чемпионат<b>{callback_data.text}</b>\n\n"
             f"Выберите интересующую таблицу",
        parse_mode='HTML',
        # Инлайн-кнопки с таблицами
        reply_markup=table_keyboard(items=available_table_names)
    )
    # Текущее состояние - выбор таблицы
    await state.set_state(ChooseTable.choosing_table_name)
    await callback.answer()


# На этапе выбора чемпионата не выбран чемпионат
@router.message(ChooseTable.choosing_competition_name)
async def competition_chosen_incorrectly(message: Message):
    await message.answer(
        text="Для просмотра данных чемпионата нажмите на соответствующую кнопку",
        reply_markup=competition_keyboard(items=available_competition_names)
    )


# Этап выбора таблицы
@router.callback_query(ChooseTable.choosing_table_name,
                       TableCallbackFactory.filter(F.action == "choose"))
async def table_chosen(
        callback: types.CallbackQuery,
        callback_data: TableCallbackFactory,
        state: FSMContext):
    # Получение данных состояний
    user_data = await state.get_data()
    # Вместо сообщения будет выводится выбранная пользователем таблица
    # Соответствующего чемпионата
    await callback.message.answer(
        text="Вы выбрали:\n\n"
             f"Чемпионат <b>{user_data['chosen_competition']}</b>\n"
             f"Таблица <b>{callback_data.text.lower()}</b>",
        reply_markup=ReplyKeyboardRemove()
    )
    await callback.answer()


# На этапе выбора чемпионата нажата кнопка "Назад"
@router.callback_query(ChooseTable.choosing_table_name,
                       TableCallbackFactory.filter(F.action == "cancel"))
async def competition_chosen(
        callback: types.CallbackQuery,
        state: FSMContext):
    await callback.message.answer(
        text="Для просмотра статистики выберите чемпионат",
        # Инлайн-клнопки с чемпионатами
        reply_markup=competition_keyboard(items=available_competition_names)
    )
    # Текущее состояние - выбор таблицы
    await state.set_state(ChooseTable.choosing_competition_name)
    await callback.answer()


# На этапе выбора таблицы не выбрана таблица
@router.message(ChooseTable.choosing_table_name)
async def food_size_chosen_incorrectly(message: Message):
    await message.answer(
        text="Для просмотра данных интересующей таблицы нажмите на соответствующую кнопку",
        reply_markup=table_keyboard(items=available_table_names)
    )


# Нажата кнопка не из текущего сообщения
@router.callback_query()
async def error(callback: types.CallbackQuery):
    await callback.answer(
        text="Ошибка! Обновите меню командой — /menu"
    )
