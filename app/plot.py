import asyncio
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.keyboards import get_paragraph_branch_kb, get_paragraph_continue_kb

class Plot():
    def __init__(self, delay:int, plot_location:dict, cur_chapter:str):
        self._text_delay = delay
        self._plot_location = plot_location
        self._current_chapter = cur_chapter

    def _load_pr(self, number:str):
        try:
            self._paragraph = self._plot_location[self._current_chapter][f"Paragraph_{number}"]
        except KeyError:
            raise KeyError(f"[ERROR] Can't find Paragraph_{number} in destination({self._plot_location})")
        self._lenght = len(self._paragraph)
        self._texts, self._buttons = [], []
        for elem in self._paragraph.keys():
            if type(elem) != int: continue
            txt = self._paragraph[elem].get("Text", False)
            if not txt: continue
            self._texts.append(txt)
            branch = self._paragraph[elem].get("Branch", False)
            if not branch: 
                self._buttons.append(branch) # add False
                continue
            self._buttons.append(self._plot_location["Branching"][f"Paragraph_{number}"]["Buttons"]) # else
        return self._texts, self._buttons, self._lenght

    async def print(self, what:str, callback:CallbackQuery, pr_number:str = "1", part:str = None, state:FSMContext = None):
        if what == "branching":
            try:
                self._paragraph = self._plot_location[self._current_chapter][f"Paragraph_{pr_number}"]
            except KeyError:
                raise KeyError(f"[ERROR] Can't find Paragraph_{pr_number} in destination({self._plot_location})")

            self._btns = self._plot_location["Branching"][f"Paragraph_{int(pr_number)-1}"]["Buttons"]
            self._btns_lenght = len(self._btns)
            self._btn_data = await state.get_data()
            self._current_order = int(self._btn_data["cur_order"])
            for idx in range(self._btns_lenght):
                self._btns[idx][2] = self._current_order # set to all buttons current count of order
                if self._btns[idx][0] ==  self._btn_data["button_txt"]: # If button were clicked
                    self._btns[idx][3] = True # "use" = True
            
            self._txt = ""
            self._branching_order = self._plot_location["Branching"][f"Paragraph_{int(pr_number)-1}"].get("Order", False)
            if self._branching_order:
                self._txt += self._branching_order[self._btn_data["cur_order"]] + self._btn_data["button_txt"] + "\n"
            self._txt += self._paragraph[part].get("Text", False)
            self._repl_markup = get_paragraph_branch_kb(self._btns)
            if self._current_order == self._btns_lenght:
                self._repl_markup = get_paragraph_continue_kb(pr_number)
            await callback.message.answer(text=self._txt, parse_mode=ParseMode.MARKDOWN, reply_markup=self._repl_markup)

        elif what == "paragraph":
            self._txt, self._buttons, self._paragraph_len = self._load_pr(pr_number)
            for idx in range(0, self._paragraph_len):
                if self._buttons[idx]:
                    await callback.message.answer(text=self._txt[idx], reply_markup=get_paragraph_branch_kb(self._buttons[idx]), parse_mode=ParseMode.MARKDOWN)
                    #await Plot_Branch.waiting_for_choise.set()
                    return
                await callback.message.answer(text=self._txt[idx], parse_mode=ParseMode.MARKDOWN)
                await asyncio.sleep(self._text_delay)

#class Plot_Branch(StatesGroup):
    #waiting_for_choise = State()