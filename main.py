from aiogram import Bot, types
from aiogram.types import Message, ParseMode
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import text, bold, italic, code
import logging
import os
import random
import json
try:
    import config as cfg
    import keyboards as kb
    import messages as msg
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
    file = open("users.json", "w")
    file.close()
#==== End ====
async def save_json_file(data: dict):
    with open("users.json", "w", encoding="UTF-8") as file:
         json.dump(data, file, sort_keys=False, ensure_ascii=False)

@dp.message_handler(lambda message: message.text == "Меню")
async def show_menu(message: types.Message):
    await message.answer(text(bold("Меню\n"), "Выберите действие:"), reply_markup=kb.menu_inkb, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(lambda message: message.text == "Инвентарь")
async def show_inventory(message: types.Message):

    txt = users[str(message.from_user.id)]["inventory"][key for key in 
    await message.answer(text(bold("В твоих карманах сейчас:")), reply_markup=kb.inv_inkb)

@dp.message_handler(lambda message: message.text == "Инфо")
async def show_info(message: types.Message):
    await message.answer("Рисую Инфо")

@dp.message_handler(commands=["start"])
async def start_message(message: types.Message):
    if not message.from_user.id in users:
        users[str(message.from_user.id)] = {"first_name": message.from_user["first_name"], "last_name": message.from_user["last_name"], "inventory": {key: None for key in range(0, 6)}}
        save_json_file(users)
    await message.answer(msg.first_message, reply_markup=kb.main_kb)

@dp.message_handler(commands=["help"])
async def help_message(message: types.Message):
    await message.answer(msg.contact_us)

@dp.message_handler(commands=["rkm"])
async def markup_main_kb(message: types.Message):
    await message.reply("Нарисовал кнопки, чтоб было удобнее. Удалить - /rm", reply_markup=kb.main_kb)

@dp.message_handler(commands=["rm"])
async def remove_main_kb(message: types.Message):
    await message.reply("Убираю главное меню. Вернуть - /rkm", reply_markup=kb.ReplyKeyboardRemove())

@dp.callback_query_handler()
async def callback_worker(call: types.CallbackQuery):
    if call.data == "menu":
        await call.message.answer("Menu button")
    elif call.data == "inventory":
        await call.message.answer("Inventory button")
    else:
        await call.message.answer(msg.use_help)
    await call.answer()

@dp.message_handler(content_types=["any"])
async def i_have_lapki(message: types.Message):
   await message.answer(msg.use_help)

if __name__ == '__main__':
    executor.start_polling(dp)
