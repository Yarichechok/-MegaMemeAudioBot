import asyncio
import logging
import os
from dotenv import load_dotenv

load_dotenv()

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.session.aiohttp import AiohttpSession

from handlers import admin, inline, user

TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

proxy_url = "http://proxy.server:3128"
session = AiohttpSession(proxy=proxy_url)

bot = Bot(token=TOKEN, session=session)

dp = Dispatcher()

dp.include_router(admin.router)
dp.include_router(user.router)
dp.include_router(inline.router)

async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command="/start", description="🚀 Головне меню"),
        BotCommand(command="/random", description="🎲 Випадковий мем"),
        BotCommand(command="/help", description="❓ Як користуватися")
    ]
    await bot.set_my_commands(main_menu_commands)

async def main():
    print("Бот запущений (v2.4 PA Proxy)...")
    await set_main_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнений")