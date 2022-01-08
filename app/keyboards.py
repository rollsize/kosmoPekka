from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

menu_cb = CallbackData("menu", "assign")
settings_cb = CallbackData("settings", "assign")
inv_actions_cb = CallbackData("inv_actions", "inv_mes_id", "action", "slot_number")
inv_slots_cb = CallbackData("inventory", "number")
text_delay_cb = CallbackData("new_text_delay", "value")
paragraph_cb = CallbackData("pr_keyboard", "paragraph", "txt_key", "order")
continue_paragraph_cb = CallbackData("next_pr_button", "continue_paragraph")

def get_start_inkb():
    start_inkb = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Поехали!", callback_data="les_go"))
    return start_inkb

def get_main_kb():
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for txt in ["Меню", "Инвентарь", "Инфо"]:
        main_kb.insert(KeyboardButton(text=txt))
    return main_kb
####
def get_menu_inkb():
    menu_inkb = InlineKeyboardMarkup(row_width=3)
    menu_inkb.insert(InlineKeyboardButton(text="Сюжет", callback_data=menu_cb.new(assign="plot")))
    menu_inkb.insert(InlineKeyboardButton(text="Настройки", callback_data=menu_cb.new(assign="settings_menu")))
    return menu_inkb
####
def get_settings_inkb():
    settings_inkb = InlineKeyboardMarkup(row_width=3)
    settings_inkb.insert(InlineKeyboardButton(text="Изменить задержку", callback_data=settings_cb.new(assign="text_delay")))
    settings_inkb.add(InlineKeyboardButton(text="Закрыть", callback_data=settings_cb.new(assign="settings_close")))
    return settings_inkb
####
def get_inv_actions_inkb(inv_mes_id:str, slot_number:str, can_drop=True):
    inv_actions_inkb = InlineKeyboardMarkup(row_width=2)
    #inv_actions_inkb.insert(InlineKeyboardButton(text="Использовать", callback_data=inv_actions_cb.new(action="use")))
    if can_drop:
        inv_actions_inkb.insert(InlineKeyboardButton(text="Выбросить", callback_data=inv_actions_cb.new(inv_mes_id=inv_mes_id,action="drop", slot_number=slot_number)))
    inv_actions_inkb.add(InlineKeyboardButton(text="Назад", callback_data=inv_actions_cb.new(inv_mes_id=inv_mes_id,action="inv_back", slot_number="0")))
    return inv_actions_inkb

def get_inv_slots_inkb():
    inv_slots_inkb = InlineKeyboardMarkup(row_width=3)
    for idx in range(1, 6):
        inv_slots_inkb.insert(InlineKeyboardButton(text=idx, callback_data=inv_slots_cb.new(number=idx)))
    return inv_slots_inkb
####
def get_text_delay_inkb():
    delay_inkb = InlineKeyboardMarkup(row_width=4)
    for idx in range(0, 9):
        delay_inkb.insert(InlineKeyboardButton(text=idx, callback_data=text_delay_cb.new(value=idx)))
    return delay_inkb
####
def get_paragraph_branch_kb(buttons:list):
    paragraph_branch = InlineKeyboardMarkup(row_width=3)
    for idx in range(len(buttons)):
        txt, point_to, order, is_used = buttons[idx]
        if not is_used:
            paragraph_branch.insert(InlineKeyboardButton(text=txt, callback_data=paragraph_cb.new(paragraph=point_to, txt_key=txt, order=order)))
    return paragraph_branch

def get_paragraph_continue_kb(continue_paragraph:str):
    continue_kb = InlineKeyboardMarkup()
    continue_kb.add(InlineKeyboardButton(text="Продолжить", callback_data=continue_paragraph_cb.new(continue_paragraph=continue_paragraph)))

    return continue_kb