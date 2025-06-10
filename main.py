# pip install aiogram aiohttp gigachat
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from gigachat import GigaChat

# Токены
BOT_TOKEN = "7738648766:AAHcXsUWJDYHpUSnBXEtAtJjsGG_GAPpUA0"
GIGACHAT_AUTH_KEY = "NjllM2E5NDktZTFiNC00YjMyLWE2ZDgtMDk0MWQ2MmJhNjMyOjc0YzlkNTQ4LWUzYzctNDM4Zi04MjkwLTVhNjQzNjdkMDE2OA=="  # Ключ авторизации из личного кабинета

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def query_ai(text: str) -> str:
    """Запрос к GigaChat для определения игры"""
    prompt = f"""Ты эксперт по видеоиграм. Определи популярную видеоигру по описанию: "{text}"

Ответь кратко в формате:
🎮 Игра: [название]
📂 Жанр: [жанр] 
📝 Почему: [краткое объяснение]

Если не уверен - предложи 2-3 варианта."""

    try:
        # Используем GigaChat Pro для получения ответа
        with GigaChat(
            credentials=GIGACHAT_AUTH_KEY,
            scope="GIGACHAT_API_PERS",  # Версия API для физлиц
            verify_ssl_certs=False,  # Отключение проверки SSL, в продакшене рекомендуется установить сертификат НУЦ Минцифры
            model="GigaChat-Pro"  # Явно указываем использование модели GigaChat-Pro
        ) as giga:
            response = giga.chat(prompt)
            return response.choices[0].message.content
    except Exception as e:
        return f"❌ Ошибка ИИ сервиса: {str(e)}"

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "🎮 Привет! Я ИИ-бот для определения видеоигр!\n\n"
        "Опишите игру и я скажу что это за игра.\n"
        "Работаю на продвинутой модели GigaChat Pro."
    )

@dp.message()
async def game_handler(message: Message):
    # Показываем что бот печатает
    await bot.send_chat_action(message.chat.id, "typing")
    
    # Запрос к ИИ
    ai_response = await query_ai(message.text)
    await message.answer(ai_response)

async def main():
    print("🤖 ИИ-бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
