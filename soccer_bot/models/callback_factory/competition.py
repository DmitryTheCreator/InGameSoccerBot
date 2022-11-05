from typing import Optional
from aiogram.dispatcher.filters.callback_data import CallbackData


class CompetitionCallbackFactory(CallbackData, prefix="fabcomp"):
    action: str
    text: Optional[str]
