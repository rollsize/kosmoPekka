import asyncio
from aiogram.types import Message, CallbackQuery
from keyboards import get_paragraph_kb

class Plot():
    def __init__(self, delay:int, plot_location:dict):
        self._text_delay = delay
        self._plot_location = plot_location

    def _load_pr(self):
        pass

    async def print_paragraph(self, callback:CallbackQuery, number:int):
        try:
            self._paragraph = self._plot_location[f"Paragraph_{number}"]
        except KeyError:
            raise KeyError(f"[ERROR] Can't find Paragraph_{number} in destination({self._plot_location})")
        for idx in range(1, len(self._paragraph)+1):
            self._sms = self._paragraph[idx]["Text"]
            self._buttons = self._paragraph[idx].get("Buttons", False)
            if buttons:
                await callback.message.answer(text=self._sms, reply_markup=get_paragraph_kb(self._buttons))
                break
            else:
                await callback.message.answer(text=self._sms)
                await asyncio.sleep(self._text_delay)

    