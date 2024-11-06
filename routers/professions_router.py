from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import keyboard
from FSM import UserState
from data_base import MongoDB

router = Router()

STEP = 10
BACK_STEP = STEP * 2
db = MongoDB()


@router.message(UserState.use_bot, F.text == "Перечень подходящих профессий")
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    data_list = await db.get_prof_by_type(filter_user=user_data.get("type"), limit=STEP, skip=0)
    count = await db.get_prof_count_by_type(user_data.get("type"))
    await state.update_data(pointer_prof=STEP, count_prof=count.get("count"))
    print(data_list)
    await message.answer("Вот, что нам удалось найти", reply_markup=keyboard.page_prof_keyboard(data_list))


@router.callback_query(F.data.startswith("cbprof_"))
async def select_prof(call: CallbackQuery, state: FSMContext) -> None:
    request_code = call.data.replace("cbprof_", "")
    collage_list = await db.get_college_by_code(request_code)
    for college in collage_list:
        text = college["college"] + "\n"
        text += college["code"] + " " + college["prof"] + "\n"
        text += "\n"
        if "link" in college:
            text += "Официальный сайт:\n" + college["link"] + "\n"
        if "socnet" in college:
            text += "Социальная сеть:\n" + college["socnet"] + "\n"
        await call.message.answer(text)
    await call.answer()


@router.callback_query(F.data == "prof_next")
async def callback(call: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_pointer = user_data.get("pointer_prof")
    if user_pointer >= user_data.get("count_prof"):
        await call.answer()
        return

    data_list = await db.get_prof_by_type(filter_user=user_data.get("type"),
                                          limit=STEP,
                                          skip=user_pointer)
    await state.update_data(pointer_prof=user_pointer + STEP)
    print(
        "\n-----",
        "\ncommand: next",
        "\nsend db skip: ", user_pointer,
        "\nsend db limin: ", STEP,
        "\n-----"
    )
    await call.message.edit_text(text="Вот, что нам удалось найти", reply_markup=keyboard.page_prof_keyboard(data_list))


@router.callback_query(F.data == "prof_previous")
async def callback(call: CallbackQuery, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_pointer = user_data.get("pointer_prof")
    if user_pointer <= STEP:
        await call.answer()
        return

    data_list = await db.get_prof_by_type(filter_user=user_data.get("type"),
                                          limit=STEP,
                                          skip=(user_pointer - BACK_STEP))
    await state.update_data(pointer_prof=user_pointer - STEP)
    print(
        "\n-----",
        "\ncommand: prev",
        "\nsend db skip: ", user_pointer - BACK_STEP,
        "\nsend db limin: ", STEP,
        "\n-----"
    )
    await call.message.edit_text(text="Вот, что нам удалось найти", reply_markup=keyboard.page_prof_keyboard(data_list))
