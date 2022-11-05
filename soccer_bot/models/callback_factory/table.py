from typing import Optional
from aiogram.dispatcher.filters.callback_data import CallbackData


class TableCallbackFactory(CallbackData, prefix="fabtable"):
    action: str
    text: Optional[str]
