import logging
import aiofiles
from aiogram import Bot, Dispatcher, executor
from aiogram.types import ContentType, Message
from config import BOT_TOKEN
from main import main
from random import choice

logging.basicConfig(level=logging.INFO)
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)

fail_phrases = ["Прости, плохо слышно, не понимаю...", "Что-то я отвлекся, повтори еще раз.",
                "Похоже мы плохо друг друга понимаем. Введи /help и я тебе подскажу."]


@dp.message_handler(commands=["start", "help"])
async def greeting(message: Message):
    return await message.answer("Привет! Нажми /get чтобы получить все домашнее задание")


@dp.message_handler(commands=["get"])
async def get_homework(message: Message):
    await message.answer("Подожди...")
    src = await main()
    return await message.answer_document(await aiofiles.open(src, "rb"))


@dp.message_handler(content_types=ContentType.TEXT)
async def another(message: Message):
    phrase = choice(fail_phrases)
    return await message.answer(phrase)


if __name__ == '__main__':
    executor.start_polling(dp)
