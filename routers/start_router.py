from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import keyboard
from FSM import UserState

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("""
«Совсем не знаю, куда поступать»
«Да всё равно уже, куда поступлю – туда и пойду»
Известны ли вам такие ответы?

Мы сталкиваемся с проблемой выбора профессии, с которой хотелось бы связать свою будущее и зачастую не можем ее решить самостоятельно. Таким образом, мы перекладываем решение на родителей, либо выбираем самую популярную профессию. Такой подход может привести к разочарованию и отчуждению от профессионального пути. 
Но мы нашли решение!

С помощью нашего бота вы можете познакомиться с образовательными организациями, с профессиями и специальностями, а так же об основных особенностях поступления на базе 9 или 11 классов.
""")
    await select_type(message, state)


@router.message(Command("change"))
async def select_type(message: Message, state: FSMContext) -> None:
    await state.set_state(UserState.set_type)
    await message.answer("Для начала нужно выбрать подходящий вам тип профессии",
                         reply_markup=keyboard.types_keyboard())


@router.callback_query(F.data.startswith("type_"), UserState.set_type)
async def callback(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    type_prof = call.data.replace('type_', '')
    if type_prof == "idk":
        await call.message.answer("""
Если кажется, что ни одна профессия вам не подходит, вы просто еще не нашли дело, которое полюбите!
Поэтому важно открыться новому и попробовать силы в неизвестной для себя сфере. С помощью теста вы сможете:
1. Найти то, что никогда не занимались и что может понравиться
2. Понять, что нужно уметь и чем вы можете заниматься по новой специальности
3. Сменить свою область деятельности
Тест не займет много времени, а подошедшие профессии можно будет подробнее разобрать со специалистами профориентационного центра. 

Чтобы пройти тест вам нужно будет перейти по ссылке: 
https://onlinetestpad.com/gnk76aqcoc7s6""",
                                  reply_markup=keyboard.types_keyboard())
    else:
        await state.update_data(type=type_prof)
        await state.set_state(UserState.use_bot)
        await call.message.answer("Отлично! Мы это запоминим и сможем сформировать список, подходящий именно вам!",
                                  reply_markup=keyboard.main_keyboard())

