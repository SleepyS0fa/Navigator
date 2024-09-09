from aiogram import Router
from aiogram.types import CallbackQuery, Message

router = Router()


@router.callback_query()
async def not_found(call: CallbackQuery):
    await call.answer()
    await call.message.answer(
        "Отправлен неизвестный id.\nВозможно произошло обновление базы, попробуйте обновить список")


@router.message()
async def not_found(message: Message):
    await message.answer("Не извесная команда")
