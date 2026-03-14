"""
Telegram Football Players Bot.

This bot allows users to:
- add football players
- search players by name
- view top players based on goals
- interact through Telegram commands and buttons.
"""

import asyncio
import logging
import json
from modules import Player

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import TOKEN
from keyboards import create_buttons_keyboard
from data import find_player_by_name, save_player_to_file, get_top_players
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

def load_players():
    """
    Load players from the JSON database.

    Returns:
        list[Player]: List of Player objects.
    """
    try:
        with open("players.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return [Player(**player) for player in data]
    except FileNotFoundError:
        return []


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

        players = get_top_players()

        if not players:
            await callback.message.answer("No players in database ❌")
            return

        text = "🏆 <b>Top 5 Players (by goals)</b>\n\n"

        for i, player in enumerate(players, start=1):
            text += (
                f"{i}. ⚽ <b>{player.name}</b>\n"
                f"Goals: {player.goals}\n"
                f"Club: {player.club}\n\n"
            )

        await callback.message.answer(text)

        logging.info("Button pressed")

    elif callback.data == "buttons_help":
        await callback.message.answer(
            "/find_player - find player info\n"
            "/add_player - add new player\n"
            "/top - show top players"
        )
        logging.info("Button pressed")

    await callback.answer()



# =============================
# COMMANDS
# =============================


@dp.message(START_COMMAND)
async def command_start_handler(message: Message):
    """
    Handle the /start command and show the main menu.
    """
    await message.answer("Hello! 👋", reply_markup=create_buttons_keyboard())
    logging.info("STARTED THE BOT")


@dp.message(HELP_COMMAND)
async def command_help_handler(message: Message):
    """
    Send help information about available bot commands.
    """

    text = (
        "Here's what I can do:\n\n"

        "/start - restart the bot 🏁\n"
        "/find_player - find player info 🔎\n"
        "/top - show top players 🏆\n"
        "/add_player - add your own player ➕\n"
        "/help - show instructions 🆘"
    )

    await message.answer(
    text,
    reply_markup=create_buttons_keyboard()
    )

    logging.info("Help command used")


@dp.message(TOP_COMMAND)
async def command_top_handler(message: Message):
    """
    Show the top 5 players sorted by number of goals.
    """
    players = get_top_players()

    if not players:
        await message.answer(
            "No players in database ❌",
            reply_markup=create_buttons_keyboard()
        )
        return

    text = "🏆 <b>Top 5 Players (by goals)</b>\n\n"

    for i, player in enumerate(players, start=1):
        text += (
            f"{i}. ⚽ <b>{player.name}</b>\n"
            f"Goals: {player.goals}\n"
            f"Club: {player.club}\n\n"
        )

    await message.answer(
        text,
        reply_markup=create_buttons_keyboard()
    )



# =============================
# FIND PLAYER
# =============================


@dp.message(FINDPLAYER_COMMAND)
async def find_player_start(message: Message, state: FSMContext):
    """
    Start player search process and ask for player name.
    """
    await message.answer("Enter the player's name:")
    await state.set_state(FindPlayer.select_name)
    logging.info("Find player command started")


@dp.message(FindPlayer.select_name)
async def process_find_player(message: Message, state: FSMContext):
    """
    Search for players by name and send their information.
    """
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

            await message.answer_photo(
                photo=player.photo,
                caption=text
            )

        logging.info("Player found")


    else:
        await message.answer("Player not found ❌")
        logging.warning("Player not found")

    await message.answer(
    "What do you want to do next?",
    reply_markup=create_buttons_keyboard()
)

    

# =============================
# ADD PLAYER
# =============================


@dp.message(ADDPLAYER_COMMAND)
async def add_player_start(message: Message, state: FSMContext):
    """
    Start the process of adding a new player.
    """
    await message.answer("Enter player's name:")
    await state.set_state(AddPlayer.select_name)
    logging.info("Started adding player")


@dp.message(AddPlayer.select_name)
async def process_name(message: Message, state: FSMContext):
    """
    Save player's name and ask for age.
    """

    await state.update_data(name=message.text)
    await message.answer("Enter age:")
    await state.set_state(AddPlayer.select_age)


@dp.message(AddPlayer.select_age)
async def process_age(message: Message, state: FSMContext):
    """
    Validate and save player's age.
    """
    if not message.text.isdigit():
        return await message.answer("Enter valid number!")

    await state.update_data(age=int(message.text))
    await message.answer("Enter nationality:")
    await state.set_state(AddPlayer.select_nationality)


@dp.message(AddPlayer.select_nationality)
async def process_nationality(message: Message, state: FSMContext):
    """
    Save player's nationality.
    """

    await state.update_data(nationality=message.text)
    await message.answer("Enter club:")
    await state.set_state(AddPlayer.select_club)


@dp.message(AddPlayer.select_club)
async def process_club(message: Message, state: FSMContext):
    """
    Save player's club information.
    """

    await state.update_data(club=message.text)
    await message.answer("Enter matches:")
    await state.set_state(AddPlayer.select_matches)


@dp.message(AddPlayer.select_matches)
async def process_matches(message: Message, state: FSMContext):
    """
    Save number of matches played by the player.
    """
    if not message.text.isdigit():
        return await message.answer("Enter valid number!")

    await state.update_data(matches=int(message.text))
    await message.answer("Enter goals:")
    await state.set_state(AddPlayer.select_goals)


@dp.message(AddPlayer.select_goals)
async def process_goals(message: Message, state: FSMContext):
    """
    Save number of goals scored by the player.
    """
    if not message.text.isdigit():
        logging.warning("User entered invalid number for goals")
        return await message.answer("Enter valid number!")

    await state.update_data(goals=int(message.text))
    await message.answer("Enter trophies separated by comma:")
    await state.set_state(AddPlayer.select_trophys)


@dp.message(AddPlayer.select_trophys)
async def process_trophys(message: Message, state: FSMContext):
    """
    Save player's trophies list.
    """
    trophys_list = [t.strip() for t in message.text.split(",")]

    await state.update_data(trophys=trophys_list)
    await message.answer("Now please send a photo of the player.")
    await state.set_state(AddPlayer.select_photo)

    
@dp.message(AddPlayer.select_photo, F.photo)
async def process_photo_id(message: Message, state: FSMContext):
    """
    Save player's photo and store player data in the database.
    """

    photo_id = message.photo[-1].file_id

    await state.update_data(photo=photo_id)

    data = await state.get_data()

    player_obj = Player(**data)

    save_player_to_file(player_obj)

    await message.answer(
    f"Player {player_obj.name} successfully added ✅",
    reply_markup=create_buttons_keyboard()
    )


    logging.info("Another player added")

    await state.clear()


@dp.message(AddPlayer.select_photo)
async def no_save_photo(message: Message, state: FSMContext):
    """
    Ask user to send a photo if none was provided.
    """

    await message.answer("You did not send a photo. Please send a photo of the player.")


# =============================
# BOT START
# =============================

async def main():
    """
    Initialize the bot and start polling.
    """

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



