import asyncio
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.keyboards import get_paragraph_kb

class Plot():
    def __init__(self, delay:int, plot_location:dict, cur_chapter:str):
        self._text_delay = delay
        self._plot_location = plot_location
        self._current_chapter = cur_chapter

    def _load_pr(self, number:int):
        try:
            self._paragraph = self._plot_location[self._current_chapter][f"Paragraph_{number}"]
        except KeyError:
            raise KeyError(f"[ERROR] Can't find Paragraph_{number} in destination({self._plot_location})")
        self._lenght = len(self._paragraph)
        self._texts, self._buttons = [], []
        for idx in range(1, self._lenght+1):
            txt = self._paragraph.get([idx], False)
            if not txt: continue
            self._texts.append(self._paragraph.get([idx], False)
            branch = self._paragraph[idx].get("Branch", False)
            if not branch:
                self._buttons.append(branch)
                continue
            self._buttons.append(self._plot_location["Branching"][f"Paragraph_{number}"]["Buttons"]) # else
        return self._texts, self._buttons, self._lenght

    async def print(self, what:str, callback:CallbackQuery, number:int=None):
        if what == "branching":
            pass
        elif what == "paragraph":
            self._txt, self._buttons, self._paragraph_len = self._load_pr(number)
            for idx in range(0, self._paragraph_len):
                if self._buttons[idx]:
                    await callback.message.answer(text=self._txt[idx], reply_markup=get_paragraph_kb(self._buttons[idx]), parse_mode=ParseMode.MARKDOWN)
                    return await Plot_Branch.waiting_for_choise.set()
                else:
                    await callback.message.answer(text=self._txt[idx], parse_mode=ParseMode.MARKDOWN)
                    await asyncio.sleep(self._text_delay)

class Plot_Branch(StatesGroup):
    waiting_for_choise = State()