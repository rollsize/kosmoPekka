from aiogram import Bot, types
from aiogram.types import Message, ParseMode
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.utils.exceptions import MessageNotModified
import asyncio
import logging
import os
import json
try:
    import app.config as cfg
    import app.keyboards as kb
    import app.messages as msg
    import app.plot as pl
    import app.items as items
except ModuleNotFoundError:
    raise

bot = Bot(token=cfg.token)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
#==== Load users ====
users = {}
def save_json_file(data: dict):
    with open("users.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, sort_keys=False, ensure_ascii=False)

if os.path.exists(os.path.join(os.getcwd(), "users.json")):
    with open("users.json", "r", encoding="UTF-8") as file:
        users = json.load(file)
else:
    print("[WARNING] Can't found users.json file in the directory. Created again.")
    save_json_file(users)
#==== End ====

async def compile_paragraph(user: dict, callback: types.CallbackQuery, paragraph_num:str = "1"):
    paragraph = msg.plot[cfg.current_chapter][f"Paragraph_{paragraph_num}"]
    receive = None
    for elem in paragraph.keys():
        if type(elem) != int: continue
        receive = paragraph[elem].get("Receive", False)
        break
    if receive:
        for idx in range(1, 6):
            if user["inventory"][str(idx)]: continue #if not empty - next
            user["inventory"][str(idx)] = receive.get("Name", None)
            break
        save_json_file(users)
    await pl.Plot(int(user["text_delay"]), msg.plot, cfg.current_chapter).print("paragraph", callback, pr_number=paragraph_num)
#Handlers
async def show_menu(message: Message):
    await message.answer(text(bold("Меню\n\n"), "Выберите действие:"), reply_markup=kb.get_menu_inkb(), parse_mode=ParseMode.MARKDOWN)

async def show_inventory(message: Message):
    inventory = users[str(message.from_user.id)]["inventory"]
    inv_content = ""
    for idx, val in enumerate(inventory.values()):
        val = "Пусто" if not val else val
        inv_content += f"{idx+1} - " + text(italic(f"{val}; "))
    if inv_content.count("Пусто") < 5:
        await message.answer(text(bold("В твоих карманах сейчас:\n\n"), inv_content), reply_markup=kb.get_inv_slots_inkb(), parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("Твои карманы пока пусты")

async def show_info(message: Message):
    await message.answer(msg.info, parse_mode=ParseMode.MARKDOWN)

async def start_message(message: Message):
    await dp.bot.set_my_commands([types.BotCommand(command="/menu", description="Открыть меню"), types.BotCommand(command="/help", description="Помощь"),
        types.BotCommand(command="/settings", description="Открыть настройки"), types.BotCommand(command="/inv", description="Открыть инвентарь"), 
        types.BotCommand(command="/rm", description="Удалить основную клавиатуру"), types.BotCommand(command="/rkm", description="Вернуть основную клавиатуру"),
        types.BotCommand(command="/delay", description="Установить задержку появления текста (/delay 0-8)")]) # set bot commands
    message_from = message.from_user
    if not str(message_from.id) in users.keys(): # if not exist
        users[str(message_from.id)] = {"first_name": message_from["first_name"], "last_name": message_from["last_name"], "inventory": {key: None for key in range(1, 6)},
                                        "text_delay": 3}
        save_json_file(users)
    await message.answer(msg.first_message, reply_markup=kb.get_start_inkb(), parse_mode=ParseMode.MARKDOWN)

async def help_message(message: Message):
    await message.answer(msg.contact_us)

async def markup_main_kb(message: Message):
    await message.reply(msg.rkm, reply_markup=kb.get_main_kb())

async def remove_main_kb(message: Message):
    await message.reply(msg.rm, reply_markup=kb.ReplyKeyboardRemove())

async def change_text_delay(message: Message):
    argument = message.get_args()
    if not argument.isdigit() or int(argument) > 8 or int(argument) < 0:
        return await message.answer(text("Используйте команду /delay", bold("цифра") + "(0-8)"), parse_mode=ParseMode.MARKDOWN)
    users[str(message.from_user.id)]["text_delay"] = argument
    save_json_file(users)
    await message.answer(text("Задержка появления текста теперь", bold(f"{argument}")), parse_mode=ParseMode.MARKDOWN)

#Register handlers
dp.register_message_handler(start_message, commands="start", state="*")
dp.register_message_handler(show_menu, Text(equals="Меню", ignore_case=True), state="*")
dp.register_message_handler(show_menu, commands="menu", state="*")
dp.register_message_handler(help_message, commands="help", state="*")
dp.register_message_handler(show_inventory, Text(equals="инвентарь", ignore_case=True), state="*")
dp.register_message_handler(show_inventory, commands="inv", state="*")
dp.register_message_handler(change_text_delay, commands="delay", state="*")
dp.register_message_handler(show_info, Text(equals="Инфо", ignore_case=True), state="*")
dp.register_message_handler(show_info, commands="info", state="*")
dp.register_message_handler(markup_main_kb, commands="rkm", state="*")
dp.register_message_handler(remove_main_kb, commands="rm", state="*")

#Callbacks
@dp.callback_query_handler(text="les_go", state="*")
async def callback_les_go(call: types.CallbackQuery):
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup="")
    await call.message.answer(text="Приятного путешествия!", reply_markup=kb.get_main_kb())
    user = users[str(call.from_user.id)]
    await compile_paragraph(user, call)
    await call.answer()

@dp.callback_query_handler(kb.paragraph_cb.filter(), state="*") #state=pl.Plot_Branch.waiting_for_choise)
async def callback_paragraph_buttons(call: types.CallbackQuery, callback_data:dict, state:FSMContext):
    paragraph = callback_data["paragraph"] # Get the number of paragraph
    txt_key = callback_data["txt_key"] # Get the key of part to print for messages.py
    order = int(callback_data["order"])+1 # Increase current order
    await state.update_data(cur_order = order, button_txt=txt_key)
    user = users[str(call.from_user.id)]
    await pl.Plot(int(user['text_delay']), msg.plot, cfg.current_chapter).print("branching", call, pr_number=paragraph, part=txt_key, state=state)
    
    await call.answer()

@dp.callback_query_handler(kb.continue_paragraph_cb.filter(), state="*")
async def callback_continue_paragraph(call: types.CallbackQuery, callback_data:dict):
    paragraph = callback_data.get("continue_paragraph", 1)
    user = users[str(call.from_user.id)]
    await compile_paragraph(user, call, paragraph)
    await call.answer()


@dp.callback_query_handler(kb.menu_cb.filter(), state="*")
async def callback_menu(call: types.CallbackQuery, callback_data:dict):
    assign = callback_data.get("assign", False)
    if assign == "plot":
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup="")
    elif assign == "settings_menu":
        sms = text(bold("Настройки\n\n"), "Задержка появления текста:", bold(f"{users[str(call.from_user.id)]['text_delay']}"))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=sms, reply_markup=kb.get_settings_inkb(), parse_mode=ParseMode.MARKDOWN)
    await call.answer()

@dp.callback_query_handler(kb.inv_slots_cb.filter(), state="*")
async def callback_inventory(call: types.CallbackQuery, callback_data:dict):
    slot_number = callback_data.get("number", 0)
    inventory_slot = users[str(call.from_user.id)]["inventory"][slot_number] # Get the content of slot
    if inventory_slot: # if not empty
        can_drop = False
        sms = f"Выберите действие для кармана {slot_number}({inventory_slot})"
        if not items.item[inventory_slot].get("is_plot_obj", False): # Check is the item in slot is plot object(n = can drop)
            can_drop = True # You can drop it
            sms += "\n\n(Предмет исчезнет, если его выбросить)"
        mes_id = call.message.message_id
        await call.message.answer(text=sms, reply_markup=kb.get_inv_actions_inkb(mes_id, slot_number, can_drop))
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=mes_id, reply_markup="")
        await call.answer()
    else: # if empty
        await call.answer(text="Карман пуст!", show_alert=True)

@dp.callback_query_handler(kb.inv_actions_cb.filter(), state="*")
async def callback_inventory_actions(call: types.CallbackQuery, callback_data: dict):
    action = callback_data.get("action", False)
    if action == "drop":
        slot_number = int(callback_data["slot_number"])
        users[str(call.from_user.id)]["inventory"][slot_number] = None
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Теперь карман {slot_number} пуст", reply_markup="")
    elif action == "inv_back":
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=callback_data["inv_mes_id"], reply_markup=kb.get_inv_slots_inkb()) #Return to inventory message keyb
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id) #delete this msg
    await call.answer()

@dp.callback_query_handler(kb.settings_cb.filter(), state="*")
async def callback_settings(call: types.CallbackQuery, callback_data:dict):
    assign = callback_data.get("assign", False)
    if assign == "text_delay":
        sms = text(bold(f"Задержка появления текста: {users[str(call.from_user.id)]['text_delay']}\n\n") + "Выберите новое значение")
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=sms, reply_markup=kb.get_text_delay_inkb(), parse_mode=ParseMode.MARKDOWN)
    elif assign == "settings_close":
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup="")
    await call.answer()

@dp.callback_query_handler(kb.text_delay_cb.filter(), state="*")
async def callback_change_text_delay(call: types.CallbackQuery, callback_data:dict):
    value = callback_data.get("value", False)
    users[str(call.from_user.id)]["text_delay"] = value
    save_json_file(users)
    sms = text("Задержка появления текста теперь", bold(f"{value}"))
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=sms, reply_markup="", parse_mode=ParseMode.MARKDOWN)
    await call.answer()

@dp.message_handler(content_types=["any"], state="*")
async def i_have_lapki(message: Message):
    await message.answer(msg.use_help)

@dp.errors_handler(exception=MessageNotModified)
async def message_not_modified_handler(update, error):
    return True #pass

async def shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()
    
if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)