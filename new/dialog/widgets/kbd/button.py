from typing import List, Callable, Optional, Union

from aiogram.types import InlineKeyboardButton, CallbackQuery

from dialog.dialog import Dialog
from dialog.manager.manager import DialogManager
from dialog.widgets.text import Text
from .base import Keyboard


class Button(Keyboard):
    def __init__(self, text: Text, callback_data: str, on_click: Optional[Callable] = None,
                 when: Union[str, Callable] = None):
        super().__init__(when)
        self.text = text
        self.callback_data = callback_data
        self.on_click = on_click

    async def process_callback(self, c: CallbackQuery, dialog: Dialog, manager: DialogManager) -> bool:
        if c.data != self.callback_data:
            return False
        if self.on_click:
            await self.on_click(c, dialog, manager)
        return True

    async def _render_kbd(self, data) -> List[List[InlineKeyboardButton]]:
        return [[
            InlineKeyboardButton(
                text=await self.text.render_text(data),
                callback_data=self.callback_data
            )
        ]]


class Uri(Keyboard):
    def __init__(self, text: Text, uri: Text, when: Union[str, Callable, None] = None):
        super().__init__(when)
        self.text = text
        self.uri = uri

    async def _render_kbd(self, data) -> List[List[InlineKeyboardButton]]:
        return [[
            InlineKeyboardButton(
                text=await self.text.render_text(data),
                uri=await self.uri.render_text(data)
            )
        ]]
