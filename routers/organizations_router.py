from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import keyboard
from FSM import UserState
from data_base import MongoDB

router = Router()

db = MongoDB()
STEP = 10
BACK_STEP = STEP * 2


@router.message(UserState.use_bot, F.text == "Перечень образовательных организаций")
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    college_list = await db.get_college_by_type(filter_user=user_data.get("type"), limit=STEP, skip=0)
    count = await db.get_college_count_by_type(user_data.get("type"))
    await state.update_data(pointer_college=STEP, count_college=count.get("count"))
    await message.answer("Вот, что нам удалось найти", reply_markup=keyboard.page_college_keyboard(college_list))


@router.callback_query(F.data.startswith("cbcollege_"))
async def select_prof(call: CallbackQuery, state: FSMContext) -> None:
    college_hash = call.data.replace("cbcollege_", "")
    user_data = await state.get_data()
    college_list = await db.get_prof_by_college(user_data.get("type"), college_hash)

    college_text = college_list["_id"]["college"] + "\n"
    if "link" in college_list["_id"]:
        college_text += f"Официальный сайт: {college_list['_id']['link']}\n"
    if "socnet" in college_list["_id"]:
        college_text += f"Социальная сеть: {college_list['_id']['socnet']}\n"
    college_text += "\nСпециальности:" + "\n"
    prof_text = ""
    print(college_list["profs"])
    for prof in college_list["profs"]:
        prof_text += prof["code"] + " "
        prof_text += prof["prof"] + "\n"
    await call.message.answer(college_text + prof_text)
    await call.answer()


@router.callback_query(F.data == "college_next")
async def callback(call: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_pointer = user_data.get("pointer_college")
    if user_pointer >= user_data.get("count_college"):
        await call.answer()
        return

    data_list = await db.get_college_by_type(filter_user=user_data.get("type"),
                                             limit=STEP,
                                             skip=user_pointer)
    await state.update_data(pointer_college=user_pointer + STEP)
    await call.message.edit_text(text="Вот, что нам удалось найти",
                                 reply_markup=keyboard.page_college_keyboard(data_list))


@router.callback_query(F.data == "college_previous")
async def callback(call: CallbackQuery, state: FSMContext) -> None:
    print("college_prev")

    user_data = await state.get_data()
    user_pointer = user_data.get("pointer_college")
    if user_pointer <= STEP:
        await call.answer()
        return

    data_list = await db.get_college_by_type(filter_user=user_data.get("type"),
                                             limit=STEP,
                                             skip=(user_pointer - BACK_STEP))
    await state.update_data(pointer_college=user_pointer - STEP)
    await call.message.edit_text(text="Вот, что нам удалось найти",
                                 reply_markup=keyboard.page_college_keyboard(data_list))
