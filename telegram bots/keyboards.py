import logging

from aiogram.utils.keyboard import InlineKeyboardBuilder


logger = logging.getLogger(__name__)


buttons = {
    "Find Player🔎": "find_player",
    "Add Player➕": "add_player",
    "Top players🏆": "top_players",
    "Help🆘": "help"
}



def create_buttons_keyboard():
    builder = InlineKeyboardBuilder()

    for text, callback in buttons.items():
        builder.button(
            text=text,
            callback_data=f"buttons_{callback}"
        )

    builder.adjust(2)
    """
    makes two buttons in a row.
    """
    logging.info("Keyboard created.")

    return builder.as_markup()
























# from aiogram.utils.keyboard import InlineKeyboardBuilder
# from aiogram.filters.callback_data import CallbackData

# class FilmCallback(CallbackData, prefix="film", sep=";"):
#     id: int
#     name: str
    


# def films_keyboard_markup(films_list:list[dict], offset:int|None = None, skip:int|None = None):
#     """
#     Створює клавіатуру на основі отриманого списку фільмів
#     Приклад використання
#     >>> await message.answer(
#             text="Some text",
#             reply_markup=films_keyboard_markup(films_list)
#         )
#     """
   
#     # Створюємо та налаштовуємо клавіатуру
#     builder = InlineKeyboardBuilder()
#     builder.adjust(1, repeat=True)

#     for index, film_data in enumerate(films_list):
#         # Створюємо об'єкт CallbackData
#         callback_data = FilmCallback(id=index, **film_data)
#         # Додаємо кнопку до клавіатури
#         builder.button(
#             text=f"{callback_data.name}",
#             callback_data=callback_data.pack()
#         )
#     # Повертаємо клавіатуру у вигляді InlineKeyboardMarkup
#     builder.adjust(1, repeat=True)
#     return builder.as_markup()