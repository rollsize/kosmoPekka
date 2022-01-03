from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
for txt in ["Меню", "Инвентарь", "Инфо"]:
    main_kb.insert(KeyboardButton(text=txt))
####
menu_inkb = InlineKeyboardMarkup(row_width=2)
menu_inkb.insert(InlineKeyboardButton(text="Сюжет", callback_data="menu"))

####
inv_inkb = InlineKeyboardMarkup(row_width=3)
for idx in range(1, 6):
    inv_inkb.insert(InlineKeyboardButton(text=idx, callback_data="inv"))