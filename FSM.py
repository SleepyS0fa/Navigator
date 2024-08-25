from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    set_type = State()
    use_bot = State()
    organizations = State()
    professions = State()
