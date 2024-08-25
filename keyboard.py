from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def create(titles: list[str]) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for title in titles:
        builder.row(KeyboardButton(text=title))
    keyboard = ReplyKeyboardMarkup(keyboard=builder.export())
    keyboard.resize_keyboard = True
    return keyboard


def main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        "Перечень подходящих профессий",
        "Перечень образовательных организаций",
        "FAQ, контакты",
    ]
    return create(keyboard)


def page_prof_keyboard(titles: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for title in titles:
        builder.button(text=title.get("prof"), callback_data=f"cbprof_{title.get('code')}")

    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="Назад", callback_data="prof_previous"),
                InlineKeyboardButton(text="Далее", callback_data="prof_next")
                )
    return builder.as_markup()


def page_college_keyboard(buttons: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for button in buttons:
        builder.button(text=button.get("college"), callback_data=f"cbcollege_{button.get('hash_college')}")

    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="Назад", callback_data="college_previous"),
                InlineKeyboardButton(text="Далее", callback_data="college_next")
                )
    return builder.as_markup()


def page_faq_keyboard(buttons: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for button in buttons:
        builder.button(text=button.get("question"), callback_data=f"cbfaq_{button.get('_id').__str__()}")

    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="Назад", callback_data="faq_previous"),
                InlineKeyboardButton(text="Далее", callback_data="faq_next")
                )
    return builder.as_markup()


def types_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text="Человек-человек", callback_data="type_human")],
        [InlineKeyboardButton(text="Человек-техника", callback_data="type_tech")],
        [InlineKeyboardButton(text="Человек-природа", callback_data="type_nature")],
        [InlineKeyboardButton(text="Человек-знак", callback_data="type_sign")],
        [InlineKeyboardButton(text="Человек-художественный образ", callback_data="type_art")],
        [InlineKeyboardButton(text="Я не знаю свой тип", callback_data="type_idk")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
