from aiogram import Router, F
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import keyboard
from FSM import UserState
from data_base import MongoDB

router = Router()

db = MongoDB()
db.set_collection("faq")
STEP = 8
BACK_STEP = STEP * 2


@router.message(UserState.use_bot, F.text == "FAQ, контакты")
async def command_start_handler(message: Message, state: FSMContext) -> None:
    faq_list = await db.get_faq_question_list(limit=STEP, skip=0)
    count = await db.get_faq_count()
    await state.update_data(pointer_faq=STEP, count_faq=count)
    await message.answer("Здесь список самых часто задаваемых вопросов.\nЕсли же нужного вопроса нет, то можно "
                         "обратиться к нам напрямую\n Телефон: +9(999) 999-99-99 \n Почта: edu@example.com",
                         reply_markup=keyboard.page_faq_keyboard(faq_list))


@router.callback_query(F.data.startswith("cbfaq_"))
async def select_prof(call: CallbackQuery) -> None:
    question_id = call.data.replace("cbfaq_", "")
    faq_doc = await db.get_faq_question(question_id)
    request = r"" + faq_doc.get('question') + "\n\n" + faq_doc.get('answer').replace(r"\n", "\n")

    await call.message.answer(request)
    await call.answer()


@router.callback_query(F.data == "faq_next")
async def callback(call: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_pointer = user_data.get("pointer_faq")
    if user_pointer >= user_data.get("count_faq"):
        await call.answer()
        return

    data_list = await db.get_faq_question_list(limit=STEP,
                                               skip=user_pointer)
    await state.update_data(pointer_faq=user_pointer + STEP)
    await call.message.edit_text(text="Вот, что нам удалось найти",
                                 reply_markup=keyboard.page_faq_keyboard(data_list))


@router.callback_query(F.data == "faq_previous")
async def callback(call: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_pointer = user_data.get("pointer_faq")
    if user_pointer <= STEP:
        await call.answer()
        return

    data_list = await db.get_faq_question_list(limit=STEP,
                                               skip=(user_pointer - BACK_STEP))
    await state.update_data(pointer_faq=user_pointer - STEP)
    await call.message.edit_text(text="Вот, что нам удалось найти",
                                 reply_markup=keyboard.page_faq_keyboard(data_list))

