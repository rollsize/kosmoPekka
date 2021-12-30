from aiogram import Bot, types
from aiogram.types import Message, Update, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions
import logging
import os
import random
import json
try:
    import config as cfg
except ModuleNotFoundError:
    raise ModuleNotFoundError("[ERROR] No config.py file in the directory")
try:
    import messages as msg
except ModuleNotFoundError:
    raise ModuleNotFoundError("[ERROR] No messages.py file in the directory")
# Сделать команды на основные кнопки
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

@dp.errors_handler(exception=exceptions.BotBlocked)
async def error_bot_blocked(update: types.Update, exception: exceptions.BotBlocked):
    print(update)
    print(f"[WARNING]User blocked me!\Message: {update}\nОшибка: {exception}")
    return True

@dp.message_handler(commands=["start"])
async def welcome_message(message: types.Message):
    if not message.from_user.id in users:
        users[str(message.from_user.id)] = {"first_name": message.from_user["first_name"], "last_name": message.from_user["last_name"], "inventory": {key: None for key in range(0, 6)}}
        await save_json_file(users) 
    welcome_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb_keys = []
    kb_keys.append(KeyboardButton(text="Меню", call_data="Menu"))
    kb_keys.append(KeyboardButton(text="Инвентарь", call_data="Invent"))
    kb_keys.append(KeyboardButton(text="Инфо", call_data="Info"))
    welcome_keyboard.add(*kb_keys)
    await message.answer(msg.first_message, reply_markup=welcome_keyboard)

@dp.message_handler(commands=["help"])
async def credits(message: types.Message):
    await message.answer(msg.contact_us)

@dp.callback_query_handler(lambda call:True)
async def callback_worker(call):
    if call.data == "Menu":
        await message.answer("You picked 'Yes'")

if __name__ == '__main__':
    executor.start_polling(dp)
