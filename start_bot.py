import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.mongo import MongoStorage
from aiogram.methods import DeleteWebhook
from aiogram.types import Message, CallbackQuery
from motor.motor_asyncio import AsyncIOMotorClient

import keyboard
import settings
from FSM import UserState

from routers import start_router
from routers import professions_router
from routers import organizations_router
from routers import faq_router
"""Develop by SleepySofa"""

TOKEN = settings.TOKEN

client = AsyncIOMotorClient(settings.DB)

dp = Dispatcher(storage=MongoStorage(client, db_name="navigator", collection_name="fsm"))
dp.include_router(start_router.router)
dp.include_router(professions_router.router)
dp.include_router(organizations_router.router)
dp.include_router(faq_router.router)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
