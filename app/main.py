import logging
import random
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiohttp import web

from const import WELCOME_MESSAGE, CHOICES, WIN_MESSAGE, LOSE_MESSAGE, DRAW_MESSAGE

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем токен бота и порт из переменных окружения
BOT_TOKEN = getenv("BOT_TOKEN")
PORT = int(getenv("PORT", 8080))

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(WELCOME_MESSAGE)

# Обработчик сообщений
@dp.message()
async def play_game(message: Message):
    user_choice = message.text.lower()
    if user_choice not in CHOICES:
        await message.answer("Выберите: камень, ножницы или бумага.")
        return

    bot_choice = random.choice(CHOICES)
    result = determine_winner(user_choice, bot_choice)

    await message.answer(f"Ты выбрал: {user_choice.capitalize()}\nЯ выбрал: {bot_choice.capitalize()}\n{result}")

def determine_winner(user: str, bot: str) -> str:
    """Определяет победителя"""
    if user == bot:
        return DRAW_MESSAGE
    if (user == "камень" and bot == "ножницы") or \
       (user == "ножницы" and bot == "бумага") or \
       (user == "бумага" and bot == "камень"):
        return WIN_MESSAGE
    return LOSE_MESSAGE

# Webhook обработка
routes = web.RouteTableDef()

@routes.get("/")
async def index(request):
    return web.Response(text="Бот работает!")

@routes.post(f"/{BOT_TOKEN}")
async def webhook_handler(request):
    request_data = await request.json()
    update = types.Update(**request_data)
    await dp._process_update(bot=bot, update=update)
    return web.Response(text="OK")

# Запуск бота
if __name__ == "__main__":
    logger.info("Бот запущен...")

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host="0.0.0.0", port=PORT)