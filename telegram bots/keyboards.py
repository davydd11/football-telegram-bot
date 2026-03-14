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
