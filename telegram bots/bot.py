import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import TOKEN
from keyboards import create_buttons_keyboard
from modules import Player
from data import find_player_by_name, save_player_to_file
from state_machine import AddPlayer, FindPlayer
from commands import (
    START_COMMAND,
    HELP_COMMAND,
    TOP_COMMAND,
    ADDPLAYER_COMMAND,
    FINDPLAYER_COMMAND,

    START_BOT_COMMAND,
    HELP_BOT_COMMAND,
    TOP_BOT_COMMAND,
    ADDPLAYER_BOT_COMMAND,
    FINDPLAYER_BOT_COMMAND
)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_logger.log", mode="a", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

dp = Dispatcher()


# =============================
# BUTTON HANDLER
# =============================

@dp.callback_query(lambda c: c.data.startswith("buttons_"))
async def process_buttons(callback: CallbackQuery, state: FSMContext):

    if callback.data == "buttons_find_player":
        await callback.message.answer("Enter player's name:")
        await state.set_state(FindPlayer.select_name)
        logging.info("Button pressed")

    elif callback.data == "buttons_add_player":
        await callback.message.answer("Enter player's name:")
        await state.set_state(AddPlayer.select_name)
        logging.info("Button pressed")

    elif callback.data == "buttons_top_players":
        await callback.message.answer("Top players feature coming soon ⚽")
        logging.info("Button pressed")

    elif callback.data == "buttons_help":
        await callback.message.answer(
            "/find_player - find player info\n"
            "/add_player - add new player\n"
            "/top - show top players"
        )
        logging.info("Button pressed")

    await callback.answer()
    
    """
    Button Handler, makes the keyboard buttons work when pressed.
    """


# =============================
# COMMANDS
# =============================

@dp.message(START_COMMAND)
async def command_start_handler(message: Message):
    await message.answer("Hello! 👋", reply_markup=create_buttons_keyboard())
    logging.info("STARTED THE BOT")

    """Function that starts the bot."""

@dp.message(HELP_COMMAND)
async def command_help_handler(message: Message):

    text = (
        "Here's what I can do:\n\n"

        "/start - restart the bot 🏁\n"
        "/find_player - find player info 🔎\n"
        "/top - show top players 🏆\n"
        "/add_player - add your own player ➕\n"
        "/help - show instructions 🆘"
    )

    await message.answer(text)
    logging.info("Help command used")

    """
    HELP command
    """


@dp.message(TOP_COMMAND)
async def command_top_handler(message: Message):
    await message.answer("Top players feature coming soon ⚽")
    logging.info("Top command used")

    """
    Top command, which shows top 5 players
    """


# =============================
# FIND PLAYER
# =============================

@dp.message(FINDPLAYER_COMMAND)
async def find_player_start(message: Message, state: FSMContext):
    await message.answer("Enter the player's name:")
    await state.set_state(FindPlayer.select_name)
    logging.info("Find player command started")


@dp.message(FindPlayer.select_name)
async def process_find_player(message: Message, state: FSMContext):

    name = message.text
    players = find_player_by_name(name)

    if players:

        for player in players:
            text = (
    f"━━━━━━━━━━━━━━━\n"
    f"⚽ <b>{player.name}</b>\n"
    f"━━━━━━━━━━━━━━━\n\n"

    f"📋 <b>Player Information</b>\n"
    f"🎂 Age: {player.age}\n"
    f"🌍 Nationality: {player.nationality}\n"
    f"🏟 Club: {player.club}\n\n"

    f"📊 <b>Stats</b>\n"
    f"🎮 Matches: {player.matches}\n"
    f"🥅 Goals: {player.goals}\n\n"

    f"🏆 <b>Trophies</b>\n"
    f"{', '.join(player.trophys)}\n"

    f"━━━━━━━━━━━━━━━"
)

            await message.answer(text)

        logging.info("Player found")

    else:
        await message.answer("Player not found ❌")
        logging.warning("Player not found")

    await state.clear()
    
    """
    Function which finds the player
    """

# =============================
# ADD PLAYER
# =============================

@dp.message(ADDPLAYER_COMMAND)
async def add_player_start(message: Message, state: FSMContext):
    await message.answer("Enter player's name:")
    await state.set_state(AddPlayer.select_name)
    logging.info("Started adding player")

    """
    Starts the ADDPLAYER command which add's 
    """


@dp.message(AddPlayer.select_name)
async def process_name(message: Message, state: FSMContext):

    await state.update_data(name=message.text)
    await message.answer("Enter age:")
    await state.set_state(AddPlayer.select_age)


@dp.message(AddPlayer.select_age)
async def process_age(message: Message, state: FSMContext):

    if not message.text.isdigit():
        return await message.answer("Enter valid number!")

    await state.update_data(age=int(message.text))
    await message.answer("Enter nationality:")
    await state.set_state(AddPlayer.select_nationality)


@dp.message(AddPlayer.select_nationality)
async def process_nationality(message: Message, state: FSMContext):

    await state.update_data(nationality=message.text)
    await message.answer("Enter club:")
    await state.set_state(AddPlayer.select_club)


@dp.message(AddPlayer.select_club)
async def process_club(message: Message, state: FSMContext):

    await state.update_data(club=message.text)
    await message.answer("Enter matches:")
    await state.set_state(AddPlayer.select_matches)


@dp.message(AddPlayer.select_matches)
async def process_matches(message: Message, state: FSMContext):

    if not message.text.isdigit():
        return await message.answer("Enter valid number!")

    await state.update_data(matches=int(message.text))
    await message.answer("Enter goals:")
    await state.set_state(AddPlayer.select_goals)


@dp.message(AddPlayer.select_goals)
async def process_goals(message: Message, state: FSMContext):

    if not message.text.isdigit():
        return await message.answer("Enter valid number!")
    
    logging.warning("entered not a valid number")

    await state.update_data(goals=int(message.text))
    await message.answer("Enter trophies separated by comma:")
    await state.set_state(AddPlayer.select_trophys)


@dp.message(AddPlayer.select_trophys)
async def process_trophys(message: Message, state: FSMContext):

    trophys_list = [t.strip() for t in message.text.split(",")]

    await state.update_data(trophys=trophys_list)

    data = await state.get_data()

    player_obj = Player(**data)

    save_player_to_file(player_obj)

    await message.answer(f"Player {player_obj.name} successfully added ✅")

    logging.info("Another player added")

    await state.clear()


# =============================
# BOT START
# =============================

async def main():

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands(
        [
            START_BOT_COMMAND,
            HELP_BOT_COMMAND,
            TOP_BOT_COMMAND,
            ADDPLAYER_BOT_COMMAND,
            FINDPLAYER_BOT_COMMAND
        ]
    )

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())








# @dp.message(ADDPLAYER_COMMAND)
# async def command_start_handler(message: Message) -> None:
#     await message.answer(f"Hello, this is command: {4}")



# @dp.message(CommandStart())
# async def command_start_handler(message: Message) -> None:
#     await message.answer(
#         f"Hello, this is your first bot {html.bold(message.from_user.full_name)}!"
#     )
    

# @dp.message(FILMS_COMMAND)
# async def films(message: Message) -> None:
#     data = get_films()
#     markup = films_keyboard_markup(films_list=data)
#     await message.answer(
#         f"Перелік фільмів. Натисніть на назву фільму для отримання деталей.",
#         reply_markup=markup
#     )


# @dp.message(Command("help"))
# async def cmd_help(message: Message) -> None:
    
#     text = (
#         "<b>Ось що я вмію:</b>\n\n"
#         "/start - Перезапустити бота\n"
#         "/help - Довідка\n"
#         "/roll - Throw a dice 🎲\n"
#         "/fox - Get a Fox 🦊\n"
#         "Frank"
#     )
#     await message.answer(text)


# @dp.message()
# async def echo_handler(message: Message) -> None:
#     try:
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         await message.answer("Nice try!")