from aiogram import Bot, types
from aiogram.types import Message, ParseMode
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.utils.exceptions import MessageNotModified
import asyncio
import logging
import os
import random
import json
try:
    import config as cfg
    import keyboards as kb
    import messages as msg
    import plot as pl
    import items
except ModuleNotFoundError:
    raise

bot = Bot(token=cfg.token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
#==== Load users ====
users = {}
if os.path.exists(os.path.join(os.getcwd(), "users.json")):
    with open("users.json", "r", encoding="UTF-8") as file:
        users = json.load(file)
else:
    print("[WARNING] Can't found users.json file in the directory. Created again.")
    save_json_file(users)
#==== End ====
async def save_json_file(data: dict):
    with open("users.json", "w", encoding="UTF-8") as file:
         json.dump(data, file, sort_keys=False, ensure_ascii=False)
#Handlers
@dp.message_handler(lambda message: message.text == "Меню")
async def show_menu(message: types.Message):
    await message.answer(text(bold("Меню\n\n"), "Выберите действие:"), reply_markup=kb.get_menu_inkb(), parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(lambda message: message.text == "Инвентарь")
async def show_inventory(message: types.Message):
    inventory = users[str(message.from_user.id)]["inventory"]
    inv_content = ""
    for idx, val in enumerate(inventory.values()):
        val = "Пусто" if not val else val
        inv_content += f"{idx+1} - " + text(italic(f"{val}; "))
    if inv_content.count("Пусто") < 5:
        await message.answer(text(bold("В твоих карманах сейчас:\n\n"), inv_content), reply_markup=kb.get_inv_slots_inkb(), parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("Твои карманы пока пусты")

@dp.message_handler(lambda message: message.text == "Инфо")
async def show_info(message: types.Message):
    await message.answer(msg.info, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    message_from = message.from_user
    if not str(message_from.id) in users.keys():
        users[str(message_from.id)] = {"first_name": message_from["first_name"], "last_name": message_from["last_name"], "inventory": {key: None for key in range(1, 6)},
                                            "text_delay": 3}
        await save_json_file(users)
    await message.answer(msg.first_message, reply_markup=kb.get_start_inkb(), parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(commands=["help"])
async def help_message(message: types.Message):
    await message.answer(msg.contact_us)

@dp.message_handler(commands=["rkm"])
async def markup_main_kb(message: types.Message):
    await message.reply(msg.rkm, reply_markup=kb.get_main_kb())

@dp.message_handler(commands=["rm"])
async def remove_main_kb(message: types.Message):
    await message.reply(msg.rm, reply_markup=kb.ReplyKeyboardRemove())

@dp.message_handler(commands=["delay"])
async def change_text_delay(message: types.Message):
    argument = message.get_args()
    if not argument.isdigit() or int(argument) > 8 or int(argument) < 0:
        return await message.answer(text("Используйте команду /delay", bold("цифра") + "(0-8)"), parse_mode=ParseMode.MARKDOWN)
    users[str(message.from_user.id)]["text_delay"] = argument
    await save_json_file(users)
    await message.answer(text("Задержка появления текста теперь", bold(f"{argument}")), parse_mode=ParseMode.MARKDOWN)
#Callbacks
@dp.callback_query_handler(text="les_go")
async def callback_les_go(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup="")
    await call.message.answer(text="Приятного путешествия!", reply_markup=kb.get_main_kb())
    user = users[str(call.from_user.id)]
    plot = pl.Plot(int(user['text_delay']), msg.plot["Prologue"])
    await plot.print_paragraph(call, 1)
    await call.answer()

@dp.callback_query_handler(kb.paragraph_cb.filter())
async def callback_paragraph_buttons(call: types.CallbackQuery, callback_data:dict):
    key = callback_data["key"]

    await call.answer()

@dp.callback_query_handler(kb.menu_cb.filter())
async def callback_menu(call: types.CallbackQuery, callback_data:dict):
    assign = callback_data["assign"]
    if assign == "plot":
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup="")
    elif assign == "settings_menu":
        sms = text(bold("Настройки\n\n"), "Задержка появления текста:", bold(f"{users[str(call.from_user.id)]['text_delay']}"))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=sms, reply_markup=kb.get_settings_inkb(), parse_mode=ParseMode.MARKDOWN)
    await call.answer()

@dp.callback_query_handler(kb.settings_cb.filter())
async def callback_settings(call: types.CallbackQuery, callback_data:dict):
    assign = callback_data["assign"]
    if assign == "text_delay":
        sms = text(bold(f"Задержка появления текста: {users[str(call.from_user.id)]['text_delay']}\n\n") + "Выберите новое значение")
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=sms, reply_markup=kb.get_text_delay_inkb(), parse_mode=ParseMode.MARKDOWN)
    elif assign == "settings_close":
       await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup="")
    await call.answer()

@dp.callback_query_handler(kb.inv_slots_cb.filter())
async def callback_inventory(call: types.CallbackQuery, callback_data:dict):
    slot_number = callback_data["number"]
    inventory_slot = users[str(call.from_user.id)]["inventory"][slot_number] # Get the content of slot
    if inventory_slot: # if not empty
        can_drop = False
        sms = f"Выберите действие для кармана {slot_number}"
        if not items.item[inventory_slot].get("is_plot_obj", False): # Check is the item in slot is plot object(n = can drop)
            can_drop = True # You can drop it
            sms += "\n\n(Предмет исчезнет, если его выбросить)"
        mes_id = call.message.message_id
        await call.message.answer(text=sms, reply_markup=kb.get_inv_actions_inkb(mes_id, slot_number, can_drop))
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=mes_id, reply_markup="")
        await call.answer()
    else: # if empty
        await call.answer(text="Карман пуст!", show_alert=True)

@dp.callback_query_handler(kb.inv_actions_cb.filter())
async def callback_inventory_actions(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "use": # Not now
        pass
    elif action == "drop":
        slot_number = int(callback_data["slot_number"])
        users[str(call.from_user.id)]["inventory"][slot_number] = None
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Теперь карман {slot_number} пуст", reply_markup="")
    elif action == "inv_back":
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=callback_data["inv_mes_id"], reply_markup=kb.get_inv_slots_inkb()) #Return to inventory message keyb
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id) #delete this msg
    await call.answer()

@dp.callback_query_handler(kb.text_delay_cb.filter())
async def callback_change_text_delay(call: types.CallbackQuery, callback_data:dict):
    value = callback_data.get("value", 0)
    users[str(call.from_user.id)]["text_delay"] = value
    await save_json_file(users)
    sms = text("Задержка появления текста теперь", bold(f"{value}"))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=sms, reply_markup="", parse_mode=ParseMode.MARKDOWN)
    await call.answer()

@dp.message_handler(content_types=["any"])
async def i_have_lapki(message: types.Message):
   await message.answer(msg.use_help)

@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    return True #pass

if __name__ == '__main__':
    executor.start_polling(dp)
